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
            "allowed_choices": ["child", "member", "root"],
            "description": "Defines if the api is deprecated",
            "type": "enum"
        },
        "allowsGet": {
            "description": "Defines if teh available operations",
            "type": "bool"
        },
        "allowsCreate": {
            "description": "Defines if teh available operations",
            "type": "bool"
        },
        "allowsUpdate": {
            "description": "Defines if teh available operations",
            "type": "bool"
        },
        "allowsDelete": {
            "description": "Defines if teh available operations",
            "type": "bool"
        },
        "associatedSpecificationID": {
            "description": "the associated specification.",
            "type": "string"
        }
    }
}