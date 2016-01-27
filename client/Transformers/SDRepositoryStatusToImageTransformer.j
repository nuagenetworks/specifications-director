@import <Foundation/Foundation.j>

@global SDRepositoryStatusREADY;
@global SDRepositoryStatusPULLING;
@global SDRepositoryStatusNEEDS_PULL;
@global SDRepositoryStatusERROR;
@global SDRepositoryStatusQUEUED;


@implementation SDRepositoryStatusToImageTransformer: CPValueTransformer

+ (Class)transformedValueClass
{
    return CPImage;
}

+ (BOOL)allowsReverseTransformation
{
    return NO;
}

- (id)transformedValue:(id)value
{
    switch (value)
    {
        case SDRepositoryStatusREADY:
            return CPImageInBundle('repo-status-ready.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusPULLING:
            return CPImageInBundle('repo-status-pulling.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusNEEDS_PULL:
            return CPImageInBundle('repo-status-needspull.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusERROR:
            return CPImageInBundle('repo-status-error.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusQUEUED:
            return CPImageInBundle('repo-status-queued.png', CGSizeMake(16.0, 16.0));
    }
}

@end


// registration
SDRepositoryStatusToImageTransformerName = @"SDRepositoryStatusToImageTransformerName";
[CPValueTransformer setValueTransformer:[SDRepositoryStatusToImageTransformer new] forName:SDRepositoryStatusToImageTransformerName];
