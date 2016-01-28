@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import <NUKit/NUHoverView.j>
@import "../Models/SDModels.j"

@class SDItemizedSpecifications
@global SDRepositoryStatusNEEDS_PULL
@global SDRepositoryStatusPULLING
@global SDRepositoryStatusREADY
@global SDRepositoryStatusERROR


@implementation SDRepositoriesViewController : NUModule
{
    @outlet CPButton                    buttonDownload;
    @outlet CPButton                    buttonPull;
    @outlet CPButton                    buttonOpen;
    @outlet CPTextField                 labelError;
    @outlet CPTextField                 labelPulling;
    @outlet CPView                      viewError;
    @outlet CPView                      viewLoadingContainer;
    @outlet CPView                      viewPull;
    @outlet CPView                      viewRepositories;
    @outlet CPView                      viewWorking;
    @outlet NUHoverView                 hoverView;

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

    [viewSubtitleContainer setBackgroundColor:[CPColor colorWithHexString:@"e21b2d"]];
    [self _showControlButtons:NO];

    [viewError setBackgroundColor:NUSkinColorGreyLight];
    [viewPull setBackgroundColor:NUSkinColorGreyLight];
    [viewWorking setBackgroundColor:NUSkinColorGreyLight];

    [buttonPull setThemeState:CPThemeStateDefault];
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
    [self _showControlButtons:NO];

    [hoverView showWithAnimation:NO];
    [hoverView setEnabled:NO];

    [self _updateCurrentStateView];
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

        [self _showControlButtons:NO];
    }
    else
    {
        [hoverView setEnabled:YES];

        [SDRepository setCurrentRepository:[someObject firstObject]];

        [self setApplicationNameAndIcon];

        [self _showControlButtons:YES];
    }

    [self _updateCurrentStateView];
}

- (BOOL)shouldProcessJSONObject:(id)aJSONObject ofType:(CPString)aType eventType:(CPString)anEventType
{
    return YES;
}

- (void)performPostPushOperation
{
    [super performPostPushOperation];
    [self _updateCurrentStateView];
}


#pragma mark -
#pragma mark Utilities

- (void)_updateCurrentStateView
{
    if (![_currentSelectedObjects count])
    {
        [self showPullView:NO];
        [self showWorkingView:NO];
        [self showErrorView:NO];
        return;
    }

    var repoStatus = [[_currentSelectedObjects firstObject] status];

    switch (repoStatus)
    {
        case SDRepositoryStatusNEEDS_PULL:
            [self showPullView:YES];
            [self showWorkingView:NO];
            [self showErrorView:NO];
            break;

        case SDRepositoryStatusPULLING:
        case SDRepositoryStatusQUEUED:
            [self showPullView:NO];
            [self showWorkingView:YES];
            [self showErrorView:NO];
            break;

        case SDRepositoryStatusERROR:
            [self showPullView:NO];
            [self showWorkingView:NO];
            [self showErrorView:YES];
            break;

        case SDRepositoryStatusREADY:
            [self showPullView:NO];
            [self showWorkingView:NO];
            [self showErrorView:NO];
            break;
    }
}

- (void)_showControlButtons:(shouldShow)shouldShow
{
    if (!shouldShow)
    {
        [buttonPull setHidden:YES];
        [buttonDownload setHidden:YES];
        [buttonOpen setHidden:YES];
    }
    else
    {
        var currentRepository = [_currentSelectedObjects firstObject];

        [buttonDownload setHidden:[currentRepository status] != SDRepositoryStatusREADY];
        [buttonPull setHidden:[currentRepository status] != SDRepositoryStatusREADY];
        [buttonOpen setHidden:[currentRepository status] != SDRepositoryStatusREADY];
    }
}

- (void)setApplicationNameAndIcon
{
    [[NUKit kit] bindApplicationNameToObject:[SDRepository currentRepository] withKeyPath:@"name"];
}

- (void)showWorkingView:(BOOL)shouldShow
{
    [self showErrorView:NO];

    if (shouldShow)
    {
        var repo = [_currentSelectedObjects firstObject];

        if ([repo status] == SDRepositoryStatusPULLING)
            [labelPulling setStringValue:@"Pulling Specifications from\n" + [repo description] + "@" + [repo branch] + @"..."]
        if ([repo status] == SDRepositoryStatusQUEUED)
            [labelPulling setStringValue:@"Operation Enqueued.\nWaiting for next available pulling slot."];

        if ([viewWorking superview])
            return;

        [self _showControlButtons:NO];

        [viewWorking setFrame:[viewEditObject bounds]];
        [viewEditObject addSubview:viewWorking positioned:CPWindowAbove relativeTo:viewEditObject];
        [[NUDataTransferController defaultDataTransferController] showFetchingViewOnView:viewLoadingContainer];
    }
    else
    {
        if (![viewWorking superview])
            return;

        [[NUDataTransferController defaultDataTransferController] hideFetchingViewFromView:viewLoadingContainer];
        [viewWorking removeFromSuperview];

        [self _showControlButtons:YES];
    }
}

- (void)showErrorView:(BOOL)shouldShow
{
    if (shouldShow)
    {
        if ([viewError superview])
            return;

        [viewError setFrame:[viewEditObject frame]];
        [viewEditObject addSubview:viewError];
    }
    else
    {
        if (![viewError superview])
            return;


        [viewError removeFromSuperview];
    }
}

- (void)showPullView:(BOOL)shouldShow
{
    if (shouldShow)
    {
        if ([viewPull superview])
            return;

        [viewPull setFrame:[viewEditObject bounds]];
        [viewEditObject addSubview:viewPull positioned:CPWindowAbove relativeTo:viewEditObject];
    }
    else
    {
        if (![viewPull superview])
            return;

        [viewPull removeFromSuperview];
    }
}


#pragma mark -
#pragma mark Actions

- (@action)pull:(id)aSender
{
    [[NURESTJobsController defaultController] postJob:[SDPullJob new] toEntity:[_currentSelectedObjects firstObject] andCallSelector:@selector(_didPull:) ofObject:self];
    [self showWorkingView:YES];
}

- (void)_didPull:(NURESTJob)aJob
{
    if ([aJob parentID] != [[_currentSelectedObjects firstObject] ID])
        return;

    [[[self visibleSubModule] visibleSubModule] reload];

    if ([aJob status] == NURESTJobStatusFAILED)
        [labelError setStringValue:[aJob result]];

    [self _updateCurrentStateView];
}

- (@action)download:(id)aSender
{
    var repository = [_currentSelectedObjects firstObject],
        url = [repository url].replace(@"api/v3", @"") + [repository organization] + @"/" + [repository repository] + @"/zipball/" + [repository branch];

    window.location.assign(url);
}

- (@action)openInGithub:(id)aSender
{
    var repository = [_currentSelectedObjects firstObject],
        url = [repository url].replace(@"api/v3", @"") + [repository organization] + @"/" + [repository repository] + @"/tree/" + [repository branch];

    window.open(url, @"_new");
}

- (@action)closeErrorView:(id)aSender
{
    [[_currentSelectedObjects firstObject] setStatus:SDRepositoryStatusNEEDS_PULL];
    [[_currentSelectedObjects firstObject] saveAndCallSelector:nil ofObject:nil];

    [self showPullView:YES];
    [self showErrorView:NO];
}
@end
