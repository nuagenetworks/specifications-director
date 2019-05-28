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
@import <NUKit/NUModule.j>
@import "../Models/SDModels.j"

@global SDAttributeTypeBoolean
@global SDAttributeDefaultBoolean
@global SDAttributeTypeObject
@global SDAttributeTypeList

@class SDEditorAttributesViewController

@implementation SDAttributesViewController : NUModule
{
    @outlet SDEditorAttributesViewController    editorAttributesController;
    @outlet CPPopUpButton                       buttonSubtype;
    @outlet CPView                              viewSubtype;
    
    CGSize                                      _originalPopoverSize;
    CGSize                                      _noSubtypePopoverSize;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attributes";
}

+ (CPImage)moduleIcon
{
    return [SDAttribute icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"attributeDataView" forClass:SDAttribute];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Attribute" identifier:[SDAttribute RESTName]];
    [context setPopover:popover];
    [context setFetcherKeyPath:@"attributes"];
    [self registerContext:context forClass:SDAttribute];
    [context setAdditionalEditionViews:[viewSubtype]];
    
    _originalPopoverSize = [popover contentSize];
    _noSubtypePopoverSize = CGSizeMakeCopy(_originalPopoverSize);
    _noSubtypePopoverSize.height = _noSubtypePopoverSize.height - [viewSubtype frameSize].height - 10;
}

- (void)configureEditor:(NUEditorsViewController)anEditorController
{
    [anEditorController registerEditor:editorAttributesController forObjectsWithRESTName:[SDAttribute RESTName]];
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
#pragma mark NUModuleContext Delegates

- (void)moduleContext:(NUModuleContext)aContext willManageObject:(NUVSDObject)anObject
{
    [self handleType:self];
}

- (void)moduleContext:(NUModuleContext)aContext validateObject:(NUVSDObject)anObject attribute:(CPString)anAttribute validation:(NUValidation)aValidation
{
    var type                       = [anObject type],
        conditionSubtypeApplicable = type == SDAttributeTypeObject || type == SDAttributeTypeList;
        
    if (conditionSubtypeApplicable) 
        _validate(aValidation, anAttribute, anObject, @"subtype", [[_stringNotEmpty]]);
    else
        [aValidation removeErrorForProperty:@"subtype"];
        
    _validate(aValidation, anAttribute, anObject, @"name", [[_stringNotEmpty], [_maxLength, 255]]);
    _validate(aValidation, anAttribute, anObject, @"description", [[_stringNotEmpty], [_maxLength, 255]]);    
}

- (void)moduleContext:(NUModuleContext)aContext willSaveObject:(NUVSDObject)anObject
{
    if ([anObject type] == SDAttributeTypeBoolean)
        [anObject setDefaultValue:SDAttributeDefaultBoolean];
        
    if (![anObject ID])
    {
        if (![anObject userlabel])
        {
            var defaultLabel = [anObject name].replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); });
        
            [anObject setUserlabel:defaultLabel.trim().substring(0, 50)];
        }

        if ([anObject type] == SDAttributeTypeString)
        {
            if (![anObject minLength])
                [anObject setMinLength:0];

            if (![anObject maxLength])
                [anObject setMaxLength:255];
        }
        else if ([anObject type] == SDAttributeTypeInteger)
        {
            if (![anObject minValue])
                [anObject setMinValue:0];

            if (![anObject maxValue])
                [anObject setMaxValue:2147483647];
        }
    }
}


#pragma mark -
#pragma mark Actions

- (@action)handleType:(id)aSender
{
    var editedObject               = [_currentContext editedObject],
        type                       = [editedObject type],
        conditionSubtypeApplicable = type == SDAttributeTypeObject || type == SDAttributeTypeList;

    [viewSubtype setHidden: !conditionSubtypeApplicable];
    [popover setContentSize:conditionSubtypeApplicable ? _originalPopoverSize : _noSubtypePopoverSize];
    if (conditionSubtypeApplicable)
    {
        var apiFetcher = [[[_currentContext parentObject] parentObject] specifications];
        
        [apiFetcher fetchAndCallSelector:@selector(_fetcher:ofObject:didFetchAPIs:) ofObject:self];
    } else {
        [editedObject setSubtype: null];
    }
}


#pragma mark -
#pragma mark Utilities

- (void)_fetcher:(NURESTFetcher)aFetcher ofObject:(SDRESTObject)anObject didFetchAPIs:(CPArray)someAPIs
{
    var editedObject    = [_currentContext editedObject],
        conditionList   = [editedObject type] == SDAttributeTypeList,
        allowedSubtypes = [[CPArrayController alloc] init];
    
    if (conditionList) 
    {
        [allowedSubtypes insertObject:@{"entityName": SDAttributeSubtypeDouble} atArrangedObjectIndex:0];
        [allowedSubtypes insertObject:@{"entityName": SDAttributeTypeEnum} atArrangedObjectIndex:1];
        [allowedSubtypes insertObject:@{"entityName": SDAttributeSubtypeLong} atArrangedObjectIndex:2];
        [allowedSubtypes insertObject:@{"entityName": SDAttributeTypeString} atArrangedObjectIndex:3];
    }
    
    if ([someAPIs count])
        [allowedSubtypes addObjects: someAPIs];    
        
    if ([[allowedSubtypes arrangedObjects] count])
    {           
        [buttonSubtype unbind:CPContentBinding];
        [buttonSubtype unbind:CPContentValuesBinding];
        [buttonSubtype unbind:CPSelectedObjectBinding];
        [buttonSubtype removeAllItems];
        [buttonSubtype bind:CPContentBinding toObject:allowedSubtypes withKeyPath:@"arrangedObjects.entityName" options:nil];
        [buttonSubtype bind:CPContentValuesBinding toObject:allowedSubtypes withKeyPath:@"arrangedObjects.entityName" options:nil];
        [buttonSubtype bind:CPSelectedObjectBinding toObject:editedObject withKeyPath:@"subtype" options:nil];
    }
}

@end
