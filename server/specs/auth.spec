{
    "attributes": [
        {
            "description": "the username of the current user",
            "name": "userName",
            "type": "string"
        }
    ],
    "children": [
        {
            "create": true,
            "get": true,
            "membership": "root",
            "rest_name": "token"
        },
        {
            "create": true,
            "get": true,
            "membership": "root",
            "rest_name": "repository"
        }
    ],
    "model": {
        "description": "Authentication API",
        "entity_name": "Auth",
        "extends": [
            "@parsable"
        ],
        "package": "github",
        "resource_name": "auth",
        "rest_name": "auth",
        "root": true
    }
}