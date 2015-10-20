@import <Foundation/Foundation.j>
@import "SDRESTObject.j"

@class SDAttributesFetcher
@class SDChildAPIsFetcher
@class SDParentAPIsFetcher

@implementation SDAbstractSpecification : SDRESTObject
{
    BOOL                _allowsCreate           @accessors(property=allowsCreate);
    BOOL                _allowsDelete           @accessors(property=allowsDelete);
    BOOL                _allowsGet              @accessors(property=allowsGet);
    BOOL                _allowsUpdate           @accessors(property=allowsUpdate);
    CPArray             _extends                @accessors(property=extends);
    CPString            _description            @accessors(property=description);
    CPString            _entityName             @accessors(property=entityName);
    CPString            _name                   @accessors(property=name);
    CPString            _objectResourceName     @accessors(property=objectResourceName);
    CPString            _objectRESTName         @accessors(property=objectRESTName)
    CPString            _package                @accessors(property=package);
    CPString            _rootRESTName           @accessors(property=rootRESTName);

    SDAttributesFetcher _attributes             @accessors(property=attributes);
    SDChildAPIsFetcher  _childAPIs              @accessors(property=childAPIs);
    SDParentAPIsFetcher _parentAPIs             @accessors(property=parentAPIs);
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"allowsCreate"];
        [self exposeLocalKeyPathToREST:@"allowsDelete"];
        [self exposeLocalKeyPathToREST:@"allowsGet"];
        [self exposeLocalKeyPathToREST:@"allowsUpdate"];
        [self exposeLocalKeyPathToREST:@"description"];
        [self exposeLocalKeyPathToREST:@"entityName"];
        [self exposeLocalKeyPathToREST:@"extends"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"objectResourceName"];
        [self exposeLocalKeyPathToREST:@"objectRESTName"];
        [self exposeLocalKeyPathToREST:@"package"];
        [self exposeLocalKeyPathToREST:@"rootRESTName"];

        _attributes = [SDAttributesFetcher fetcherWithParentObject:self];
        _childAPIs  = [SDChildAPIsFetcher fetcherWithParentObject:self];
        _parentAPIs = [SDParentAPIsFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setName:(CPString)aName
{
    if (_name == aName)
        return;

    [self willChangeValueForKey:@"name"];
    [self willChangeValueForKey:@"displayName"];
    if (aName.indexOf('.spec') == -1)
        aName += @".spec";

    _name = aName;
    [self didChangeValueForKey:@"name"];
    [self didChangeValueForKey:@"displayName"];
}

- (CPString)displayName
{
    return _name.replace(/\.spec$/, "");
}

- (BOOL)isRoot
{
    return (_objectRESTName == _rootRESTName);
}

@end
