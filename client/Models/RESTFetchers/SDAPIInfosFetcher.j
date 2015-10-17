@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDAPIInfo


@implementation SDAPIInfosFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAPIInfo;
}

@end
