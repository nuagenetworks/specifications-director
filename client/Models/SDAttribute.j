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

SDAttributeTypeBoolean = @"boolean"
SDAttributeTypeEnum    = @"enum"
SDAttributeTypeFloat   = @"float"
SDAttributeTypeInteger = @"integer"
SDAttributeTypeList    = @"list"
SDAttributeTypeObject  = @"object"
SDAttributeTypeString  = @"string"
SDAttributeTypeTime    = @"time"

SDAttributeFormatFree = @"free";
SDAttributeFormatEmail = @"email";
SDAttributeFormatPhoneNumber = @"phoneNumber";
SDAttributeFormatIPv4 = @"IPv4";
SDAttributeFormatIPv6 = @"IPv6";
SDAttributeFormatDate = @"date";


@implementation SDAttribute : SDRESTObject
{
    BOOL                _autogenerated  @accessors(property=autogenerated);
    BOOL                _creationOnly   @accessors(property=creationOnly);
    BOOL                _defaultOrder   @accessors(property=defaultOrder);
    BOOL                _deprecated     @accessors(property=deprecated);
    BOOL                _exposed        @accessors(property=exposed);
    BOOL                _filterable     @accessors(property=filterable);
    BOOL                _orderable      @accessors(property=orderable);
    BOOL                _readOnly       @accessors(property=readOnly);
    BOOL                _required       @accessors(property=required);
    BOOL                _transient      @accessors(property=transient);
    BOOL                _unique         @accessors(property=unique);
    CPArrayController   _allowedChoices @accessors(property=allowedChoices);
    // CPArrayController   _availability   @accessors(property=availability);
    CPNumber            _maxLength      @accessors(property=maxLength);
    CPNumber            _maxValue       @accessors(property=maxValue);
    CPNumber            _minLength      @accessors(property=minLength);
    CPNumber            _minValue       @accessors(property=minValue);
    CPString            _allowedChars   @accessors(property=allowedChars);
    CPString            _channel        @accessors(property=channel);
    CPString            _defaultValue   @accessors(property=defaultValue);
    CPString            _description    @accessors(property=description);
    CPString            _format         @accessors(property=format);
    CPString            _name           @accessors(property=name);
    CPString            _type           @accessors(property=type);
    CPString            _subtype        @accessors(property=subtype);
    CPString            _userlabel      @accessors(property=userlabel);
}


#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"attribute";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"autogenerated"];
        [self exposeLocalKeyPathToREST:@"creationOnly"];
        [self exposeLocalKeyPathToREST:@"defaultOrder"];
        [self exposeLocalKeyPathToREST:@"deprecated"];
        [self exposeLocalKeyPathToREST:@"exposed"];
        [self exposeLocalKeyPathToREST:@"filterable"];
        [self exposeLocalKeyPathToREST:@"orderable"];
        [self exposeLocalKeyPathToREST:@"readOnly"];
        [self exposeLocalKeyPathToREST:@"required"];
        [self exposeLocalKeyPathToREST:@"transient"];
        [self exposeLocalKeyPathToREST:@"unique"];
        [self exposeLocalKeyPathToREST:@"allowedChoices"];
        // [self exposeLocalKeyPathToREST:@"availability"];
        [self exposeLocalKeyPathToREST:@"maxLength"];
        [self exposeLocalKeyPathToREST:@"maxValue"];
        [self exposeLocalKeyPathToREST:@"minLength"];
        [self exposeLocalKeyPathToREST:@"minValue"];
        [self exposeLocalKeyPathToREST:@"allowedChars"];
        [self exposeLocalKeyPathToREST:@"channel"];
        [self exposeLocalKeyPathToREST:@"defaultValue"];
        [self exposeLocalKeyPathToREST:@"description"];
        [self exposeLocalKeyPathToREST:@"format"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"type"];
        [self exposeLocalKeyPathToREST:@"subtype"];
        [self exposeLocalKeyPathToREST:@"userlabel"];

        _autogenerated = NO;
        _creationOnly = NO;
        _defaultOrder = NO;
        _deprecated = NO;
        _exposed = YES;
        _filterable = YES;
        _orderable = YES;
        _readOnly = NO;
        _required = NO;
        _transient = NO;
        _unique = NO;
        _type = SDAttributeTypeString
        _format = SDAttributeFormatFree;

        _allowedChoices = [[CPArrayController alloc] initWithContent:[]];
        // _availability = [[CPArrayController alloc] initWithContent:[]];
    }

    return self;
}

@end
