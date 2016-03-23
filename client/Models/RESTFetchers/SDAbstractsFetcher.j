@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDAbstract


@implementation SDAbstractsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAbstract;
}

@end
