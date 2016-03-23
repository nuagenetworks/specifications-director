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

@global SDAttributeTypeBoolean
@global SDAttributeTypeEnum
@global SDAttributeTypeFloat
@global SDAttributeTypeInteger
@global SDAttributeTypeList
@global SDAttributeTypeObject
@global SDAttributeTypeString
@global SDAttributeTypeTime


@implementation SDTypeToColorTransformer: CPValueTransformer

+ (Class)transformedValueClass
{
    return CPString;
}

+ (BOOL)allowsReverseTransformation
{
    return NO;
}

- (id)transformedValue:(id)value
{
    switch (value)
    {
        case SDAttributeTypeBoolean:
            return [CPColor colorWithHexString:@"9acd99"];

        case SDAttributeTypeEnum:
            return [CPColor colorWithHexString:@"659aff"];

        case SDAttributeTypeFloat:
            return [CPColor colorWithHexString:@"8c49a0"];

        case SDAttributeTypeInteger:
            return [CPColor colorWithHexString:@"ffd07a"];

        case SDAttributeTypeList:
            return [CPColor colorWithHexString:@"c4c4e6"];

        case SDAttributeTypeObject:
            return [CPColor colorWithHexString:@"cccd9a"];

        case SDAttributeTypeString:
            return [CPColor colorWithHexString:@"ff9a00"];

        case SDAttributeTypeTime:
            return [CPColor colorWithHexString:@"009acc"];
    }

    return [CPColor redColor];
}

@end


// registration
SDTypeToColorTransformerName = @"SDTypeToColorTransformerName";
[CPValueTransformer setValueTransformer:[SDTypeToColorTransformer new] forName:SDTypeToColorTransformerName];
