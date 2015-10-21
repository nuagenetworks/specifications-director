@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>
@import <RESTCappuccino/NURESTJobsController.j>

@global NURESTJobsControllerJobCompletedNotification

@implementation SDRepositoryDataView : NUAbstractDataView
{
    @outlet CPButton      buttonPull;
    @outlet CPButton      buttonCommit;
    @outlet CPTextField   fieldName;
    @outlet CPTextField   fieldOrganization;
    @outlet CPTextField   fieldRepository;
    @outlet CPTextField   fieldURL;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"name" options:nil];
    [fieldURL bind:CPValueBinding toObject:_objectValue withKeyPath:@"url" options:nil];
    [fieldOrganization bind:CPValueBinding toObject:_objectValue withKeyPath:@"organization" options:nil];
    [fieldRepository bind:CPValueBinding toObject:_objectValue withKeyPath:@"repository" options:nil];
}


#pragma mark -
#pragma mark Actions

- (@action)pull:(id)aSender
{
    [[NURESTJobsController defaultController] postJob:[SDPullJob new] toEntity:_objectValue andCallSelector:@selector(_didPull:) ofObject:self];
}

- (void)_didPull:(NURESTJob)aJob
{

}

- (@action)commit:(id)aSender
{
    [[NURESTJobsController defaultController] postJob:[SDCommitJob new] toEntity:_objectValue andCallSelector:@selector(_didCommit:) ofObject:self];
}

- (void)_didCommit:(NURESTJob)aJob
{

}

#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        buttonCommit      = [aCoder decodeObjectForKey:@"buttonCommit"];
        buttonPull        = [aCoder decodeObjectForKey:@"buttonPull"];
        fieldName         = [aCoder decodeObjectForKey:@"fieldName"];
        fieldOrganization = [aCoder decodeObjectForKey:@"fieldOrganization"];
        fieldRepository   = [aCoder decodeObjectForKey:@"fieldRepository"];
        fieldURL          = [aCoder decodeObjectForKey:@"fieldURL"];

    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:buttonCommit forKey:@"buttonCommit"];
    [aCoder encodeObject:buttonPull forKey:@"buttonPull"];
    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:fieldOrganization forKey:@"fieldOrganization"];
    [aCoder encodeObject:fieldRepository forKey:@"fieldRepository"];
    [aCoder encodeObject:fieldURL forKey:@"fieldURL"];
}

@end
