@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDSpecificationAssociator


@implementation SDAPIsViewController : NUModule
{
    @outlet CPCheckBox                  checkBoxAllowsCreate;
    @outlet CPCheckBox                  checkBoxAllowsUpdate;
    @outlet CPPopUpButton               buttonRelationship;
    @outlet CPTextField                 labelRelationship;
    @outlet SDSpecificationAssociator   specificationAssociator;
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

    [self registerDataViewWithName:@"APIDataView" forClass:SDChildAPI];

    [specificationAssociator setDelegate:self];
    [specificationAssociator setDisassociationButtonHidden:YES];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Children API" identifier:[SDChildAPI RESTName]];
    [context setFetcherKeyPath:@"childAPIs"];
    [context setPopover:popover];
    [self registerContext:context forClass:SDChildAPI];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleWillHide
{
    [super moduleWillHide];
    [specificationAssociator setCurrentParent:nil];
}


#pragma mark -
#pragma mark Actions

- (@action)relationshipChanged:(id)aSender
{
    var editedObject = [_currentContext editedObject];

    if ([_currentParent root])
    {
        [popover setContentSize:CGSizeMake(320, 260)];
        [buttonRelationship setHidden:YES];
        [labelRelationship setHidden:YES];
        [checkBoxAllowsUpdate setHidden:YES];
        [checkBoxAllowsCreate setHidden:NO];
        [editedObject setAllowsCreate:YES];
        [editedObject setAllowsUpdate:NO];
        [editedObject setRelationship:SDAPIRelationshipRoot];
        return;
    }

    switch ([editedObject relationship])
    {
        case SDAPIRelationshipChild:
            [popover setContentSize:CGSizeMake(320, 315)];
            [buttonRelationship setHidden:NO];
            [labelRelationship setHidden:NO];
            [checkBoxAllowsUpdate setHidden:YES];
            [checkBoxAllowsCreate setHidden:NO];
            [editedObject setAllowsCreate:YES];
            [editedObject setAllowsUpdate:NO];
            break;

        case SDAPIRelationshipMember:
            [popover setContentSize:CGSizeMake(320, 315)];
            [buttonRelationship setHidden:NO];
            [labelRelationship setHidden:NO];
            [checkBoxAllowsUpdate setHidden:NO];
            [checkBoxAllowsCreate setHidden:YES];
            [editedObject setAllowsCreate:NO];
            [editedObject setAllowsUpdate:YES];
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

@end
