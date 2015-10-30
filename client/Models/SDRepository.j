@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@class SDAbstractsFetcher
@class SDAPIInfosFetcher
@class SDMonolitheConfigsFetcher
@class SDSpecificationsFetcher

NURepositoryCurrent = nil;

@implementation SDRepository : SDRESTObject
{
    BOOL                        _valid              @accessors(property=valid);
    CPString                    _name               @accessors(property=name);
    CPString                    _url                @accessors(property=url);
    CPString                    _username           @accessors(property=username);
    CPString                    _password           @accessors(property=password)
    CPString                    _organization       @accessors(property=organization);
    CPString                    _repository         @accessors(property=repository);
    CPString                    _branch             @accessors(property=branch);
    CPString                    _path               @accessors(property=path);

    SDAbstractsFetcher          _abstracts          @accessors(property=abstracts);
    SDAPIInfosFetcher           _APIInfos           @accessors(property=APIInfos);
    SDMonolitheConfigsFetcher   _monolitheConfigs   @accessors(property=monolitheConfigs);
    SDSpecificationsFetcher     _specifications     @accessors(property=specifications);
}

+ (id)currentRepository
{
    return NURepositoryCurrent;
}

+ (void)setCurrentRepository:(id)anRepository
{
    NURepositoryCurrent = anRepository;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"repository";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"url"];
        [self exposeLocalKeyPathToREST:@"username"];
        [self exposeLocalKeyPathToREST:@"password"];
        [self exposeLocalKeyPathToREST:@"organization"];
        [self exposeLocalKeyPathToREST:@"repository"];
        [self exposeLocalKeyPathToREST:@"branch"];
        [self exposeLocalKeyPathToREST:@"path"];
        [self exposeLocalKeyPathToREST:@"valid"];

        _APIInfos         = [SDAPIInfosFetcher fetcherWithParentObject:self];
        _specifications   = [SDSpecificationsFetcher fetcherWithParentObject:self];
        _abstracts        = [SDAbstractsFetcher fetcherWithParentObject:self];
        _monolitheConfigs = [SDMonolitheConfigsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
