@import <Foundation/Foundation.j>
@import "Abstracts/SDAbstractSpecification.j"

@class SDAbstractsFetcher

@implementation SDSpecification : SDAbstractSpecification
{
    SDAbstractsFetcher  _abstracts @accessors(property=abstracts);
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"specification";
}

- (id)init
{
    if (self = [super init])
    {
        _abstracts = [SDAbstractsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
