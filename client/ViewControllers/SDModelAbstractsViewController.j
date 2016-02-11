@import <Foundation/Foundation.j>
@import <NUKit/NUModuleAssignation.j>
@import "../Models/SDModels.j"


@implementation SDModelAbstractsViewController : NUModuleAssignation



#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Abstracts";
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self registerDataViewWithName:@"abstractDataView" forClass:SDAbstract];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Abstract" identifier:[SDAbstract RESTName]];
    [context setFetcherKeyPath:@"abstracts"];
    [context setPopover:popover];
    [self registerContext:context forClass:SDAbstract];
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanAdd                = conditionRepoHasPushPermission,
        conditionCanEdit               = anObject && conditionRepoHasPushPermission,
        permittedActionsSet            = [CPSet new];

    if (conditionCanAdd)
        [permittedActionsSet addObject:NUModuleAssignationActionAssign];

    if (conditionCanEdit)
        [permittedActionsSet addObject:NUModuleAssignationActionUnassign];

    return permittedActionsSet;
}


#pragma mark -
#pragma mark NUModuleAssignation API

- (void)configureObjectsChooser:(NUObjectChooser)anObjectChooser
{
    [anObjectChooser setModuleTitle:"Select Abstracts Specification"];
    [anObjectChooser registerDataViewWithName:@"abstractDataView" forClass:SDAbstract];
}

- (NUVSDObject)parentOfAssociatedObject
{
    return [SDRepository currentRepository];
}

- (void)assignObjects:(CPArray)someObjects
{
    [_currentParent assignEntities:someObjects ofClass:SDAbstract andCallSelector:nil ofObject:nil];
}

@end
