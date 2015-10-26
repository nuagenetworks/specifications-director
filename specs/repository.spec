{
    "model": {
        "rest_name": "repository",
        "resource_name": "repositories",
        "entity_name": "Repository",
        "description": "Represents a github repository.",
        "extends": [],
        "package": "github"
    },

    "children": {
        "specification": {
            "get": true,
            "create": true
        },
        "abstract": {
            "get": true,
            "create": true
        },
        "apiinfo": {
            "get": true,
            "create": true
        },
        "job": {
            "get": true,
            "create": true
        }
    },

    "attributes": {
        "name": {
            "description": "The name of the organization",
            "type": "string",
            "unique": true
        },
        "url": {
            "description": "The Github API Url",
            "type": "string"
        },
        "password": {
            "description": "The password.",
            "type": "string"
        },
        "organization": {
            "description": "The organization.",
            "type": "string"
        },
        "repository": {
            "description": "The repository.",
            "type": "string"
        },
        "branch": {
            "description": "The branch.",
            "type": "string"
        },
        "path": {
            "description": "The relative path inside the repository.",
            "type": "string"
        }
    }
}