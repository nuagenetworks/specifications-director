@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "Abstracts/SDAbstractAPIsViewController.j"

@implementation SDParentAPIsViewController : SDAbstractAPIsViewController
{
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Parent APIs";
}

+ (id)managedAPIClass
{
    return SDParentAPI
}

+ (CPString)managedAPIName
{
    return @"Parent API";
}

+ (CPString)managedAPIsFetcherKeyPath
{
    return @"parentAPIs";
}

@end