@import <Foundation/Foundation.j>

@global SDAttributeTypeBoolean
@global SDAttributeTypeEnum
@global SDAttributeTypeFloat
@global SDAttributeTypeInteger
@global SDAttributeTypeList
@global SDAttributeTypeObject
@global SDAttributeTypeString
@global SDAttributeTypeTime


@implementation SDTypeToColorTransformer: CPValueTransformer

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
        case SDAttributeTypeBoolean:
            return [CPColor colorWithHexString:@"9acd99"];

        case SDAttributeTypeEnum:
            return [CPColor colorWithHexString:@"659aff"];

        case SDAttributeTypeFloat:
            return [CPColor colorWithHexString:@"8c49a0"];

        case SDAttributeTypeInteger:
            return [CPColor colorWithHexString:@"ffd07a"];

        case SDAttributeTypeList:
            return [CPColor colorWithHexString:@"c4c4e6"];

        case SDAttributeTypeObject:
            return [CPColor colorWithHexString:@"cccd9a"];

        case SDAttributeTypeString:
            return [CPColor colorWithHexString:@"ff9a00"];

        case SDAttributeTypeTime:
            return [CPColor colorWithHexString:@"009acc"];
    }

    return [CPColor redColor];
}

@end


// registration
SDTypeToColorTransformerName = @"SDTypeToColorTransformerName";
[CPValueTransformer setValueTransformer:[SDTypeToColorTransformer new] forName:SDTypeToColorTransformerName];
