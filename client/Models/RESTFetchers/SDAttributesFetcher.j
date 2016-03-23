@import <Foundation/Foundation.j>
@import <Bambou/NURESTFetcher.j>

@class SDAttribute


@implementation SDAttributesFetcher : NURESTFetcher

+ (Class)managedObjectClass
{
    return SDAttribute;
}

@end
