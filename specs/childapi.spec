{
    "attributes": [
        {
            "description": "Defines if the member objects can be assigned",
            "name": "allowsUpdate",
            "type": "bool"
        },
        {
            "description": "Defines if the child objects can be updated in bulk",
            "name": "allowsBulkUpdate",
            "type": "bool"
        },
        {
            "allowed_choices": [
                "child",
                "member",
                "root",
                "alias"
            ],
            "description": "Defines the kind of relation ship",
            "name": "relationship",
            "type": "enum"
        },
        {
            "description": "Defines if the api is deprecated",
            "name": "deprecated",
            "type": "boolean"
        },
        {
            "description": "Defines if the child objects can be created in bulk",
            "name": "allowsBulkCreate",
            "type": "bool"
        },
        {
            "description": "Defines if the child objects can be deleted in bulk",
            "name": "allowsBulkDelete",
            "type": "bool"
        },
        {
            "description": "Defines if the child objects can be created",
            "name": "allowsCreate",
            "type": "bool"
        },
        {
            "description": "the associated specification.",
            "name": "associatedSpecificationID",
            "type": "string"
        },
        {
            "description": "Defines if the child objects can be retrieved",
            "name": "allowsGet",
            "type": "bool"
        },
        {
            "description": "Defines if the api is deprecated",
            "name": "path",
            "transient": true,
            "type": "string"
        },
        {
            "description": "Defines if the child objects can be deleted",
            "name": "allowsDelete",
            "type": "bool"
        }
    ],
    "model": {
        "description": "Represents an child api.",
        "entity_name": "ChildAPI",
        "extends": [
            "@parsable"
        ],
        "package": "specifications",
        "resource_name": "childapis",
        "rest_name": "childapi"
    }
}