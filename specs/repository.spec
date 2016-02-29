{
    "attributes": [
        {
            "allowed_choices": [
                "READY",
                "PULLING",
                "NEEDS_PULL",
                "ERROR",
                "QUEUED",
                "MERGING"
            ],
            "default_value": "NEEDS_PULL",
            "description": "Defines if everything is fine with the information.",
            "name": "status",
            "type": "enum"
        },
        {
            "description": "The name of the organization",
            "name": "name",
            "type": "string",
            "unique": true
        },
        {
            "description": "The repository.",
            "name": "repository",
            "type": "string"
        },
        {
            "description": "The token to use.",
            "name": "associatedTokenID",
            "type": "string"
        },
        {
            "description": "The Github API Url",
            "name": "url",
            "type": "string"
        },
        {
            "description": "Defines if the current user can push on the repository.",
            "name": "pushPermission",
            "type": "boolean"
        },
        {
            "description": "The branch.",
            "name": "branch",
            "type": "string"
        },
        {
            "description": "The relative path inside the repository.",
            "name": "path",
            "type": "string"
        },
        {
            "description": "The organization.",
            "name": "organization",
            "type": "string"
        },
        {
            "description": "The password.",
            "name": "password",
            "type": "string"
        }
    ],
    "children": [
        {
            "create": true,
            "get": true,
            "rest_name": "job"
        },
        {
            "create": true,
            "get": true,
            "rest_name": "specification"
        },
        {
            "create": true,
            "get": true,
            "rest_name": "apiinfo"
        },
        {
            "create": true,
            "get": true,
            "rest_name": "monolitheconfig"
        },
        {
            "create": true,
            "get": true,
            "rest_name": "abstract"
        }
    ],
    "model": {
        "description": "Represents a github repository.",
        "entity_name": "Repository",
        "extends": [],
        "package": "github",
        "resource_name": "repositories",
        "rest_name": "repository"
    }
}