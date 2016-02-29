{
    "attributes": [
        {
            "description": "Defines if teh available operations",
            "name": "allowsUpdate",
            "type": "bool"
        },
        {
            "description": "The name of the specification. example 'unicorn'",
            "name": "name",
            "required": true,
            "type": "string",
            "unique": true
        },
        {
            "description": "The package of the specification",
            "name": "package",
            "type": "string"
        },
        {
            "description": "True if a Github operation is running on this object",
            "name": "syncing",
            "type": "boolean"
        },
        {
            "description": "Defines if teh available operations",
            "name": "allowsCreate",
            "type": "bool"
        },
        {
            "description": "Defines if teh available operations",
            "name": "allowsGet",
            "type": "bool"
        },
        {
            "description": "Defines if teh available operations",
            "name": "allowsDelete",
            "type": "bool"
        },
        {
            "description": "The description of the specification. example 'unicorn is some kind of horse'",
            "name": "description",
            "type": "string"
        }
    ],
    "children": [
        {
            "create": true,
            "get": true,
            "relationship": "child",
            "rest_name": "attribute"
        },
        {
            "get": true,
            "relationship": "member",
            "rest_name": "abstract",
            "update": true
        },
        {
            "create": false,
            "get": true,
            "relationship": "child",
            "rest_name": "childapi"
        }
    ],
    "model": {
        "package": "specifications"
    }
}