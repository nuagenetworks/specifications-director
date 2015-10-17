@import <Foundation/Foundation.j>
@import <NUKit/NUModuleSelfParent.j>
@import "../Models/SDModels.j"

@class SDModelAbstractsViewController

@implementation SDModelViewController : NUModuleSelfParent
{
    @outlet CPView                          editionViewGeneral;
    @outlet CPView                          viewAbstractsContainer;
    @outlet CPView                          viewContainer;

    @outlet SDModelAbstractsViewController  abstractsController;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Model";
}

+ (CPImage)moduleIcon
{
    return [SDAPIInfo icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [[self view] setBackgroundColor:NUSkinColorGrey];
    [viewContainer setBackgroundColor:NUSkinColorWhite];
    [viewBottom setBorderTopColor:NUSkinColorGrey];

    var frame = [editionViewGeneral frame];
    [frame.size.width = [scrollViewMain contentSize].width];
    [editionViewGeneral setFrame:frame];

    var view = [abstractsController view];

    [viewAbstractsContainer setFrame:[view bounds]];
    [viewAbstractsContainer addSubview:[abstractsController view]];
    [abstractsController setParentModule:self];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleDidShow
{
    [super moduleDidShow];
    [abstractsController willShow];

}

- (void)moduleWillHide
{
    [abstractsController willHide];
    [super moduleWillHide];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Model" identifier:[SDModel RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setAdditionalEditionViews:[editionViewGeneral]];
    [self registerContext:context forClass:SDModel];
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

    [[aParent models] fetchAndCallBlock:function(fetcher, entity, content) {
        [super setCurrentParent:[content firstObject]];
        [abstractsController setCurrentParent:[content firstObject]];
        [super willShow];
    }];
}

@end
