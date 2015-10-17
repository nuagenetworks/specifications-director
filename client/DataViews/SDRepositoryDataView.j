@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>


@implementation SDRepositoryDataView : NUAbstractDataView
{
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
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
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

    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:fieldOrganization forKey:@"fieldOrganization"];
    [aCoder encodeObject:fieldRepository forKey:@"fieldRepository"];
    [aCoder encodeObject:fieldURL forKey:@"fieldURL"];
}

@end
