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

@implementation SDAPIInfoViewController : NUModuleSelfParent
{
    @outlet CPTextField fieldAPIVersion;
    @outlet CPTextField fieldAPIPrefix;
    @outlet CPView      editionViewGeneral;
    @outlet CPView      viewContainer;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"API Information";
}

+ (CPImage)moduleIcon
{
    return [SDAPIInfo icon];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [[self view] setBackgroundColor:NUSkinColorGrey];
    [scrollViewMain setBorderTopColor:NUSkinColorGrey];
    [viewContainer setBackgroundColor:NUSkinColorWhite];
    [viewBottom setBorderTopColor:NUSkinColorGrey];
}


#pragma mark -
#pragma mark NUModule API

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"API Info" identifier:[SDAPIInfo RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setAdditionalEditionViews:[editionViewGeneral]];
    [self registerContext:context forClass:SDAPIInfo];
}

- (CPArray)moduleCurrentVisibleEditionViews
{
    return [editionViewGeneral];
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


#pragma mark -
#pragma mark Overrides

- (void)willShow
{
    // pass here, see below.
}

- (void)setCurrentParent:(NUVSDObject)aParent
{
    if (!aParent)
    {
        [super setCurrentParent:nil];
        return;
    }

    [[aParent APIInfos] fetchAndCallBlock:function(fetcher, entity, content) {
        [super setCurrentParent:[content firstObject]];
        [super willShow];
    }];
}

@end
