@import <Foundation/Foundation.j>
@import <NUKit/NUModuleSelfParent.j>
@import "../../Models/SDModels.j"


@implementation SDEditorAttributeSelfViewController : NUModuleSelfParent
{
    @outlet CPView viewEditorStringConfig;
    @outlet CPView viewEditorNumberConfig;
    @outlet CPView viewEditorEnumConfig;
    @outlet CPView viewEditorEnumFlags;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attribute";
}

+ (CPString)moduleTabIconIdentifier
{
    return @"self";
}

- (void)viewDidLoad
{
    [super viewDidLoad];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Attribute" identifier:[SDAttribute RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setSearchForTagsRecursively:YES];
    [context setAdditionalEditionViews:[viewEditionMain, viewEditorStringConfig, viewEditorNumberConfig, viewEditorEnumConfig, viewEditorEnumFlags]];
    [self registerContext:context forClass:SDAttribute];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleUpdateEditorInterface
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanEdit               = conditionRepoHasPushPermission;

    [_currentContext setBoundControlsEnabled:conditionCanEdit];
}


#pragma mark -
#pragma mark NUModuleSelfParent API

- (CPArray)moduleCurrentVisibleEditionViews
{
    var editionViews = [viewEditionMain],
        editedObject = [_currentContext editedObject];

    switch ([editedObject type])
    {
        case SDAttributeTypeInteger:
        case SDAttributeTypeFloat:
            [editionViews addObject:viewEditorNumberConfig]
            break;

        case SDAttributeTypeString:
            [editionViews addObject:viewEditorStringConfig];
            break;

        case SDAttributeTypeEnum:
            [editionViews addObject:viewEditorEnumConfig];
            break;
    }

    [editionViews addObject:viewEditorEnumFlags];

    return editionViews;
}

#pragma mark -
#pragma mark Action

- (IBAction)changeType:(id)aSender
{
    [self reloadStackView];
}

@end
