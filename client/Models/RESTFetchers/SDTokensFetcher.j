@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDToken


@implementation SDTokensFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDToken;
}

@end