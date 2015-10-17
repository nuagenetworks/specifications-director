@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>


@implementation SDSpecificationDataView : NUAbstractDataView
{
    @outlet CPTextField   fieldName;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"name" options:nil];
}


#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldName = [aCoder decodeObjectForKey:@"fieldName"];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldName forKey:@"fieldName"];
}

@end
