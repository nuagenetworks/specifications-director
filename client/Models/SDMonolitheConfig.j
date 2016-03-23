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
@import "Abstracts/SDRESTObject.j"

@implementation SDMonolitheConfig : SDRESTObject
{
    CPString     _APIDocOutput          @accessors(property=APIDocOutput);
    CPString     _APIDocUserVanilla     @accessors(property=APIDocUserVanilla);
    CPString     _copyright             @accessors(property=copyright);
    CPString     _productAccronym       @accessors(property=productAccronym);
    CPString     _productName           @accessors(property=productName);
    CPString     _SDKAuthor             @accessors(property=SDKAuthor);
    CPString     _SDKBambouVersion      @accessors(property=SDKBambouVersion);
    CPString     _SDKClassPrefix        @accessors(property=SDKClassPrefix);
    CPString     _SDKCLIName            @accessors(property=SDKCLIName);
    CPString     _SDKDescription        @accessors(property=SDKDescription);
    CPString     _SDKDocOutput          @accessors(property=SDKDocOutput);
    CPString     _SDKDocTMPPath         @accessors(property=SDKDocTMPPath);
    CPString     _SDKDocUserVanilla     @accessors(property=SDKDocUserVanilla)
    CPString     _SDKEmail              @accessors(property=SDKEmail);
    CPString     _SDKLicenseName        @accessors(property=SDKLicenseName);
    CPString     _SDKName               @accessors(property=SDKName);
    CPString     _SDKOutput             @accessors(property=SDKOutput)
    CPString     _SDKRevisionNumber     @accessors(property=SDKRevisionNumber);
    CPString     _SDKURL                @accessors(property=SDKURL);
    CPString     _SDKUserVanilla        @accessors(property=SDKUserVanilla);
    CPString     _SDKVersion            @accessors(property=SDKVersion);
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"monolitheconfig";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"APIDocOutput"];
        [self exposeLocalKeyPathToREST:@"APIDocUserVanilla"];
        [self exposeLocalKeyPathToREST:@"copyright"];
        [self exposeLocalKeyPathToREST:@"productAccronym"];
        [self exposeLocalKeyPathToREST:@"productName"];
        [self exposeLocalKeyPathToREST:@"SDKAuthor"];
        [self exposeLocalKeyPathToREST:@"SDKBambouVersion"];
        [self exposeLocalKeyPathToREST:@"SDKClassPrefix"];
        [self exposeLocalKeyPathToREST:@"SDKCLIName"];
        [self exposeLocalKeyPathToREST:@"SDKDescription"];
        [self exposeLocalKeyPathToREST:@"SDKDocOutput"];
        [self exposeLocalKeyPathToREST:@"SDKDocTMPPath"];
        [self exposeLocalKeyPathToREST:@"SDKDocUserVanilla"];
        [self exposeLocalKeyPathToREST:@"SDKEmail"];
        [self exposeLocalKeyPathToREST:@"SDKLicenseName"];
        [self exposeLocalKeyPathToREST:@"SDKName"];
        [self exposeLocalKeyPathToREST:@"SDKOutput"];
        [self exposeLocalKeyPathToREST:@"SDKRevisionNumber"];
        [self exposeLocalKeyPathToREST:@"SDKURL"];
        [self exposeLocalKeyPathToREST:@"SDKUserVanilla"];
        [self exposeLocalKeyPathToREST:@"SDKVersion"];
    }

    return self;
}

@end
