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
@import <RESTCappuccino/RESTCappuccino.j>

// first import basic things
@import "Resources/Branding/branding.js"
@import "Resources/app-version.js"

@import "DataViews/SDDataViewsLoader.j"
@import "Models/SDModels.j"
@import "ViewControllers/SDViewControllers.j"
@import "Transformers/SDTransformers.j"
@import "Associators/SDAssociators.j"

NURESTUserRoleCSPRoot = @"NURESTUserRoleCSPRoot";
NURESTUserRoleOrgAdmin = @"NURESTUserRoleOrgAdmin"

SDApplicationShowServerLoginField = NO;

@global open

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
    //[[CPUserDefaults standardUserDefaults] setObject:@"https://127.0.0.1:2000" forKey:@"NUAPIURL"];

    if ([[NUKit kit] valueForApplicationArgument:@"serverfield"])
        SDApplicationShowServerLoginField = YES;

    [dataViewsLoader load];

    // configure NUKit
    [[NUKit kit] setCompanyName:BRANDING_INFORMATION["label-company-name"]];
    [[NUKit kit] setCompanyLogo:CPImageInBundle("Branding/logo-company.png")];
    [[NUKit kit] setApplicationName:BRANDING_INFORMATION["label-application-name"]];
    [[NUKit kit] setApplicationLogo:CPImageInBundle("Branding/logo-application.png")];
    [[NUKit kit] setCopyright:[self _copyrightString]];
    [[NUKit kit] setAPIPrefix:@"api/"];

    [[[NUKit kit] loginWindowController] setShowsEnterpriseField:NO];
    [[[NUKit kit] loginWindowController] setShowsServerField:SDApplicationShowServerLoginField];

    [[NUKit kit] parseStandardApplicationArguments];
    [[NUKit kit] loadFrameworkDataViews];
    [[NUKit kit] setDelegate:self];

    [[NUKit kit] setRESTUser:[SDAuth defaultUser]];

    [[NUKit kit] setToolbarBackgroundColor:NUSkinColorBlack];
    [[NUKit kit] setToolbarForegroundColor:[CPColor colorWithHexString:@"fff"]];

    [[NUKit kit] registerCoreModule:repositoriesController];

    [[NUKit kit] registerPrincipalModule:configurationController
                         withButtonImage:CPImageInBundle(@"toolbar-preferences.png", 32.0, 32.0)
                                altImage:CPImageInBundle(@"toolbar-preferences-pressed.png", 32.0, 32.0)
                                 toolTip:@"Open Preferences"
                              identifier:@"button-toolbar-tokens"
                       availableToRoles:[NURESTUserRoleCSPRoot]];


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


#pragma mark -
#pragma mark Copyright

- (CPString)_copyrightString
{
    var copyright = BRANDING_INFORMATION["label-company-name"];

    if (!copyright || !copyright.length)
        return [CPString stringWithFormat:@"Version %@ (%@)", APP_BUILDVERSION, APP_GITVERSION];
    else
        return [CPString stringWithFormat:@"Copyright \u00A9 %@ %@ - %@ (%@)", new Date().getFullYear(), copyright, APP_BUILDVERSION, APP_GITVERSION];
}

@end