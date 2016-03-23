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

@class SDSpecificationAssociator


@implementation SDAPIsViewController : NUModule
{
    @outlet CPCheckBox                  checkBoxAllowsBulkCreate;
    @outlet CPCheckBox                  checkBoxAllowsBulkDelete;
    @outlet CPCheckBox                  checkBoxAllowsBulkUpdate;
    @outlet CPCheckBox                  checkBoxAllowsCreate;
    @outlet CPCheckBox                  checkBoxAllowsUpdate;
    @outlet CPPopUpButton               buttonRelationship;
    @outlet CPTextField                 labelRelationship;
    @outlet SDSpecificationAssociator   specificationAssociator;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"APIs";
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self registerDataViewWithName:@"APIDataView" forClass:SDChildAPI];

    [specificationAssociator setDelegate:self];
    [specificationAssociator setDisassociationButtonHidden:YES];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Children API" identifier:[SDChildAPI RESTName]];
    [context setFetcherKeyPath:@"childAPIs"];
    [context setPopover:popover];
    [self registerContext:context forClass:SDChildAPI];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleWillHide
{
    [super moduleWillHide];
    [specificationAssociator setCurrentParent:nil];
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
#pragma mark Actions

- (@action)relationshipChanged:(id)aSender
{
    var editedObject = [_currentContext editedObject];

    if ([_currentParent root])
    {
        [popover setContentSize:CGSizeMake(320, 313)];
        [buttonRelationship setHidden:YES];
        [labelRelationship setHidden:YES];
        [checkBoxAllowsUpdate setHidden:YES];
        [checkBoxAllowsCreate setHidden:NO];
        [checkBoxAllowsBulkUpdate setHidden:NO];
        [checkBoxAllowsBulkCreate setHidden:NO];
        [checkBoxAllowsBulkDelete setHidden:NO];

        [editedObject setAllowsGet:YES];
        [editedObject setAllowsCreate:YES];
        [editedObject setAllowsUpdate:NO];

        [editedObject setRelationship:SDAPIRelationshipRoot];
        return;
    }

    switch ([editedObject relationship])
    {
        case SDAPIRelationshipChild:
        case SDAPIRelationshipAlias:
            [popover setContentSize:CGSizeMake(320, 368)];
            [buttonRelationship setHidden:NO];
            [labelRelationship setHidden:NO];
            [checkBoxAllowsUpdate setHidden:YES];
            [checkBoxAllowsCreate setHidden:NO];
            [checkBoxAllowsBulkUpdate setHidden:NO];
            [checkBoxAllowsBulkCreate setHidden:NO];
            [checkBoxAllowsBulkDelete setHidden:NO];

            [editedObject setAllowsGet:YES];
            [editedObject setAllowsCreate:YES];
            [editedObject setAllowsUpdate:NO];

            break;

        case SDAPIRelationshipMember:
            [popover setContentSize:CGSizeMake(320, 368)];
            [buttonRelationship setHidden:NO];
            [labelRelationship setHidden:NO];
            [checkBoxAllowsUpdate setHidden:NO];
            [checkBoxAllowsCreate setHidden:YES];
            [checkBoxAllowsBulkUpdate setHidden:YES];
            [checkBoxAllowsBulkCreate setHidden:YES];
            [checkBoxAllowsBulkDelete setHidden:YES];

            [editedObject setAllowsGet:YES];
            [editedObject setAllowsCreate:NO];
            [editedObject setAllowsUpdate:YES];

            [editedObject setAllowsBulkCreate:NO];
            [editedObject setAllowsBulkUpdate:NO];
            [editedObject setAllowsBulkDelete:NO];

            break;
    }
}


#pragma mark -
#pragma mark NUModuleContext Delegate

- (void)moduleContext:(NUModuleContext)aContext willManageObject:(NUVSDObject)anObject
{
    [self relationshipChanged:self];
    [specificationAssociator setCurrentParent:anObject];
}

@end
