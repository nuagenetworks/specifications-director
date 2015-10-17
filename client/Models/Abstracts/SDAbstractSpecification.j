@import <Foundation/Foundation.j>
@import "SDRESTObject.j"

@class SDAttributesFetcher
@class SDChildAPIsFetcher
@class SDModelsFetcher
@class SDParentAPIsFetcher

@implementation SDAbstractSpecification : SDRESTObject
{
    CPString            _name       @accessors(property=name);

    SDAttributesFetcher _attributes @accessors(property=attributes);
    SDChildAPIsFetcher  _childAPIs  @accessors(property=childAPIs);
    SDModelsFetcher     _models     @accessors(property=models);
    SDParentAPIsFetcher _parentAPIs @accessors(property=parentAPIs);
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"name"];

        _models     = [SDModelsFetcher fetcherWithParentObject:self];
        _attributes = [SDAttributesFetcher fetcherWithParentObject:self];
        _childAPIs  = [SDChildAPIsFetcher fetcherWithParentObject:self];
        _parentAPIs = [SDParentAPIsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
