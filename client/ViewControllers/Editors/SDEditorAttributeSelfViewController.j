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
@import <NUKit/NUModuleSelfParent.j>
@import "../../Models/SDModels.j"

@global SDAttributeDefaultBoolean
@global SDAttributeSubtypeLong
@global SDAttributeTypeBoolean
@global SDAttributeTypeFloat
@global SDAttributeTypeInteger
@global SDAttributeTypeList
@global SDAttributeTypeObject

@implementation SDEditorAttributeSelfViewController : NUModuleSelfParent
{
    @outlet CPPopUpButton   buttonSubtype;
    @outlet CPTableView     tableViewEnumarationValues;
    @outlet CPView          viewEditorEnumConfig;
    @outlet CPView          viewEditorEnumFlags;
    @outlet CPView          viewEditorNumberConfig;
    @outlet CPView          viewEditorStringConfig;
    @outlet CPView          viewEditorSubtype;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attribute";
}

+ (CPString)moduleTabIconIdentifier
{
    return @"self";
}

- (void)viewDidLoad
{
    var textField = [[tableViewEnumarationValues tableColumns][0] dataView];
    [textField setPlaceholderString:@"Double click to enter the value"];
    [[tableViewEnumarationValues tableColumns][0] setDataView:nil];
    [[tableViewEnumarationValues tableColumns][0] setDataView:textField];

    [super viewDidLoad];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Attribute" identifier:[SDAttribute RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setSearchForTagsRecursively:YES];
    [context setAdditionalEditionViews:[viewEditionMain, viewEditorStringConfig, viewEditorNumberConfig, viewEditorEnumConfig, viewEditorEnumFlags, viewEditorSubtype]];
    [self registerContext:context forClass:SDAttribute];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleUpdateEditorInterface
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanEdit               = conditionRepoHasPushPermission;
        
    [_currentContext setBoundControlsEnabled:conditionCanEdit];
    [self _updateSubtypeAllowedValues];
}


#pragma mark -
#pragma mark NUModuleSelfParent API

- (CPArray)moduleCurrentVisibleEditionViews
{
    var editionViews                = [viewEditionMain],
        editedObject                = [_currentContext editedObject],
        type                        = [editedObject type],
        conditionSubtypeApplicable  = type == SDAttributeTypeList || type == SDAttributeTypeInteger || type == SDAttributeTypeFloat || type == SDAttributeTypeObject;

    if (conditionSubtypeApplicable)
        [editionViews addObject:viewEditorSubtype];
        
    switch ([editedObject type])
    {
        case SDAttributeTypeInteger:
        case SDAttributeTypeFloat:
            [editionViews addObject:viewEditorNumberConfig];
            break;

        case SDAttributeTypeString:
            [editionViews addObject:viewEditorStringConfig];
            break;
    }

    if ([editedObject type] == SDAttributeTypeEnum || [editedObject subtype] == SDAttributeTypeEnum)
        [editionViews addObject:viewEditorEnumConfig];

    [editionViews addObject:viewEditorEnumFlags];
        
    return editionViews;
}

#pragma mark -
#pragma mark Action

- (IBAction)changeType:(id)aSender
{
    var editedObject = [_currentContext editedObject];
    
    if ([editedObject type] == SDAttributeTypeBoolean && ![editedObject defaultValue])
        [editedObject setDefaultValue:SDAttributeDefaultBoolean];

    [editedObject setSubtype:nil];
    [self _updateSubtypeAllowedValues];
    [self reloadStackView];
}

- (IBAction)changeSubtype:(id)aSender
{
    [self reloadStackView];
}

#pragma mark -
#pragma mark Delegates

- (void)moduleContext:(NUModuleContext)aContext validateObject:(NUVSDObject)anObject attribute:(CPString)anAttribute validation:(NUValidation)aValidation
{
    _validate(aValidation, anAttribute, anObject, @"userlabel", [[_maxLength, 50]]);
}


#pragma mark -
#pragma mark Utilities

- (void)_updateSubtypeAllowedValues
{
    var editedObject    = [_currentContext editedObject],
        type            = [editedObject type],
        allowedSubTypes = [[CPArrayController alloc] init],
        conditionObject = type == SDAttributeTypeObject;

    if (type == SDAttributeTypeInteger) {
        [allowedSubTypes insertObject:@{"value":  SDAttributeTypeInteger, "label": "Integer"} atArrangedObjectIndex:0];
        [allowedSubTypes insertObject:@{"value":  SDAttributeSubtypeLong, "label": "Long"} atArrangedObjectIndex:1];
    }
    else if (type == SDAttributeTypeFloat)
        [allowedSubTypes insertObject:@{"value":  SDAttributeSubtypeDouble, "label": "Double"} atArrangedObjectIndex:0];
    else if (type == SDAttributeTypeList || type == SDAttributeTypeObject) 
    {
        var apiFetcher = [[[editedObject parentObject] parentObject] specifications];
        [apiFetcher fetchAndCallSelector:@selector(_fetcher:ofObject:didFetchAPIs:) ofObject:self];
        return;
    }
    
    [buttonSubtype unbind:CPContentBinding];
    [buttonSubtype unbind:CPContentValuesBinding];
    [buttonSubtype unbind:CPSelectedObjectBinding];
    [buttonSubtype removeAllItems];
    [buttonSubtype bind:CPContentBinding toObject:allowedSubTypes withKeyPath:@"arrangedObjects.value" options:nil];
    [buttonSubtype bind:CPContentValuesBinding toObject:allowedSubTypes withKeyPath:@"arrangedObjects.label" options:nil];
    [buttonSubtype bind:CPSelectedObjectBinding toObject:editedObject withKeyPath:@"subtype" options:nil];
}

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
