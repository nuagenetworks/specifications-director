@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>
@import <RESTCappuccino/NURESTJobsController.j>

@global SDRepositoryStatusToImageTransformerName


@implementation SDRepositoryDataView : NUAbstractDataView
{
    @outlet CPImageView   imageViewStatus;
    @outlet CPTextField   fieldBranch;
    @outlet CPTextField   fieldDescription
    @outlet CPTextField   fieldName;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    var statusTransformer = @{CPValueTransformerNameBindingOption: SDRepositoryStatusToImageTransformerName};

    [fieldBranch bind:CPValueBinding toObject:_objectValue withKeyPath:@"branch" options:nil];
    [fieldDescription bind:CPValueBinding toObject:_objectValue withKeyPath:@"description" options:nil];
    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"name" options:nil];
    [imageViewStatus bind:CPValueBinding toObject:_objectValue withKeyPath:@"status" options:statusTransformer];
}

#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldBranch      = [aCoder decodeObjectForKey:@"fieldBranch"];
        fieldDescription = [aCoder decodeObjectForKey:@"fieldDescription"];
        fieldName        = [aCoder decodeObjectForKey:@"fieldName"];
        imageViewStatus  = [aCoder decodeObjectForKey:@"imageViewStatus"];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldBranch forKey:@"fieldBranch"];
    [aCoder encodeObject:fieldDescription forKey:@"fieldDescription"];
    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:imageViewStatus forKey:@"imageViewStatus"];
}

@end
