@import <Foundation/Foundation.j>
@import <NUKit/NUAbstractDataViewsLoader.j>
@import "SDDataViews.j"

@implementation SDDataViewsLoader : NUAbstractDataViewsLoader
{
    @outlet SDAPIDataView           APIDataView             @accessors(readonly);
    @outlet SDAttributeDataView     attributeDataView       @accessors(readonly);
    @outlet SDRepositoryDataView    repositoryDataView      @accessors(readonly);
    @outlet SDSpecificationDataView specificationDataView   @accessors(readonly);
}

@end