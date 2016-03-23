{
    "attributes": [
        {
            "description": "The prefix of the entire api.",
            "name": "prefix",
            "type": "string"
        },
        {
            "description": "The version of the api",
            "name": "version",
            "type": "string"
        },
        {
            "description": "The object in the specification to consider as the root object.",
            "name": "root",
            "type": "string"
        }
    ],
    "model": {
        "description": "Represents information about the entire specifications.",
        "entity_name": "APIInfo",
        "extends": [
            "@parsable"
        ],
        "package": "specifications",
        "resource_name": "apiinfos",
        "rest_name": "apiinfo"
    }
}