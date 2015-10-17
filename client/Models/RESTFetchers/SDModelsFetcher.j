@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDModel


@implementation SDModelsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDModel;
}

@end
