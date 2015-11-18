@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import <NUKit/NUHoverView.j>
@import "../Models/SDModels.j"

@class SDItemizedSpecifications

@implementation SDRepositoriesViewController : NUModule
{
    @outlet CPButton                    buttonDownload;
    @outlet CPButton                    buttonPull;
    @outlet CPTextField                 labelError;
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

    [self showErrorView:NO];
    [self showPullView:NO];
    [self showWorkingView:NO];
}

- (void)moduleDidSelectObjects:(CPArray)someObject
{
    [[NUKit kit] closeExternalWindows];

    [self showErrorView:NO];
    [self showPullView:NO];
    [self showWorkingView:NO];

    if ([someObject count] != 1)
    {
        [hoverView setWidth:230];
        [hoverView showWithAnimation:NO];
        [hoverView setEnabled:NO];

        [SDRepository setCurrentRepository:nil];
        [self setApplicationNameAndIcon];

        [self _showControlButtons:NO];

        return;
    }

    [self _showControlButtons:YES];

    [hoverView setEnabled:YES];
    [SDRepository setCurrentRepository:[someObject firstObject]];
    [self setApplicationNameAndIcon];

    [self _showViewPullIfNeeded];
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    return [super permittedActionsForObject:anObject];
}

- (BOOL)shouldProcessJSONObject:(id)aJSONObject ofType:(CPString)aType eventType:(CPString)anEventType
{
    return YES;
}

- (void)performPostPushOperation
{
    [super performPostPushOperation];
    [self _showViewPullIfNeeded];
}


#pragma mark -
#pragma mark Utilities

- (void)_showViewPullIfNeeded
{
    if (![_currentSelectedObjects count])
        return;

    [self showPullView:![[_currentSelectedObjects firstObject] valid]];
}

- (void)_showControlButtons:(shouldShow)shouldShow
{
    if (!shouldShow)
    {
        [buttonPull setHidden:YES];
        [buttonDownload setHidden:YES];
    }
    else
    {
        var currentRepository = [_currentSelectedObjects firstObject];

        [buttonDownload setHidden:![currentRepository valid]];
        [buttonPull setHidden:![currentRepository valid]];
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
        if ([viewWorking superview])
            return;

        [hoverView setWidth:230];
        [hoverView showWithAnimation:NO];
        [hoverView setEnabled:NO];

        [self _showControlButtons:NO];

        [viewWorking setFrame:[viewEditObject bounds]];
        [viewEditObject addSubview:viewWorking positioned:CPWindowAbove relativeTo:viewEditObject];
        [[NUDataTransferController defaultDataTransferController] showFetchingViewOnView:viewLoadingContainer];
        [tableView setEnabled:NO];
    }
    else
    {
        if (![viewWorking superview])
            return;

        [[NUDataTransferController defaultDataTransferController] hideFetchingViewFromView:viewLoadingContainer];
        [viewWorking removeFromSuperview];
        [tableView setEnabled:YES];
        [hoverView setEnabled:YES];
        [hoverView hideWithAnimation:NO];

        [self _showControlButtons:YES];
    }
}

- (void)showErrorView:(BOOL)shouldShow
{
    if (shouldShow)
    {
        if ([viewError superview])
            return;

        [hoverView setWidth:230];
        [hoverView showWithAnimation:NO];
        [hoverView setEnabled:NO];

        [viewError setFrame:[viewEditObject frame]];
        [viewEditObject addSubview:viewError];
    }
    else
    {
        if (![viewError superview])
            return;

        [hoverView setEnabled:YES];

        [viewError removeFromSuperview];
    }
}

- (void)showPullView:(BOOL)shouldShow
{
    if (shouldShow)
    {
        if ([viewPull superview])
            return;

        [hoverView setWidth:230];
        [hoverView showWithAnimation:NO];
        [hoverView setEnabled:NO];

        [viewPull setFrame:[viewEditObject frame]];
        [viewEditObject addSubview:viewPull positioned:CPWindowAbove relativeTo:viewEditObject];
    }
    else
    {
        if (![viewPull superview])
            return;

        [hoverView setEnabled:YES];

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
    [self showWorkingView:NO];
    [[self visibleSubModule] reload];

    if ([aJob status] == NURESTJobStatusFAILED)
    {
        [labelError setStringValue:[aJob result]];
        [self showErrorView:YES];
    }
}

- (@action)download:(id)aSender
{
    var repository = [_currentSelectedObjects firstObject],
        url = [repository url] + @"/repos/" + [repository organization] + @"/" + [repository repository] + @"/zipball/" + [repository branch];

    window.location.assign(url);
}

- (@action)closeErrorView:(id)aSender
{
    [self showErrorView:NO];
}
@end
