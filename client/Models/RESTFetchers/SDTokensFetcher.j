@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDToken


@implementation SDTokensFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDToken;
}

@end
