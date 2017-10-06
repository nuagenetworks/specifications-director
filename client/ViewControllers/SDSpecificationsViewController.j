/*
* Copyright (c) 2016, Alcatel-Lucent Inc
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the copyright holder nor the names of its contributors
*       may be used to endorse or promote products derived from this software without
*       specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

    [[self view] setBorderLeftColor:NUSkinColorGreyLight];
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
    if (anAttribute == @"objectRESTName" && [anObject objectRESTName])
    {
        [anObject setObjectResourceName:NURESTObjectPluralize([anObject objectRESTName])];
        [anObject setEntityName:[[anObject objectRESTName] capitalizedString]];
    }

    _validate(validation, anAttribute, anObject, @"description", [[_stringNotEmpty]]);    
    _validate(validation, anAttribute, anObject, @"entityName", [[_stringNotEmpty]]);    
    _validate(validation, anAttribute, anObject, @"objectResourceName", [[_stringNotEmpty]]);    
    _validate(validation, anAttribute, anObject, @"objectRESTName", [[_stringNotEmpty]]);    
    _validate(validation, anAttribute, anObject, @"userlabel", [[_stringNotEmpty],[_maxLength, 50]]);
}

@end
