{
    "model": {
        "rest_name": "childapi",
        "resource_name": "childapis",
        "description": "Represents an child api.",
        "entity_name": "ChildAPI",
        "package": "specifications",
        "extends": ["@parsable"]
    },

    "attributes": {
        "path": {
            "description": "Defines if the api is deprecated",
            "transient": true,
            "type": "string"
        },
        "deprecated": {
            "description": "Defines if the api is deprecated",
            "type": "boolean"
        },
        "relationship": {
            "allowed_choices": ["child", "member", "root", "alias"],
            "description": "Defines the kind of relation ship",
            "type": "enum"
        },
        "allowsGet": {
            "description": "Defines if the child objects can be retrieved",
            "type": "bool"
        },
        "allowsCreate": {
            "description": "Defines if the child objects can be created",
            "type": "bool"
        },
        "allowsUpdate": {
            "description": "Defines if the member objects can be assigned",
            "type": "bool"
        },
        "allowsDelete": {
            "description": "Defines if the child objects can be deleted",
            "type": "bool"
        },
        "allowsBulkCreate": {
            "description": "Defines if the child objects can be created in bulk",
            "type": "bool"
        },
        "allowsBulkUpdate": {
            "description": "Defines if the child objects can be updated in bulk",
            "type": "bool"
        },
        "allowsBulkDelete": {
            "description": "Defines if the child objects can be deleted in bulk",
            "type": "bool"
        },
        "associatedSpecificationID": {
            "description": "the associated specification.",
            "type": "string"
        }
    }
}