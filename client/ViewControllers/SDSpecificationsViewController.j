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
@import <AppKit/CPVisualEffectView.j>
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@class SDModelViewController
@class SDAttributesViewController
@class SDAPIsViewController

@global NURESTObjectPluralize


@implementation SDSpecificationsViewController : NUModule
{
    @outlet SDModelViewController       modelController;
    @outlet SDAttributesViewController  attributesController;
    @outlet SDAPIsViewController        APIsController;

    @outlet CPCheckBox                  checkBoxRootAPI;
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

    [self setSubModules:[modelController, attributesController, APIsController]];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Specification" identifier:[SDSpecification RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"specifications"];
    [self registerContext:context forClass:SDSpecification];
}

- (void)performPostPushOperation
{
    [self disableCheckBoxRootAPIIfNeeded];
}

- (CPSet)permittedActionsForObject:(id)anObject
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanAdd                = conditionRepoHasPushPermission,
        conditionCanEdit               = anObject && conditionRepoHasPushPermission,
        permittedActionsSet            = [CPSet new];

    if (conditionCanAdd)
        [permittedActionsSet addObject:NUModuleActionAdd];

    if (conditionCanEdit)
    {
        [permittedActionsSet addObject:NUModuleActionEdit];
        [permittedActionsSet addObject:NUModuleActionDelete];
    }

    return permittedActionsSet;
}

#pragma mark -
#pragma mark Utilities

- (void)disableCheckBoxRootAPIIfNeeded
{
    var editedObject = [_currentContext editedObject]

    if (!editedObject)
        return;

    [checkBoxRootAPI setEnabled:![editedObject root]];
}

#pragma mark -
#pragma mark NUModuleContext delegates

- (void)moduleContext:(NUModuleContext)aContext willManageObject:(NUVSDObject)anObject
{
    [self disableCheckBoxRootAPIIfNeeded];
}

- (void)moduleContext:(NUModuleContext)aContext validateObject:(id)anObject attribute:(CPString)anAttribute validation:(NUValidation)validation
{
    if (anAttribute != @"objectRESTName")
        return

    if ([anObject objectRESTName])
    {
        [anObject setObjectResourceName:NURESTObjectPluralize([anObject objectRESTName])];
        [anObject setEntityName:[[anObject objectRESTName] capitalizedString]];
    }
}

@end
