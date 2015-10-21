@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTJob.j>


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
