@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDTokensViewController


@implementation SDConfigurationViewController: NUModule
{
    @outlet SDTokensViewController      tokensController;

    @outlet CPButton                    buttonBack @accessors(readonly);
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Preferences";
}

+ (CPImage)moduleIcon
{
    return CPImageInBundle(@"toolbar-preferences.png");
}


+ (BOOL)isTableBasedModule
{
    return NO;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self setSubModules:[tokensController]];

    [viewTitleContainer setBackgroundColor:NUSkinColorRed];
    [viewTitleContainer setBorderBottomColor:nil];
}

@end
