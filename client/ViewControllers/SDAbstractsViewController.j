@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDModelViewController
@class SDAttributesViewController
@class SDAPIsViewController

@implementation SDAbstractsViewController : NUModule
{
    @outlet SDModelViewController       modelController;
    @outlet SDAttributesViewController  attributesController;
    @outlet SDAPIsViewController        APIsController;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Abstracts";
}

+ (CPImage)moduleIcon
{
    return [SDAbstract icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"specificationDataView" forClass:SDAbstract];
    [self setModuleTitle:@"Abstracts"];
    [self setSubModules:[modelController, attributesController, APIsController]];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Abstract" identifier:[SDAbstract RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"abstracts"];
    [self registerContext:context forClass:SDAbstract];
}

@end
