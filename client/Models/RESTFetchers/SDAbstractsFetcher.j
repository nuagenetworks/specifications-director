@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDAbstract


@implementation SDAbstractsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAbstract;
}

@end
