@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>

@global SDTypeToColorTransformerName

@implementation SDAttributeDataView : NUAbstractDataView
{
    @outlet CPTextField   fieldDescription;
    @outlet CPTextField   fieldName;
    @outlet CPTextField   fieldType;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    var typeToColorTransformer = @{CPValueTransformerNameBindingOption: SDTypeToColorTransformerName};

    [fieldDescription bind:CPValueBinding toObject:_objectValue withKeyPath:@"description" options:nil];
    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"name" options:nil];
    [fieldType bind:CPValueBinding toObject:_objectValue withKeyPath:@"type" options:nil];
    [fieldType bind:@"backgroundColor" toObject:_objectValue withKeyPath:@"type" options:typeToColorTransformer];
}


#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldDescription = [aCoder decodeObjectForKey:@"fieldDescription"];
        fieldName        = [aCoder decodeObjectForKey:@"fieldName"];
        fieldType        = [aCoder decodeObjectForKey:@"fieldType"];

        [fieldType setTextColor:NUSkinColorWhite];
        [fieldType setBorderRadius:100];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldDescription forKey:@"fieldDescription"];
    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:fieldType forKey:@"fieldType"];
}

@end
