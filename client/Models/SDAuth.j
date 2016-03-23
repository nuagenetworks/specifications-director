@import <Foundation/Foundation.j>
@import <Bambou/NURESTAbstractUser.j>

@class SDRepositoriesFetcher
@class SDTokensFetcher


@implementation SDAuth : NURESTAbstractUser
{
    SDRepositoriesFetcher   _repositories   @accessors(property=repositories);
    SDTokensFetcher         _tokens         @accessors(property=tokens);
}


#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"auth";
}

- (id)init
{
    if (self = [super init])
    {
        _repositories = [SDRepositoriesFetcher fetcherWithParentObject:self];
        _tokens = [SDTokensFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setRole:(CPString)aRole
{
    _role = @"NURESTUserRoleCSPRoot";
}

- (void)displayDescription
{
    return _userName;
}

@end
