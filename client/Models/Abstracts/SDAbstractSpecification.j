@import <Foundation/Foundation.j>
@import "SDRESTObject.j"

@class SDAttributesFetcher
@class SDChildAPIsFetcher
@class SDParentAPIsFetcher

@implementation SDAbstractSpecification : SDRESTObject
{
    CPString            _name                   @accessors(property=name);
    BOOL                _allowsCreate           @accessors(property=allowsCreate);
    BOOL                _allowsDelete           @accessors(property=allowsDelete);
    BOOL                _allowsGet              @accessors(property=allowsGet);
    BOOL                _allowsUpdate           @accessors(property=allowsUpdate);
    CPArray             _extends                @accessors(property=extends);
    CPString            _description            @accessors(property=description);
    CPString            _entityName             @accessors(property=entityName);
    CPString            _objectResourceName     @accessors(property=objectResourceName);
    CPString            _objectRESTName         @accessors(property=objectRESTName)
    CPString            _package                @accessors(property=package);

    SDAttributesFetcher _attributes             @accessors(property=attributes);
    SDChildAPIsFetcher  _childAPIs              @accessors(property=childAPIs);
    SDParentAPIsFetcher _parentAPIs             @accessors(property=parentAPIs);
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"extends"];
        [self exposeLocalKeyPathToREST:@"description"];
        [self exposeLocalKeyPathToREST:@"entityName"];
        [self exposeLocalKeyPathToREST:@"objectResourceName"];
        [self exposeLocalKeyPathToREST:@"objectRESTName"];
        [self exposeLocalKeyPathToREST:@"package"];
        [self exposeLocalKeyPathToREST:@"allowsCreate"];
        [self exposeLocalKeyPathToREST:@"allowsDelete"];
        [self exposeLocalKeyPathToREST:@"allowsGet"];
        [self exposeLocalKeyPathToREST:@"allowsUpdate"];

        _attributes = [SDAttributesFetcher fetcherWithParentObject:self];
        _childAPIs  = [SDChildAPIsFetcher fetcherWithParentObject:self];
        _parentAPIs = [SDParentAPIsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
