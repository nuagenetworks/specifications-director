@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDChildAPI


@implementation SDChildAPIsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDChildAPI;
}

@end
