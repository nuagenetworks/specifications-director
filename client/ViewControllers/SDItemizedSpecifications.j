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
@import <NUKit/NUModuleItemized.j>
@import "../Models/SDModels.j"

@class SDAbstractsViewController
@class SDAPIInfoViewController
@class SDMonolitheConfigsViewController
@class SDSpecificationsViewController

@implementation SDItemizedSpecifications : NUModuleItemized
{
    @outlet SDAbstractsViewController           abstractsController;
    @outlet SDAPIInfoViewController             APIInfoController;
    @outlet SDMonolitheConfigsViewController    monolitheConfigController;
    @outlet SDSpecificationsViewController      specificationsController;
}

#pragma mark -
#pragma mark Initialization

// + (CPColor)backgroundColor
// {
//     return NUSkinColorWhite;
// }
//
// + (CPColor)selectionColor
// {
//     return NUSkinColorGrey;
// }
//
// + (CPColor)itemBorderColor
// {
//     return nil;
// }
//
// + (CPColor)itemTextColor
// {
//     return NUSkinColorBlack;
// }
//
// + (CPColor)itemSelectedTextColor
// {
//     return NUSkinColorBlack;
// }
//
// + (CPColor)separatorColor
// {
//     return NUSkinColorGreyLight;
// }

+ (CPString)moduleName
{
    return @"Specifications";
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    [self setSubModules:[specificationsController, abstractsController, APIInfoController, monolitheConfigController]];
}


#pragma mark -
#pragma mark NUModuleItemized API

- (CPArray)moduleItemizedCurrentItems
{
    return  [   {"module": specificationsController, "children": nil},
                {"module": abstractsController, "children": nil},
                {"module": nil},
                {"module": APIInfoController, "children": nil},
                {"module": monolitheConfigController, "children": nil}
            ];
}

@end
