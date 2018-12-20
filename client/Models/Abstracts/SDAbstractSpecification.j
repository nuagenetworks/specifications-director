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
@import "SDRESTObject.j"

@class SDAttributesFetcher
@class SDChildAPIsFetcher


@implementation SDAbstractSpecification : SDRESTObject
{
    BOOL                _allowsCreate           @accessors(property=allowsCreate);
    BOOL                _allowsDelete           @accessors(property=allowsDelete);
    BOOL                _allowsGet              @accessors(property=allowsGet);
    BOOL                _allowsUpdate           @accessors(property=allowsUpdate);
    BOOL                _embedded               @accessors(property=embedded);
    BOOL                _syncing                @accessors(property=syncing);
    BOOL                _root                   @accessors(property=root);
    BOOL                _template               @accessors(property=template);
    CPString            _description            @accessors(property=description);
    CPString            _entityName             @accessors(property=entityName);
    CPString            _name                   @accessors(property=name);
    CPString            _objectResourceName     @accessors(property=objectResourceName);
    CPString            _objectRESTName         @accessors(property=objectRESTName)
    CPString            _package                @accessors(property=package);
    CPString            _userlabel              @accessors(property=userlabel);
    CPArrayController   _allowedJobCommands     @accessors(property=allowedJobCommands);

    SDAttributesFetcher _attributes             @accessors(property=attributes);
    SDChildAPIsFetcher  _childAPIs              @accessors(property=childAPIs);
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeBindableAttribute:@"embedded"];
        [self exposeLocalKeyPathToREST:@"allowedJobCommands"];
        [self exposeLocalKeyPathToREST:@"allowsCreate"];
        [self exposeLocalKeyPathToREST:@"allowsDelete"];
        [self exposeLocalKeyPathToREST:@"allowsGet"];
        [self exposeLocalKeyPathToREST:@"allowsUpdate"];
        [self exposeLocalKeyPathToREST:@"description"];
        [self exposeLocalKeyPathToREST:@"syncing"];
        [self exposeLocalKeyPathToREST:@"entityName"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"objectResourceName"];
        [self exposeLocalKeyPathToREST:@"objectRESTName"];
        [self exposeLocalKeyPathToREST:@"package"];
        [self exposeLocalKeyPathToREST:@"root"];
        [self exposeLocalKeyPathToREST:@"template"];
        [self exposeLocalKeyPathToREST:@"userlabel"];

        _allowedJobCommands  = [[CPArrayController alloc] initWithContent:[]];
        _allowsDelete = YES;
        _allowsGet    = YES;
        _allowsUpdate = YES;
        _allowsCreate = NO;
        _embedded = NO;

        _attributes   = [SDAttributesFetcher fetcherWithParentObject:self];
        _childAPIs    = [SDChildAPIsFetcher fetcherWithParentObject:self];
    }

    return self;
}

@end
