@import <Foundation/Foundation.j>
@import "SDRESTObject.j"

@class SDAttributesFetcher
@class SDChildAPIsFetcher

@global _pluralize_rest_name

@implementation SDAbstractSpecification : SDRESTObject
{
    BOOL                _allowsCreate           @accessors(property=allowsCreate);
    BOOL                _allowsDelete           @accessors(property=allowsDelete);
    BOOL                _allowsGet              @accessors(property=allowsGet);
    BOOL                _allowsUpdate           @accessors(property=allowsUpdate);
    BOOL                _syncing                @accessors(property=syncing);
    BOOL                _root                   @accessors(property=root);
    CPString            _description            @accessors(property=description);
    CPString            _entityName             @accessors(property=entityName);
    CPString            _name                   @accessors(property=name);
    CPString            _objectResourceName     @accessors(property=objectResourceName);
    CPString            _objectRESTName         @accessors(property=objectRESTName)
    CPString            _package                @accessors(property=package);


    SDAttributesFetcher _attributes             @accessors(property=attributes);
    SDChildAPIsFetcher  _childAPIs              @accessors(property=childAPIs);
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
        [self exposeLocalKeyPathToREST:@"syncing"];
        [self exposeLocalKeyPathToREST:@"entityName"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"objectResourceName"];
        [self exposeLocalKeyPathToREST:@"objectRESTName"];
        [self exposeLocalKeyPathToREST:@"package"];
        [self exposeLocalKeyPathToREST:@"root"];

        [self exposeBindableAttribute:@"filename"];

        _allowsDelete = YES;
        _allowsGet    = YES;
        _allowsUpdate = YES;

        _attributes   = [SDAttributesFetcher fetcherWithParentObject:self];
        _childAPIs    = [SDChildAPIsFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setObjectRESTName:(CPString)anObjectRESTName
{
    if (_objectRESTName == anObjectRESTName)
        return;

    [self willChangeValueForKey:@"objectRESTName"];
    _objectRESTName = anObjectRESTName;
    [self didChangeValueForKey:@"objectRESTName"];

    [self setFilename:_objectRESTName];
    [self setObjectResourceName:_pluralize_rest_name(_objectRESTName)];
    [self setEntityName:[_objectRESTName capitalizedString]];
}

- (void)setFilename:(CPString)aName
{
    if (_name == aName + ".spec")
        return;

    [self willChangeValueForKey:@"name"];
    [self willChangeValueForKey:@"displayName"];
    _name = aName + ".spec"
    [self didChangeValueForKey:@"displayName"];
    [self didChangeValueForKey:@"name"];
}

- (CPString)filename
{
    return _name ? _name.replace(/\.spec$/, @"") : @"";
}

@end
