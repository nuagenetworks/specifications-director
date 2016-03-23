@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDAPIInfo


@implementation SDAPIInfosFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAPIInfo;
}

@end
