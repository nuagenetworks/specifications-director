@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../../Models/SDModels.j"

@class SDSpecificationAssociator


@implementation SDAbstractAPIsViewController : NUModule
{
    @outlet CPCheckBox                  checkBoxAllowsCreate;
    @outlet CPCheckBox                  checkBoxAllowsUpdate;
    @outlet SDSpecificationAssociator   specificationAssociator;
}

#pragma mark -
#pragma mark Initialization

+ (CPImage)moduleIcon
{
    return [[self managedAPIClass] icon];
}

+ (id)managedAPIClass
{
    throw ("implement me");
}

+ (CPString)managedAPIName
{
    throw ("implement me");
}

+ (CPString)managedAPIsFetcherKeyPath
{
    throw ("implement me");
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self registerDataViewWithName:@"APIDataView" forClass:[[self class] managedAPIClass]];

    [specificationAssociator setDelegate:self];
    [specificationAssociator setDisassociationButtonHidden:YES];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:[[self class] managedAPIName] identifier:[[[self class] managedAPIClass] RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:[[self class] managedAPIsFetcherKeyPath]];
    [self registerContext:context forClass:[[self class] managedAPIClass]];
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

    if ([editedObject relationship] == SDAPIRelationshipChild)
    {
        [checkBoxAllowsUpdate setHidden:YES];
        [checkBoxAllowsCreate setHidden:NO];
        [editedObject setAllowsCreate:NO];
    }
    else
    {
        [checkBoxAllowsUpdate setHidden:NO];
        [checkBoxAllowsCreate setHidden:YES];
        [editedObject setAllowsUpdate:NO];
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
