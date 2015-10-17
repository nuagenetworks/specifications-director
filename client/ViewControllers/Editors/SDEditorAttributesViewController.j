@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../../Models/SDModels.j"

@class SDEditorAttributeSelfViewController


@implementation SDEditorAttributesViewController : NUModule
{
    @outlet SDEditorAttributeSelfViewController selfAttributeController;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attributes";
}

+ (BOOL)moduleTabViewMode
{
    return NUModuleTabViewModeIcon;
}

+ (BOOL)isTableBasedModule
{
    return NO;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self setSubModules:[selfAttributeController]];
}


#pragma mark -
#pragma mark NUModule API

- (CPArray)currentActiveSubModules
{
    return [selfAttributeController];
}

@end
