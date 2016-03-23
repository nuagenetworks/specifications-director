@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDRepository


@implementation SDRepositoriesFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDRepository;
}

@end
