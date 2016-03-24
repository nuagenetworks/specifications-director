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
    CPString     _author             @accessors(property=author);
    CPString     _bambouVersion      @accessors(property=bambouVersion);
    CPString     _classPrefix        @accessors(property=classPrefix);
    CPString     _CLIName            @accessors(property=CLIName);
    CPString     _copyright          @accessors(property=copyright);
    CPString     _description        @accessors(property=description);
    CPString     _docOutput          @accessors(property=docOutput);
    CPString     _email              @accessors(property=email);
    CPString     _licenseName        @accessors(property=licenseName);
    CPString     _name               @accessors(property=name);
    CPString     _output             @accessors(property=output)
    CPString     _productAccronym    @accessors(property=productAccronym);
    CPString     _productName        @accessors(property=productName);
    CPString     _revisionNumber     @accessors(property=revisionNumber);
    CPString     _URL                @accessors(property=URL);
    CPString     _userVanilla        @accessors(property=userVanilla);
    CPString     _version            @accessors(property=version);
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
        [self exposeLocalKeyPathToREST:@"author"];
        [self exposeLocalKeyPathToREST:@"bambouVersion"];
        [self exposeLocalKeyPathToREST:@"classPrefix"];
        [self exposeLocalKeyPathToREST:@"CLIName"];
        [self exposeLocalKeyPathToREST:@"copyright"];
        [self exposeLocalKeyPathToREST:@"description"];
        [self exposeLocalKeyPathToREST:@"docOutput"];
        [self exposeLocalKeyPathToREST:@"email"];
        [self exposeLocalKeyPathToREST:@"licenseName"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"output"];
        [self exposeLocalKeyPathToREST:@"productAccronym"];
        [self exposeLocalKeyPathToREST:@"productName"];
        [self exposeLocalKeyPathToREST:@"revisionNumber"];
        [self exposeLocalKeyPathToREST:@"URL"];
        [self exposeLocalKeyPathToREST:@"userVanilla"];
        [self exposeLocalKeyPathToREST:@"version"];
    }

    return self;
}

@end
