@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@implementation SDMonolitheConfig : SDRESTObject
{
    CPString     _APIDocOutput          @accessors(property=APIDocOutput);
    CPString     _APIDocUserVanilla     @accessors(property=APIDocUserVanilla);
    CPString     _copyright             @accessors(property=copyright);
    CPString     _productAccronym       @accessors(property=productAccronym);
    CPString     _productName           @accessors(property=productName);
    CPString     _SDKAuthor             @accessors(property=SDKAuthor);
    CPString     _SDKBambouVersion      @accessors(property=SDKBambouVersion);
    CPString     _SDKClassPrefix        @accessors(property=SDKClassPrefix);
    CPString     _SDKCLIName            @accessors(property=SDKCLIName);
    CPString     _SDKDescription        @accessors(property=SDKDescription);
    CPString     _SDKDocOutput          @accessors(property=SDKDocOutput);
    CPString     _SDKDocTMPPath         @accessors(property=SDKDocTMPPath);
    CPString     _SDKDocUserVanilla     @accessors(property=SDKDocUserVanilla)
    CPString     _SDKEmail              @accessors(property=SDKEmail);
    CPString     _SDKLicenseName        @accessors(property=SDKLicenseName);
    CPString     _SDKName               @accessors(property=SDKName);
    CPString     _SDKOutput             @accessors(property=SDKOutput)
    CPString     _SDKRevisionNumber     @accessors(property=SDKRevisionNumber);
    CPString     _SDKURL                @accessors(property=SDKURL);
    CPString     _SDKUserVanilla        @accessors(property=SDKUserVanilla);
    CPString     _SDKVersion            @accessors(property=SDKVersion);
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"monolitheconfig";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"APIDocOutput"];
        [self exposeLocalKeyPathToREST:@"APIDocUserVanilla"];
        [self exposeLocalKeyPathToREST:@"copyright"];
        [self exposeLocalKeyPathToREST:@"productAccronym"];
        [self exposeLocalKeyPathToREST:@"productName"];
        [self exposeLocalKeyPathToREST:@"SDKAuthor"];
        [self exposeLocalKeyPathToREST:@"SDKBambouVersion"];
        [self exposeLocalKeyPathToREST:@"SDKClassPrefix"];
        [self exposeLocalKeyPathToREST:@"SDKCLIName"];
        [self exposeLocalKeyPathToREST:@"SDKDescription"];
        [self exposeLocalKeyPathToREST:@"SDKDocOutput"];
        [self exposeLocalKeyPathToREST:@"SDKDocTMPPath"];
        [self exposeLocalKeyPathToREST:@"SDKDocUserVanilla"];
        [self exposeLocalKeyPathToREST:@"SDKEmail"];
        [self exposeLocalKeyPathToREST:@"SDKLicenseName"];
        [self exposeLocalKeyPathToREST:@"SDKName"];
        [self exposeLocalKeyPathToREST:@"SDKOutput"];
        [self exposeLocalKeyPathToREST:@"SDKRevisionNumber"];
        [self exposeLocalKeyPathToREST:@"SDKURL"];
        [self exposeLocalKeyPathToREST:@"SDKUserVanilla"];
        [self exposeLocalKeyPathToREST:@"SDKVersion"];
    }

    return self;
}

@end
