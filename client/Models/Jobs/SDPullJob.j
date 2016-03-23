@import <Foundation/Foundation.j>
@import <Bambou/NURESTJob.j>


@implementation SDPullJob : NURESTJob

#pragma mark -
#pragma mark Initialization

- (id)init
{
    if (self = [super init])
    {
        _command = @"pull";
    }

    return self;
}

@end
