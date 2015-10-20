@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>

@global SDRelationshipToColorTransformerName

@implementation SDAPIDataView : NUAbstractDataView
{
    @outlet CPTextField   fieldOperations;
    @outlet CPTextField   fieldPath;
    @outlet CPTextField   fieldRelationship;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    var relationshipToColorTransformer = @{CPValueTransformerNameBindingOption: SDRelationshipToColorTransformerName};

    [fieldOperations bind:CPValueBinding toObject:_objectValue withKeyPath:@"allowedOperationsString" options:nil];
    [fieldPath bind:CPValueBinding toObject:_objectValue withKeyPath:@"path" options:nil];
    [fieldRelationship bind:@"backgroundColor" toObject:_objectValue withKeyPath:@"relationship" options:relationshipToColorTransformer];
    [fieldRelationship bind:CPValueBinding toObject:_objectValue withKeyPath:@"relationship" options:nil];

    [_objectValue fetchPath];
}


#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldOperations   = [aCoder decodeObjectForKey:@"fieldOperations"];
        fieldPath         = [aCoder decodeObjectForKey:@"fieldPath"];
        fieldRelationship = [aCoder decodeObjectForKey:@"fieldRelationship"];

        [fieldRelationship setTextColor:NUSkinColorWhite];
        [fieldRelationship setBorderRadius:100];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldOperations forKey:@"fieldOperations"];
    [aCoder encodeObject:fieldPath forKey:@"fieldPath"];
    [aCoder encodeObject:fieldRelationship forKey:@"fieldRelationship"];
}

@end
