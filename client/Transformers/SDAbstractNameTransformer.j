@import <Foundation/Foundation.j>


@implementation SDAbstractNameTransformer: CPValueTransformer

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
    console.error(value)
    return value.replace(/^@/, @"").replace(/\.spec$/, @"");
}

@end


// registration
SDAbstractNameTransformerName = @"SDAbstractNameTransformerName";
[CPValueTransformer setValueTransformer:[SDAbstractNameTransformer new] forName:SDAbstractNameTransformerName];
