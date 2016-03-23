@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDSpecification


@implementation SDSpecificationsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDSpecification;
}

@end
