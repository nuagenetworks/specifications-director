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
@import <NUKit/NUAbstractDataView.j>


@implementation SDSpecificationDataView : NUAbstractDataView
{
    @outlet CPImageView imageViewEdited;
    @outlet CPImageView imageViewWarning;
    @outlet CPTextField fieldName;
}


#pragma mark -
#pragma mark Data View Protocol

- (void)bindDataView
{
    [super bindDataView];

    var negateBoolTransformer = @{CPValueTransformerNameBindingOption: CPNegateBooleanTransformerName},
        entityRESTName        = [_objectValue objectRESTName],
        specificationName     = entityRESTName ? entityRESTName : @"resource - " + [_objectValue entityName];
        
    [fieldName setStringValue:specificationName];
                
    [imageViewWarning setHidden:!!![_objectValue issues]];
    [imageViewEdited bind:CPHiddenBinding toObject:_objectValue withKeyPath:@"syncing" options:negateBoolTransformer];

    if ([_objectValue issues])
        [imageViewWarning setToolTip:@"Some errors has been found during the parsing of the remote specification. Please review"];
}


#pragma mark -
#pragma mark CPCoding compliance

- (id)initWithCoder:(CPCoder)aCoder
{
    if (self = [super initWithCoder:aCoder])
    {
        fieldName        = [aCoder decodeObjectForKey:@"fieldName"];
        imageViewEdited  = [aCoder decodeObjectForKey:@"imageViewEdited"];
        imageViewWarning = [aCoder decodeObjectForKey:@"imageViewWarning"];
    }

    return self;
}

- (void)encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:fieldName forKey:@"fieldName"];
    [aCoder encodeObject:imageViewEdited forKey:@"imageViewEdited"];
    [aCoder encodeObject:imageViewWarning forKey:@"imageViewWarning"];
}

@end
