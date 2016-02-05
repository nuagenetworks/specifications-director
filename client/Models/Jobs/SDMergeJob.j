@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTJob.j>


@implementation SDMergeJob : NURESTJob

#pragma mark -
#pragma mark Initialization

- (id)init
{
    if (self = [super init])
    {
        _command = @"merge_master";
    }

    return self;
}

@end
