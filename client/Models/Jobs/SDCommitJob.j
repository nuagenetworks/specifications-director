@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTJob.j>


@implementation SDCommitJob : NURESTJob

#pragma mark -
#pragma mark Initialization

- (id)init
{
    if (self = [super init])
    {
        _command = @"commit";
    }

    return self;
}

@end
