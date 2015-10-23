{
    "model" : {
        "package": "specifications"
    },

    "children": {
        "attribute": {
            "relationship": "child",
            "get": true,
            "create": true
        },
        "childapi": {
            "relationship": "child",
            "get": true,
            "create": false
        },
        "abstract": {
            "relationship": "member",
            "get": true,
            "update": true
        }
    },

    "attributes": {
        "syncing": {
            "description": "True if a Github operation is running on this object",
            "type": "boolean"
        },
        "name": {
            "description": "The name of the specification. example 'unicorn'",
            "required": true,
            "type": "string",
            "unique": true
        },
        "description": {
            "description": "The description of the specification. example 'unicorn is some kind of horse'",
            "type": "string"
        },
        "package": {
            "description": "The package of the specification",
            "type": "string"
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
            "description": "The entoty name of the object. example 'Unicorn'.",
            "type": "string"
        },
        "allowsGet": {
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
        "allowsCreate": {
            "description": "Defines if teh available operations",
            "type": "bool"
        }
    }
}