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

@global SDRepositoryStatusREADY;
@global SDRepositoryStatusPULLING;
@global SDRepositoryStatusNEEDS_PULL;
@global SDRepositoryStatusERROR;
@global SDRepositoryStatusQUEUED;


@implementation SDRepositoryStatusToImageTransformer: CPValueTransformer

+ (Class)transformedValueClass
{
    return CPImage;
}

+ (BOOL)allowsReverseTransformation
{
    return NO;
}

- (id)transformedValue:(id)value
{
    switch (value)
    {
        case SDRepositoryStatusREADY:
            return CPImageInBundle('repo-status-ready.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusPULLING:
            return CPImageInBundle('repo-status-pulling.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusNEEDS_PULL:
            return CPImageInBundle('repo-status-needspull.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusERROR:
            return CPImageInBundle('repo-status-error.png', CGSizeMake(16.0, 16.0));

        case SDRepositoryStatusQUEUED:
            return CPImageInBundle('repo-status-queued.png', CGSizeMake(16.0, 16.0));
    }
}

@end


// registration
SDRepositoryStatusToImageTransformerName = @"SDRepositoryStatusToImageTransformerName";
[CPValueTransformer setValueTransformer:[SDRepositoryStatusToImageTransformer new] forName:SDRepositoryStatusToImageTransformerName];
