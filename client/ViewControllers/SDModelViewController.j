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
@import "../Models/SDModels.j"

@class SDModelAbstractsViewController

@global NURESTObjectPluralize


@implementation SDModelViewController : NUModuleSelfParent
{
    @outlet CPView                          editionViewDocumentation;
    @outlet CPView                          editionViewREST;
    @outlet CPView                          editionViewOperations;
    @outlet CPView                          viewAbstractsContainer;
    @outlet CPView                          viewContainer;

    @outlet SDModelAbstractsViewController  abstractsController;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Model";
}

+ (CPImage)moduleIcon
{
    return [SDAPIInfo icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [[self view] setBackgroundColor:NUSkinColorGrey];
    [viewContainer setBackgroundColor:NUSkinColorWhite];
    [viewBottom setBorderTopColor:NUSkinColorGrey];

    // var frame = [editionViewREST frame];
    // [frame.size.width = [scrollViewMain contentSize].width];
    // [editionViewREST setFrame:frame];
    //
    // var frame = [editionViewREST frame];
    // [frame.size.width = [scrollViewMain contentSize].width];
    // [editionViewGeneral setFrame:frame];
    //
    // var frame = [editionViewGeneral frame];
    // [frame.size.width = [scrollViewMain contentSize].width];
    // [editionViewGeneral setFrame:frame];

    var view = [abstractsController view];

    [viewAbstractsContainer setFrame:[view bounds]];
    [viewAbstractsContainer addSubview:[abstractsController view]];
    [abstractsController setParentModule:self];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleDidSetCurrentParent:(id)aParent
{
    [super moduleDidSetCurrentParent:aParent];

    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController setCurrentParent:_currentParent];

    [self setCurrentContextWithIdentifier:[_currentParent RESTName]];
}

- (void)moduleDidShow
{
    [super moduleDidShow];

    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController willShow];
}

- (void)moduleWillHide
{
    if ([_currentParent RESTName] == [SDSpecification RESTName])
        [abstractsController willHide];

    [super moduleWillHide];
}

- (void)configureContexts
{
    var contextSpecification = [[NUModuleContext alloc] initWithName:@"Model" identifier:[SDSpecification RESTName]];
    [contextSpecification setButtonSave:buttonSave];
    [contextSpecification setEditionView:[self view]];
    [contextSpecification setAdditionalEditionViews:[editionViewREST, editionViewDocumentation, editionViewOperations]];
    [self registerContext:contextSpecification forClass:SDSpecification];

    var contextAbstract = [[NUModuleContext alloc] initWithName:@"Model" identifier:[SDAbstract RESTName]];
    [contextAbstract setButtonSave:buttonSave];
    [contextAbstract setEditionView:[self view]];
    [contextAbstract setAdditionalEditionViews:[editionViewDocumentation, editionViewOperations]];
    [self registerContext:contextAbstract forClass:SDAbstract];
}

- (CPArray)moduleCurrentVisibleEditionViews
{
    if ([_currentParent RESTName] == [SDSpecification RESTName])
    {
        if ([_currentParent root])
            return [editionViewREST, editionViewDocumentation];
        else
            return [editionViewREST, editionViewOperations, editionViewDocumentation];
    }
    else
        return [editionViewOperations, editionViewDocumentation];
}

- (void)performPostPushOperation
{
    [super performPostPushOperation];
    [self updateVisibleEditionsView:self];
}

- (void)moduleUpdateEditorInterface
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanEdit               = conditionRepoHasPushPermission;

    [_currentContext setBoundControlsEnabled:conditionCanEdit];
}


#pragma mark -
#pragma mark Actions

- (@action)updateVisibleEditionsView:(id)aSender
{
    [self reloadStackView];
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
