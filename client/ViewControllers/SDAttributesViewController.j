@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDEditorAttributesViewController

@implementation SDAttributesViewController : NUModule
{
    @outlet SDEditorAttributesViewController    editorAttributesController;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attributes";
}

+ (CPImage)moduleIcon
{
    return [SDAttribute icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"attributeDataView" forClass:SDAttribute];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Attribute" identifier:[SDAttribute RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"attributes"];
    [self registerContext:context forClass:SDAttribute];
}

- (void)configureEditor:(NUEditorsViewController)anEditorController
{
    [anEditorController registerEditor:editorAttributesController forObjectsWithRESTName:[SDAttribute RESTName]];
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanAdd                = conditionRepoHasPushPermission,
        conditionCanEdit               = anObject && conditionRepoHasPushPermission,
        permittedActionsSet            = [CPSet new];

    if (conditionCanAdd)
        [permittedActionsSet addObject:NUModuleActionAdd];

    if (conditionCanEdit)
    {
        [permittedActionsSet addObject:NUModuleActionEdit];
        [permittedActionsSet addObject:NUModuleActionDelete];
    }
    return permittedActionsSet;
}

@end
