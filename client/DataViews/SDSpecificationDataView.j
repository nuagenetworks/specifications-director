@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataView.j>


@implementation SDSpecificationDataView : NUAbstractDataView
{
    @outlet CPImageView imageViewEdited;
    @outlet CPImageView imageViewWarning;
    @outlet CPTextField fieldName;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    var negateBoolTransformer = @{CPValueTransformerNameBindingOption: CPNegateBooleanTransformerName};

    [fieldName bind:CPValueBinding toObject:_objectValue withKeyPath:@"displayName" options:nil];

    [imageViewWarning setHidden:!!![_objectValue issues]];
    [imageViewEdited bind:CPHiddenBinding toObject:_objectValue withKeyPath:@"syncing" options:negateBoolTransformer];

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
        imageViewEdited  = [aCoder decodeObjectForKey:@"imageViewEdited"];
        imageViewWarning = [aCoder decodeObjectForKey:@"imageViewWarning"];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:imageViewEdited forKey:@"imageViewEdited"];
    [aCoder encodeObject:imageViewWarning forKey:@"imageViewWarning"];
}

@end
