/*
*   Filename:         NUNetworkMacroGroupsViewController.j
*   Created:          Tue May  5 13:37:12 PDT 2015
*   Author:           Christophe Serafin <christophe.serafin@alcatel-lucent.com>
*   Description:      VSA
*   Project:          Cloud Network Automation - Nuage - Data Center Service Delivery - IPD
*
* Copyright (c) 2011-2012 Alcatel, Alcatel-Lucent, Inc. All Rights Reserved.
*
* This source code contains confidential information which is proprietary to Alcatel.
* No part of its contents may be used, copied, disclosed or conveyed to any party
* in any manner whatsoever without prior written permission from Alcatel.
*
* Alcatel-Lucent is a trademark of Alcatel-Lucent, Inc.
*
*/

@import <Foundation/Foundation.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDModelViewController
@class SDAttributesViewController
@class SDAPIsViewController

@implementation SDSpecificationsViewController : NUModule
{
    @outlet SDModelViewController       modelController;
    @outlet SDAttributesViewController  attributesController;
    @outlet SDAPIsViewController        APIsController;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Specifications";
}

+ (CPImage)moduleIcon
{
    return [SDSpecification icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"specificationDataView" forClass:SDSpecification];
    [self setModuleTitle:@"Specifications"];

    [self setSubModules:[modelController, attributesController, APIsController]]
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Specification" identifier:[SDSpecification RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"specifications"];
    [self registerContext:context forClass:SDSpecification];
}

@end
