@import <Foundation/Foundation.j>
@import "SDRESTObject.j"

@class SDModelsFetcher
@class SDAttributesFetcher

SDAPIRelationshipChild = @"child"
SDAPIRelationshipMember = @"member"
SDAPIRelationshipRoot = @"root"


@implementation SDAbstractAPI : SDRESTObject
{
    BOOL        _allowsCreate               @accessors(property=allowsCreate);
    BOOL        _allowsDelete               @accessors(property=allowsDelete);
    BOOL        _allowsGet                  @accessors(property=allowsGet);
    BOOL        _allowsUpdate               @accessors(property=allowsUpdate);
    BOOL        _deprecated                 @accessors(property=deprecated);
    CPString    _associatedSpecificationID  @accessors(property=associatedSpecificationID);
    CPString    _associatedReverseAPIID     @accessors(property=associatedReverseAPIID);
    CPString    _path                       @accessors(property=path);
    CPString    _relationship               @accessors(property=relationship);
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
        [self exposeLocalKeyPathToREST:@"associatedReverseAPIID"];


        _relationship = SDAPIRelationshipChild
        _allowsCreate = YES;
        _allowsDelete = YES;
        _allowsGet = YES;
        _allowsUpdate = YES;
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

- (CPString)allowedOperationsString
{
    var ret = @"";

    if (_allowsGet)
        ret += @"Retrieval ";

    if (_allowsCreate)
        ret += @"Creation ";

    if (_allowsUpdate)
        ret += @"Modification ";

    if (_allowsDelete)
        ret += @"Deletion ";

    return ret;
}


#pragma mark -
#pragma mark Utilities

- (void)fetchPath
{
    [self setPath:@""]

    if (_relationship == SDAPIRelationshipRoot && ![[self parentObject] isRoot])
    {
        [self setPath:@"/" + [[self parentObject] objectResourceName]];
    }
    else
    {
        var associatedSpecification = [SDSpecification RESTObjectWithID:_associatedSpecificationID];

        [associatedSpecification fetchAndCallBlock:function(object, connection) {

            if (_relationship == SDAPIRelationshipRoot)
                [self setPath:@"/" + [object objectResourceName]];
            else if ([self RESTName] == [SDParentAPI RESTName])
                [self setPath:@"/" + [object objectResourceName] + @"/id/" + [[self parentObject] objectResourceName]];
            else
                [self setPath:@"/" + [[self parentObject] objectResourceName] + @"/id/" + [object objectResourceName]];
        }];
    }
}

@end
