@import <Foundation/Foundation.j>
@import <NUKit/NUModuleSelfParent.j>
@import "../Models/SDModels.j"

@implementation SDAPIInfoViewController : NUModuleSelfParent
{
    @outlet CPTextField fieldAPIVersion;
    @outlet CPTextField fieldAPIPrefix;
    @outlet CPView      editionViewGeneral;
    @outlet CPView      viewContainer;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"API Information";
}

+ (CPImage)moduleIcon
{
    return [SDAPIInfo icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [[self view] setBackgroundColor:NUSkinColorGrey];
    [scrollViewMain setBorderTopColor:NUSkinColorGrey];
    [viewContainer setBackgroundColor:NUSkinColorWhite];
    [viewBottom setBorderTopColor:NUSkinColorGrey];
}


#pragma mark -
#pragma mark NUModule API

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"API Info" identifier:[SDAPIInfo RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setAdditionalEditionViews:[editionViewGeneral]];
    [self registerContext:context forClass:SDAPIInfo];
}

- (CPArray)moduleCurrentVisibleEditionViews
{
    return [editionViewGeneral];
}

- (void)performPostPushOperation
{
    [super performPostPushOperation];
    [self updateVisibleEditionsView:self];
}

- (void)moduleUpdateEditorInterface
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanEdit               = conditionRepoHasPushPermission;

    [_currentContext setBoundControlsEnabled:conditionCanEdit];
}


#pragma mark -
#pragma mark Actions

- (@action)updateVisibleEditionsView:(id)aSender
{
    [self reloadStackView];
}


#pragma mark -
#pragma mark Overrides

- (void)willShow
{
    // pass here, see below.
}

- (void)setCurrentParent:(NUVSDObject)aParent
{
    if (!aParent)
    {
        [super setCurrentParent:nil];
        return;
    }

    [[aParent APIInfos] fetchAndCallBlock:function(fetcher, entity, content) {
        [super setCurrentParent:[content firstObject]];
        [super willShow];
    }];
}

@end
