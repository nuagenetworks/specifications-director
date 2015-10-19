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

- (void)moduleDidSetCurrentParent:(id)aParent
{
    [super moduleDidSetCurrentParent:aParent];

    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController setCurrentParent:_currentParent];

    [self setCurrentContextWithIdentifier:[_currentParent RESTName]];
}

- (void)moduleDidShow
{
    [super moduleDidShow];

    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController willShow];
}

- (void)moduleWillHide
{
    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController willHide];

    [super moduleWillHide];
}

- (void)configureContexts
{
    var contextSpecification = [[NUModuleContext alloc] initWithName:@"Model" identifier:[SDSpecification RESTName]];
    [contextSpecification setButtonSave:buttonSave];
    [contextSpecification setEditionView:[self view]];
    [contextSpecification setAdditionalEditionViews:[editionViewGeneral]];
    [self registerContext:contextSpecification forClass:SDSpecification];

    var contextAbstract = [[NUModuleContext alloc] initWithName:@"Model" identifier:[SDAbstract RESTName]];
    [contextAbstract setButtonSave:buttonSave];
    [contextAbstract setEditionView:[self view]];
    [contextAbstract setAdditionalEditionViews:[editionViewGeneral]];
    [self registerContext:contextAbstract forClass:SDAbstract];
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

@end
