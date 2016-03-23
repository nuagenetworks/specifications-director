/*
*   Filename:         AppController.j
*   Created:          Tue Oct  9 11:56:38 PDT 2012
*   Author:           Antoine Mercadal <antoine.mercadal@alcatel-lucent.com>
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

SDApplicationShowServerLoginField = YES;

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

    if ([[NUKit kit] valueForApplicationArgument:@"serverfield"])
        SDApplicationShowServerLoginField = YES;

    [dataViewsLoader load];

    // configure NUKit
    [[NUKit kit] setCompanyLogo:CPImageInBundle("Branding/logo-company.png")];
    [[NUKit kit] setApplicationLogo:CPImageInBundle("Branding/logo-application.png")];
    [[NUKit kit] setCompanyName:BRANDING_INFORMATION["label-company-name"]];
    [[NUKit kit] setApplicationName:BRANDING_INFORMATION["label-application-name"]];
    [[NUKit kit] setCopyright:[CPString stringWithFormat:@"Copyright \u00A9 %@ nuage networks - %@ (%@)", new Date().getFullYear(), APP_BUILDVERSION, APP_GITVERSION]];
    [[NUKit kit] setAutoServerBaseURL:SERVER_AUTO_URL];
    [[NUKit kit] setAPIPrefix:@"api/"];
    [[NUKit kit] setRootAPI:[SDAuth defaultUser]];

    [[[NUKit kit] loginWindowController] setShowsEnterpriseField:NO];
    [[[NUKit kit] loginWindowController] setShowsServerField:SDApplicationShowServerLoginField];

    [[NUKit kit] parseStandardApplicationArguments];
    [[NUKit kit] loadFrameworkDataViews];
    [[NUKit kit] setDelegate:self];

    [[NUKit kit] setToolbarBackgroundColor:NUSkinColorBlack];
    [[NUKit kit] setToolbarForegroundColor:[CPColor colorWithHexString:@"fff"]];

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

@implementation CPTextField (noinvalid)
- (void)setInvalid:(BOOL)isInvalid reason:(CPString)aReason
{
}
- (void)setRequired:(BOOL)isRequired
{
}
@end
