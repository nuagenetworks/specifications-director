@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@implementation SDToken : SDRESTObject
{
    CPString    _name  @accessors(property=name);
    CPString    _value @accessors(property=value);
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"token";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"value"];
    }

    return self;
}

@end
