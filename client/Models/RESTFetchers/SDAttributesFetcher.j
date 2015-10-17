@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTFetcher.j>

@class SDAttribute


@implementation SDAttributesFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAttribute;
}

@end
