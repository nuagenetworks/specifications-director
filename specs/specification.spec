{
    "model": {
        "rest_name": "specification",
        "resource_name": "specifications",
        "entity_name": "Specification",
        "description": "Represents the specification of an object.",
        "extends": ["@parsable", "@specification"]
    },

    "attributes": {
        "root": {
            "description": "true if root api",
            "type": "boolean"
        },
        "objectRESTName": {
            "description": "The rest name of the object. example 'unicorn'",
            "type": "string"
        },
        "objectResourceName": {
            "description": "The resource name of the object. example 'unicorns'",
            "type": "string"
        },
        "entityName": {
            "description": "The entity name of the object. example 'Unicorn'.",
            "type": "string"
        }
    }
}