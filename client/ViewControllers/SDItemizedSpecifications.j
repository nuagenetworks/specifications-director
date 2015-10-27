@import <Foundation/Foundation.j>
@import <NUKit/NUModuleItemized.j>
@import "../Models/SDModels.j"

@class SDAbstractsViewController
@class SDAPIInfoViewController
@class SDMonolitheConfigsViewController
@class SDSpecificationsViewController

@implementation SDItemizedSpecifications : NUModuleItemized
{
    @outlet SDAbstractsViewController           abstractsController;
    @outlet SDAPIInfoViewController             APIInfoController;
    @outlet SDMonolitheConfigsViewController    monolitheConfigController;
    @outlet SDSpecificationsViewController      specificationsController;
}

#pragma mark -
#pragma mark Initialization

// + (CPColor)backgroundColor
// {
//     return NUSkinColorWhite;
// }
//
// + (CPColor)selectionColor
// {
//     return NUSkinColorGrey;
// }
//
// + (CPColor)itemBorderColor
// {
//     return nil;
// }
//
// + (CPColor)itemTextColor
// {
//     return NUSkinColorBlack;
// }
//
// + (CPColor)itemSelectedTextColor
// {
//     return NUSkinColorBlack;
// }
//
// + (CPColor)separatorColor
// {
//     return NUSkinColorGreyLight;
// }

+ (CPString)moduleName
{
    return @"Specifications";
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self setSubModules:[specificationsController, abstractsController, APIInfoController, monolitheConfigController]];
}


#pragma mark -
#pragma mark NUModuleItemized API

- (CPArray)moduleItemizedCurrentItems
{
    return  [   {"module": specificationsController, "children": nil},
                {"module": abstractsController, "children": nil},
                {"module": nil},
                {"module": APIInfoController, "children": nil},
                {"module": monolitheConfigController, "children": nil}
            ];
}

@end
