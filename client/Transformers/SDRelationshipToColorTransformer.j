@import <Foundation/Foundation.j>

@global SDAPIRelationshipChild
@global SDAPIRelationshipMember


@implementation SDRelationshipToColorTransformer: CPValueTransformer

+ (Class)transformedValueClass
{
    return CPString;
}

+ (BOOL)allowsReverseTransformation
{
    return NO;
}

- (id)transformedValue:(id)value
{
    switch (value)
    {
        case SDAPIRelationshipChild:
            return [CPColor colorWithHexString:@"9acd99"];

        case SDAPIRelationshipMember:
            return [CPColor colorWithHexString:@"659aff"];
    }

    [CPException raise:CPInvalidArgumentException reason:[self class] + @" unexpected value to transform :" + value];
}

@end


// registration
SDRelationshipToColorTransformerName = @"SDRelationshipToColorTransformerName";
[CPValueTransformer setValueTransformer:[SDRelationshipToColorTransformer new] forName:SDRelationshipToColorTransformerName];
