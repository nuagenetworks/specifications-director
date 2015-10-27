@import <Foundation/Foundation.j>
@import "Abstracts/SDRESTObject.j"

@class SDAPIInfosFetcher
@class SDSpecificationsFetcher
@class SDAbstractsFetcher

NURepositoryCurrent = nil;

@implementation SDRepository : SDRESTObject
{
    BOOL                        _valid          @accessors(property=valid);
    CPString                    _name           @accessors(property=name);
    CPString                    _url            @accessors(property=url);
    CPString                    _username       @accessors(property=username);
    CPString                    _password       @accessors(property=password)
    CPString                    _organization   @accessors(property=organization);
    CPString                    _repository     @accessors(property=repository);
    CPString                    _branch         @accessors(property=branch);
    CPString                    _path           @accessors(property=path);

    SDAbstractsFetcher          _abstracts      @accessors(property=abstracts);
    SDAPIInfosFetcher           _APIInfos       @accessors(property=APIInfos);
    SDSpecificationsFetcher     _specifications @accessors(property=specifications);
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

        _APIInfos = [SDAPIInfosFetcher fetcherWithParentObject:self];
        _specifications = [SDSpecificationsFetcher fetcherWithParentObject:self];
        _abstracts = [SDAbstractsFetcher fetcherWithParentObject:self];

        _name = @"test repo"
        _url = @"https://api.github.com"
        _username = @"primalmotion"
        _password = @"2b5da4574ed82d64435db1cbb269e775f1f4a7f8"
        _organization = "nuagenetworks"
        _repository = "monolithe"
        _branch = "specv2"
        _path = "/examples/specifications"
    }

    return self;
}

@end
