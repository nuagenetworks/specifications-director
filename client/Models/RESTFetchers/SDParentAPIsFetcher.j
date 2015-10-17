@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDParentAPI


@implementation SDParentAPIsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDParentAPI;
}

@end
