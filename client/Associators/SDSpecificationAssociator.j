@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractSimpleObjectAssociator.j>

@implementation SDSpecificationAssociator : NUAbstractSimpleObjectAssociator

- (CPArray)currentActiveContextIdentifiers
{
    return [[SDSpecification RESTName]];
}

- (CPDictionary)associatorSettings
{
    return @{
                [SDSpecification RESTName]: @{
                    NUObjectAssociatorSettingsDataViewNameKey: @"specificationDataView",
                    NUObjectAssociatorSettingsAssociatedObjectFetcherKeyPathKey: @"specifications"
                }
            };
}

- (CPString)emptyAssociatorTitle
{
    return @"Select a Specification";
}

- (CPString)titleForObjectChooser
{
    return @"Select a Specification";
}

- (CPString)keyPathForAssociatedObjectID
{
    return @"associatedSpecificationID";
}

- (NUVSDObject)parentOfAssociatedObjects
{
    return [SDRepository currentRepository];
}

@end
