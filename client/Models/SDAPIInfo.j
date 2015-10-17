@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@implementation SDAPIInfo : SDRESTObject
{
    CPString    _prefix     @accessors(property=prefix);
    CPString    _root       @accessors(property=root);
    CPString    _version    @accessors(property=version);
}


#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"apiinfo";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"prefix"];
        [self exposeLocalKeyPathToREST:@"root"];
        [self exposeLocalKeyPathToREST:@"version"];
    }

    return self;
}

@end
