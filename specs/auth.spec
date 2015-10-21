{
    "rest_name": "auth",
    "resource_name": "auth",
    "entity_name": "Auth",
    "description": "Authentication API",
    "extends": ["@parsable"],
    "package": "github",
    "root": true,

    "children": [
        {
            "specification": "repository",
            "get": true,
            "create": true
        }
    ],

    "attributes": {
        "userName": {
            "type": "string",
            "description": "the username of the current user"
        }
    }
}