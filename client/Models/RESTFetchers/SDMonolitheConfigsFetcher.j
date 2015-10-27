@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDMonolitheConfig


@implementation SDMonolitheConfigsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDMonolitheConfig;
}

@end