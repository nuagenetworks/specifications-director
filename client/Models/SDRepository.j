@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@class SDAbstractsFetcher
@class SDAPIInfosFetcher
@class SDMonolitheConfigsFetcher
@class SDSpecificationsFetcher

NURepositoryCurrent = nil;

SDRepositoryStatusREADY = @"READY";
SDRepositoryStatusPULLING = @"PULLING";
SDRepositoryStatusNEEDS_PULL = @"NEEDS_PULL";
SDRepositoryStatusERROR = @"ERROR";
SDRepositoryStatusQUEUED = @"QUEUED";


@implementation SDRepository : SDRESTObject
{
    BOOL                        _pushPermission     @accessors(property=pushPermission);
    CPString                    _associatedTokenID  @accessors(property=associatedTokenID);
    CPString                    _branch             @accessors(property=branch);
    CPString                    _name               @accessors(property=name);
    CPString                    _organization       @accessors(property=organization);
    CPString                    _password           @accessors(property=password)
    CPString                    _path               @accessors(property=path);
    CPString                    _repository         @accessors(property=repository);
    CPString                    _status             @accessors(property=status);
    CPString                    _url                @accessors(property=url);
    CPString                    _username           @accessors(property=username);

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
        [self exposeLocalKeyPathToREST:@"associatedTokenID"];
        [self exposeLocalKeyPathToREST:@"branch"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"organization"];
        [self exposeLocalKeyPathToREST:@"password"];
        [self exposeLocalKeyPathToREST:@"path"];
        [self exposeLocalKeyPathToREST:@"pushPermission"];
        [self exposeLocalKeyPathToREST:@"repository"];
        [self exposeLocalKeyPathToREST:@"status"];
        [self exposeLocalKeyPathToREST:@"url"];
        [self exposeLocalKeyPathToREST:@"username"];

        _organization = [[SDAuth defaultUser] userName];
        _url          = @"https://github.mv.usa.alcatel.com/api/v3";
        _repository   = @"api-specifications";
        _status       = SDRepositoryStatusNEEDS_PULL;
        _branch       = @"master";
        _path         = @"/";

        _APIInfos         = [SDAPIInfosFetcher fetcherWithParentObject:self];
        _specifications   = [SDSpecificationsFetcher fetcherWithParentObject:self];
        _abstracts        = [SDAbstractsFetcher fetcherWithParentObject:self];
        _monolitheConfigs = [SDMonolitheConfigsFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setOrganization:(CPString)anOrganization
{
    if (_organization == anOrganization)
        return;

    [self willChangeValueForKey:@"organization"];
    [self willChangeValueForKey:@"description"];
    _organization = anOrganization
    [self didChangeValueForKey:@"organization"];
    [self didChangeValueForKey:@"description"];
}

- (void)setRepository:(CPString)aRepository
{
    if (_repository == aRepository)
        return;

    [self willChangeValueForKey:@"repository"];
    [self willChangeValueForKey:@"description"];
    _repository = aRepository
    [self didChangeValueForKey:@"repository"];
    [self didChangeValueForKey:@"description"];
}

- (CPString)description
{
    return _organization + @"/" + _repository
}

@end
