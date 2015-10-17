@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "Abstracts/SDAbstractAPIsViewController.j"

@implementation SDChildAPIsViewController : SDAbstractAPIsViewController
{
}

+ (CPString)moduleName
{
    return @"Child APIs";
}

+ (id)managedAPIClass
{
    return SDChildAPI
}

+ (CPString)managedAPIName
{
    return @"Child API";
}

+ (CPString)managedAPIsFetcherKeyPath
{
    return @"childAPIs";
}
@end
