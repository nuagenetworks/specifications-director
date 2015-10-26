@import <Foundation/Foundation.j>
@import <NUKit/NUModuleItemized.j>
@import "../Models/SDModels.j"

@class SDSpecificationsViewController
@class SDAPIInfoViewController
@class SDAbstractsViewController

@implementation SDItemizedSpecifications : NUModuleItemized
{
    @outlet SDSpecificationsViewController      specificationsController;
    @outlet SDAbstractsViewController           abstractsController;
    @outlet SDAPIInfoViewController             APIInfoController;
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

    [self setSubModules:[specificationsController, abstractsController, APIInfoController]];
}


#pragma mark -
#pragma mark NUModuleItemized API

- (CPArray)moduleItemizedCurrentItems
{
    return  [   {"module": specificationsController, "children": nil},
                {"module": abstractsController, "children": nil},
                {"module": nil},
                {"module": APIInfoController, "children": nil}
            ];
}

@end
