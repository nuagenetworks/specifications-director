@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@class SDAbstractsFetcher

@implementation SDModel : SDRESTObject
{
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

    SDAbstractsFetcher  _abstracts              @accessors(property=abstracts);
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"model";
}

- (id)init
{
    if (self = [super init])
    {
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

        _abstracts = [SDAbstractsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
