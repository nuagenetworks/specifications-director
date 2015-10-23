{
    "model": {
        "rest_name": "apiinfo",
        "resource_name": "apiinfos",
        "entity_name": "APIInfo",
        "description": "Represents information about the entire specifications.",
        "extends": ["@parsable"],
        "package": "specifications"
    },

    "attributes": {
        "version": {
            "description": "The version of the api",
            "type": "string"
        },
        "prefix": {
            "description": "The prefix of the entire api.",
            "type": "string"
        },
        "root": {
            "description": "The object in the specification to consider as the root object.",
            "type": "string"
        }
    }
}