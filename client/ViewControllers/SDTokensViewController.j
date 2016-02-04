@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@implementation SDTokensViewController : NUModule


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Tokens";
}

+ (CPImage)moduleIcon
{
    return [SDToken icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"tokenDataView" forClass:SDToken];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Token" identifier:[SDToken RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"tokens"];
    [self registerContext:context forClass:SDToken];
}

- (BOOL)shouldProcessJSONObject:(id)aJSONObject ofType:(CPString)aType eventType:(CPString)anEventType
{
    return aJSONObject.owner == [[SDAuth defaultUser] userName];
}

@end
