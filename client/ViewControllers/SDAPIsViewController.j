@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDSpecificationAssociator


@implementation SDAPIsViewController : NUModule
{
    @outlet CPCheckBox                  checkBoxAllowsCreate;
    @outlet CPCheckBox                  checkBoxAllowsUpdate;
    @outlet CPPopUpButton               buttonRelationship;
    @outlet SDSpecificationAssociator   specificationAssociator;

    NUCategory  _categoryParentAPIs;
    NUCategory  _categoryChildAPIs;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"APIs";
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self registerDataViewWithName:@"APIDataView" forClass:SDParentAPI];
    [self registerDataViewWithName:@"APIDataView" forClass:SDChildAPI];

    _categoryParentAPIs = [NUCategory categoryWithName:@"Parent APIs"];
    _categoryChildAPIs  = [NUCategory categoryWithName:@"Child APIs"];

    [self setCategories:[_categoryParentAPIs, _categoryChildAPIs]];

    [specificationAssociator setDelegate:self];
    [specificationAssociator setDisassociationButtonHidden:YES];
}

- (void)configureContexts
{
    var childContext = [[NUModuleContext alloc] initWithName:@"Children API" identifier:[SDChildAPI RESTName]];
    [childContext setFetcherKeyPath:@"childAPIs"];
    [self registerContext:childContext forClass:SDChildAPI];

    var parentContext = [[NUModuleContext alloc] initWithName:@"Parent API" identifier:[SDParentAPI RESTName]];
    [parentContext setPopover:popover];
    [parentContext setFetcherKeyPath:@"parentAPIs"];
    [self registerContext:parentContext forClass:SDParentAPI];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleWillHide
{
    [super moduleWillHide];

    [specificationAssociator setCurrentParent:nil];
}

- (CPArray)moduleCurrentActiveContexts
{
    return [_contextRegistry allValues];
}

- (NUCategory)categoryForObject:(NUVSDObject)anObject
{
    return [anObject RESTName] == [SDParentAPI RESTName] ? _categoryParentAPIs : _categoryChildAPIs;
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    var conditionParentAPI  = [anObject RESTName] == [SDParentAPI RESTName],
        conditionRootAPI    = [_currentParent objectRESTName] == [_currentParent rootRESTName],
        conditionCanEdit    = anObject && conditionParentAPI,
        permittedActionsSet = [CPSet new];

    if (conditionRootAPI)
        return permittedActionsSet;

    [permittedActionsSet addObject:NUModuleActionAdd];

    if (conditionCanEdit)
    {
        [permittedActionsSet addObject:NUModuleActionEdit];
        [permittedActionsSet addObject:NUModuleActionDelete];
    }

    return permittedActionsSet;
}

#pragma mark -
#pragma mark Actions

- (@action)relationshipChanged:(id)aSender
{
    var editedObject = [_currentContext editedObject];

    switch ([editedObject relationship])
    {
        case SDAPIRelationshipChild:
            [checkBoxAllowsUpdate setHidden:YES];
            [checkBoxAllowsCreate setHidden:NO];
            [editedObject setAllowsCreate:NO];
            [buttonRelationship setHidden:NO];
            break;

        case SDAPIRelationshipMember:
            [checkBoxAllowsUpdate setHidden:NO];
            [checkBoxAllowsCreate setHidden:YES];
            [editedObject setAllowsUpdate:NO];
            [buttonRelationship setHidden:NO];
            break;

        case SDAPIRelationshipRoot:
            [checkBoxAllowsUpdate setHidden:YES];
            [checkBoxAllowsCreate setHidden:NO];
            [editedObject setAllowsUpdate:NO];
            [buttonRelationship setHidden:YES];
            break;
    }
}


#pragma mark -
#pragma mark NUModuleContext Delegate

- (void)moduleContext:(NUModuleContext)aContext willManageObject:(NUVSDObject)anObject
{
    [self relationshipChanged:self];
    [specificationAssociator setCurrentParent:anObject];
}


#pragma mark -
#pragma mark Associator Delegates

- (void)didAssociatorFetchAssociatedObject:(id)anAssociator
{
    if ([[anAssociator currentAssociatedObject] objectRESTName] == [_currentParent rootRESTName])
        [[_currentContext editedObject] setRelationship:SDAPIRelationshipRoot];
    else
        [[_currentContext editedObject] setRelationship:SDAPIRelationshipChild];

    [self relationshipChanged:self];
}

@end
