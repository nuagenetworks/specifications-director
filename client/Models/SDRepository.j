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

@class SDAbstractsFetcher
@class SDAPIInfosFetcher
@class SDMonolitheConfigsFetcher
@class SDSpecificationsFetcher

NURepositoryCurrent = nil;

SDRepositoryStatusREADY = @"READY";
SDRepositoryStatusPULLING = @"PULLING";
SDRepositoryStatusNEEDS_PULL = @"NEEDS_PULL";
SDRepositoryStatusERROR = @"ERROR";
SDRepositoryStatusQUEUED = @"QUEUED";
SDRepositoryStatusMERGING = @"MERGING";


@implementation SDRepository : SDRESTObject
{
    BOOL                        _pushPermission     @accessors(property=pushPermission);
    CPString                    _associatedTokenID  @accessors(property=associatedTokenID);
    CPString                    _branch             @accessors(property=branch);
    CPString                    _name               @accessors(property=name);
    CPString                    _organization       @accessors(property=organization);
    CPString                    _password           @accessors(property=password)
    CPString                    _path               @accessors(property=path);
    CPString                    _repository         @accessors(property=repository);
    CPString                    _status             @accessors(property=status);
    CPString                    _url                @accessors(property=url);
    CPString                    _username           @accessors(property=username);

    SDAbstractsFetcher          _abstracts          @accessors(property=abstracts);
    SDAPIInfosFetcher           _APIInfos           @accessors(property=APIInfos);
    SDMonolitheConfigsFetcher   _monolitheConfigs   @accessors(property=monolitheConfigs);
    SDSpecificationsFetcher     _specifications     @accessors(property=specifications);
}

+ (id)currentRepository
{
    return NURepositoryCurrent;
}

+ (void)setCurrentRepository:(id)anRepository
{
    NURepositoryCurrent = anRepository;
}

#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"repository";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"associatedTokenID"];
        [self exposeLocalKeyPathToREST:@"branch"];
        [self exposeLocalKeyPathToREST:@"name"];
        [self exposeLocalKeyPathToREST:@"organization"];
        [self exposeLocalKeyPathToREST:@"password"];
        [self exposeLocalKeyPathToREST:@"path"];
        [self exposeLocalKeyPathToREST:@"pushPermission"];
        [self exposeLocalKeyPathToREST:@"repository"];
        [self exposeLocalKeyPathToREST:@"status"];
        [self exposeLocalKeyPathToREST:@"url"];
        [self exposeLocalKeyPathToREST:@"username"];

        _organization = [[SDAuth defaultUser] userName];
        _url          = @"https://api.github.com";
        _status       = SDRepositoryStatusNEEDS_PULL;
        _branch       = @"master";
        _path         = @"/";

        _APIInfos         = [SDAPIInfosFetcher fetcherWithParentObject:self];
        _specifications   = [SDSpecificationsFetcher fetcherWithParentObject:self];
        _abstracts        = [SDAbstractsFetcher fetcherWithParentObject:self];
        _monolitheConfigs = [SDMonolitheConfigsFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setOrganization:(CPString)anOrganization
{
    if (_organization == anOrganization)
        return;

    [self willChangeValueForKey:@"organization"];
    [self willChangeValueForKey:@"description"];
    _organization = anOrganization
    [self didChangeValueForKey:@"organization"];
    [self didChangeValueForKey:@"description"];
}

- (void)setRepository:(CPString)aRepository
{
    if (_repository == aRepository)
        return;

    [self willChangeValueForKey:@"repository"];
    [self willChangeValueForKey:@"description"];
    _repository = aRepository
    [self didChangeValueForKey:@"repository"];
    [self didChangeValueForKey:@"description"];
}

- (CPString)description
{
    return _organization + @"/" + _repository
}

@end
