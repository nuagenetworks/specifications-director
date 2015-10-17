@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDRepository


@implementation SDRepositoriesFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDRepository;
}

@end