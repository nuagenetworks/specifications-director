@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import <NUKit/NUHoverView.j>
@import "../Models/SDModels.j"

@class SDItemizedSpecifications

@implementation SDRepositoriesViewController : NUModule
{
    @outlet NUHoverView                 hoverView;
    @outlet CPView                      viewRepositories;

    @outlet SDItemizedSpecifications    itemizedSpecificationsController;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"repositories";
}

+ (BOOL)automaticSelectionSaving
{
    return NO;
}

+ (CPImage)moduleIcon
{
    return [SDRepostory icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"repositoryDataView" forClass:SDRepository];

    var size = [hoverView contentSize];
    [hoverView setDocumentView:viewRepositories];
    [hoverView setWidth:230];
    [hoverView showWithAnimation:NO];
    [hoverView setEnabled:NO];
    [hoverView setDelegate:self];

    [hoverView setWidth:200];
    [hoverView showWithAnimation:NO];
    [hoverView setEnabled:NO];

    var frame = [[self view] bounds];
    frame.size.width = [hoverView frameSize].width;
    [hoverView setFrame:frame];
    [[self view] addSubview:hoverView positioned:CPWindowAbove relativeTo:nil];

    var frame = [viewTabsContainer frame];
    frame.origin.x = NUHoverViewTriggerWidth;
    frame.size.width -= NUHoverViewTriggerWidth;
    [viewTabsContainer setFrame:frame];

    [self setApplicationNameAndIcon];

    [self setSubModules:[itemizedSpecificationsController]];
    [self setCurrentParent:nil];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Repository" identifier:[SDRepository RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"repositories"];
    [self registerContext:context forClass:SDRepository];
}

#pragma mark -
#pragma mark NUModule API

- (void)moduleWillHide
{
    [super moduleWillHide];

    [SDRepository setCurrentRepository:nil];
    [self setApplicationNameAndIcon];
    [tableView deselectAll];

    [hoverView showWithAnimation:NO];
    [hoverView setEnabled:NO];
}

- (void)moduleDidSelectObjects:(CPArray)someObject
{
    [[NUKit kit] closeExternalWindows];

    if ([someObject count] != 1)
    {
        [hoverView setWidth:230];
        [hoverView showWithAnimation:NO];
        [hoverView setEnabled:NO];

        [SDRepository setCurrentRepository:nil];
        [self setApplicationNameAndIcon];

        return;
    }

    [hoverView setEnabled:YES];
    [SDRepository setCurrentRepository:[someObject firstObject]];
    [self setApplicationNameAndIcon];
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    return [super permittedActionsForObject:anObject];
}

- (BOOL)shouldProcessJSONObject:(id)aJSONObject ofType:(CPString)aType eventType:(CPString)anEventType
{
    return YES;
}


#pragma mark -
#pragma mark Utilities

- (void)setApplicationNameAndIcon
{
    [[NUKit kit] bindApplicationNameToObject:[SDRepository currentRepository] withKeyPath:@"name"];
}

@end
