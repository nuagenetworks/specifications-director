@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@class SDModelsFetcher
@class SDAttributesFetcher

SDAPIRelationshipChild = @"child"
SDAPIRelationshipMember = @"member"
SDAPIRelationshipRoot = @"root"


@implementation SDChildAPI : SDRESTObject
{
    BOOL        _allowsBulkCreate           @accessors(property=allowsBulkCreate);
    BOOL        _allowsBulkDelete           @accessors(property=allowsBulkDelete);
    BOOL        _allowsBulkUpdate           @accessors(property=allowsBulkUpdate);
    BOOL        _allowsCreate               @accessors(property=allowsCreate);
    BOOL        _allowsDelete               @accessors(property=allowsDelete);
    BOOL        _allowsGet                  @accessors(property=allowsGet);
    BOOL        _allowsUpdate               @accessors(property=allowsUpdate);
    BOOL        _deprecated                 @accessors(property=deprecated);
    CPString    _associatedSpecificationID  @accessors(property=associatedSpecificationID);
    CPString    _path                       @accessors(property=path);
    CPString    _relationship               @accessors(property=relationship);
}

+ (CPString)RESTName
{
    return @"childapi";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"allowsCreate"];
        [self exposeLocalKeyPathToREST:@"allowsDelete"];
        [self exposeLocalKeyPathToREST:@"allowsGet"];
        [self exposeLocalKeyPathToREST:@"allowsUpdate"];
        [self exposeLocalKeyPathToREST:@"associatedSpecificationID"];
        [self exposeLocalKeyPathToREST:@"deprecated"];
        [self exposeLocalKeyPathToREST:@"relationship"];
        [self exposeLocalKeyPathToREST:@"path"];
        [self exposeLocalKeyPathToREST:@"allowsBulkCreate"];
        [self exposeLocalKeyPathToREST:@"allowsBulkDelete"];
        [self exposeLocalKeyPathToREST:@"allowsBulkUpdate"];

        _allowsBulkCreate = NO;
        _allowsBulkDelete = NO;
        _allowsBulkUpdate = NO;
        _allowsCreate     = YES;
        _allowsDelete     = NO;
        _allowsGet        = YES;
        _allowsUpdate     = NO;
        _relationship     = SDAPIRelationshipChild
    }

    return self;
}

- (void)setAllowsCreate:(BOOL)shouldAllow
{
    if (_allowsCreate == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsCreate"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsCreate = shouldAllow
    [self didChangeValueForKey:@"allowsCreate"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsGet:(BOOL)shouldAllow
{
    if (_allowsGet == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsGet"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsGet = shouldAllow
    [self didChangeValueForKey:@"allowsGet"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsUpdate:(BOOL)shouldAllow
{
    if (_allowsUpdate == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsUpdate"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsUpdate = shouldAllow
    [self didChangeValueForKey:@"allowsUpdate"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsDelete:(BOOL)shouldAllow
{
    if (_allowsDelete == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsDelete"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsDelete = shouldAllow
    [self didChangeValueForKey:@"allowsDelete"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsBulkCreate:(BOOL)shouldAllow
{
    if (_allowsBulkCreate == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsBulkCreate"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsBulkCreate = shouldAllow
    [self didChangeValueForKey:@"allowsBulkCreate"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsBulkUpdate:(BOOL)shouldAllow
{
    if (_allowsBulkUpdate == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsBulkUpdate"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsBulkUpdate = shouldAllow
    [self didChangeValueForKey:@"allowsBulkUpdate"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (void)setAllowsBulkDelete:(BOOL)shouldAllow
{
    if (_allowsBulkDelete == shouldAllow)
        return;

    [self willChangeValueForKey:@"allowsBulkDelete"];
    [self willChangeValueForKey:@"allowedOperationsString"];
    _allowsBulkDelete = shouldAllow
    [self didChangeValueForKey:@"allowsBulkDelete"];
    [self didChangeValueForKey:@"allowedOperationsString"];
}

- (CPString)allowedOperationsString
{
    var ret = @"";

    if (_allowsGet)
        ret += @"Retrieval, ";

    if (_allowsCreate)
        ret += @"Creation, ";

    if (_allowsUpdate)
        ret += @"Modification, ";

    if (_allowsDelete)
        ret += @"Deletion, ";

    if (_allowsBulkCreate)
        ret += @"Bulk Creation, ";

    if (_allowsBulkUpdate)
        ret += @"Bulk Modification, ";

    if (_allowsBulkDelete)
        ret += @"Bulk Deletion, ";

    if (ret.length > 2)
        ret = ret.substring(0, ret.length - 2);

    return ret;
}

@end
