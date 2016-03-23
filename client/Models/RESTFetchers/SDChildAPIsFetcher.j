@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDChildAPI


@implementation SDChildAPIsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDChildAPI;
}

@end
