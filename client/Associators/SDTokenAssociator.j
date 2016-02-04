@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractSimpleObjectAssociator.j>

@implementation SDTokenAssociator : NUAbstractSimpleObjectAssociator

- (CPArray)currentActiveContextIdentifiers
{
    return [[SDToken RESTName]];
}

- (CPDictionary)associatorSettings
{
    return @{
                [SDToken RESTName]: @{
                    NUObjectAssociatorSettingsDataViewNameKey: @"tokenDataView",
                    NUObjectAssociatorSettingsAssociatedObjectFetcherKeyPathKey: @"tokens"
                }
            };
}

- (CPString)emptyAssociatorTitle
{
    return @"Select a Token";
}

- (CPString)titleForObjectChooser
{
    return @"Select a Token";
}

- (CPString)keyPathForAssociatedObjectID
{
    return @"associatedTokenID";
}

- (NUVSDObject)parentOfAssociatedObjects
{
    return [SDAuth defaultUser];
}

@end
