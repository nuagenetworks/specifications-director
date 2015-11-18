/*
*   Filename:         NUVCenterObject.j
*   Created:          Mon Mar 23 10:44:31 PST 2015
*   Author:           Christophe Serafin <christophe.serafin@alcatel-lucent.com>
*   Description:      VSA
*   Project:          VSD - Nuage - Data Center Service Delivery - IPD
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
@import <NUKit/NUKitObject.j>
@import <NUKit/NUUtilities.j>

@implementation SDRESTObject : NUKitObject
{
    CPArrayController _issues   @accessors(property=issues)
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"issues"];
    }

    return self;
}

@end
