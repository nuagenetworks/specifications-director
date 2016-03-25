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
@import <NUKit/NUAssociators.j>
@import <NUKit/NUCategories.j>
@import <NUKit/NUControls.j>
@import <NUKit/NUDataSources.j>
@import <NUKit/NUDataViews.j>
@import <NUKit/NUDataViewsLoaders.j>
@import <NUKit/NUHierarchyControllers.j>
@import <NUKit/NUKit.j>
@import <NUKit/NUModels.j>
@import <NUKit/NUModules.j>
@import <NUKit/NUSkins.j>
@import <NUKit/NUTransformers.j>
@import <NUKit/NUUtils.j>
@import <NUKit/NUWindowControllers.j>
@import <Bambou/Bambou.j>

@import "DataViews/SDDataViewsLoader.j"
@import "Models/SDModels.j"
@import "ViewControllers/SDViewControllers.j"
@import "Transformers/SDTransformers.j"
@import "Associators/SDAssociators.j"

SDApplicationShowServerLoginField = NO;

@global open
@global BRANDING_INFORMATION
@global SERVER_AUTO_URL
@global APP_BUILDVERSION
@global APP_GITVERSION


@implementation AppController : CPObject
{
    @outlet SDConfigurationViewController   configurationController;
    @outlet SDDataViewsLoader               dataViewsLoader;
    @outlet SDRepositoriesViewController    repositoriesController;
}


#pragma mark -
#pragma mark Initialization


- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    [CPMenu setMenuBarVisible:NO];

    var config = [[NUKit kit] moduleColorConfiguration];
    [config setObject:NUSkinColorBlack forKey:@"toolbar-background"];
    [config setObject:NUSkinColorWhite forKey:@"toolbar-foreground"];
    [[NUKit kit] setModuleColorConfiguration:config];

    if ([[NUKit kit] valueForApplicationArgument:@"serverfield"] || !SERVER_AUTO_URL || SERVER_AUTO_URL == @"")
        SDApplicationShowServerLoginField = YES;

    [dataViewsLoader load];

    // configure NUKit
    [[NUKit kit] setCompanyLogo:CPImageInBundle("Branding/logo-company.png")];
    [[NUKit kit] setApplicationLogo:CPImageInBundle("Branding/logo-application.png")];
    [[NUKit kit] setCompanyName:BRANDING_INFORMATION["label-company-name"]];
    [[NUKit kit] setApplicationName:BRANDING_INFORMATION["label-application-name"]];
    [[NUKit kit] setCopyright:[CPString stringWithFormat:@"Copyright \u00A9 %@ Nuage Networks - %@ (%@)", new Date().getFullYear(), APP_BUILDVERSION, APP_GITVERSION]];
    [[NUKit kit] setAutoServerBaseURL:SERVER_AUTO_URL];
    [[NUKit kit] setAPIPrefix:@"api/"];
    [[NUKit kit] setRootAPI:[SDAuth current]];

    [[[NUKit kit] loginWindowController] setShowsEnterpriseField:NO];
    [[[NUKit kit] loginWindowController] setShowsServerField:SDApplicationShowServerLoginField];

    [[NUKit kit] parseStandardApplicationArguments];
    [[NUKit kit] loadFrameworkDataViews];
    [[NUKit kit] setDelegate:self];

    [[NUKit kit] registerCoreModule:repositoriesController];

    [[NUKit kit] registerPrincipalModule:configurationController
                         withButtonImage:CPImageInBundle(@"toolbar-preferences.png", 32.0, 32.0)
                                altImage:CPImageInBundle(@"toolbar-preferences-pressed.png", 32.0, 32.0)
                                 toolTip:@"Open Preferences"
                              identifier:@"button-toolbar-tokens"
                       availableToRoles:nil];

    [[NUKit kit] startListenNotification];
    [[NUKit kit] manageLoginWindow];

    [[[NUKitToolBar defaultToolBar] buttonLogout] setValue:CPImageInBundle(@"toolbar-logout-light.png", 32.0, 32.0) forThemeAttribute:@"image" inState:CPThemeStateNormal];
}


#pragma mark -
#pragma mark Actions

- (IBAction)openInspector:(id)aSender
{
    [[NUKit kit] openInspectorForSelectedObject];
}

@end
