@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDSpecification


@implementation SDSpecificationsFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDSpecification;
}

@end
