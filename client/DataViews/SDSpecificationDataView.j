@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>


@implementation SDSpecificationDataView : NUAbstractDataView
{
    @outlet CPTextField fieldName;
    @outlet CPImageView imageViewWarning;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"name" options:nil];

    [imageViewWarning setHidden:!!![_objectValue issues]];

    if ([_objectValue issues])
        [imageViewWarning setToolTip:@"Some errors has been found during the parsing of the remote specification. Please review"];
}


#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldName        = [aCoder decodeObjectForKey:@"fieldName"];
        imageViewWarning = [aCoder decodeObjectForKey:@"imageViewWarning"];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:imageViewWarning forKey:@"imageViewWarning"];
}

@end
