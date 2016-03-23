@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDMonolitheConfig


@implementation SDMonolitheConfigsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDMonolitheConfig;
}

@end
