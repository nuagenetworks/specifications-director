{
    "attributes": [
        {
            "description": "The rest name of the object. example 'unicorn'",
            "name": "objectRESTName",
            "type": "string"
        },
        {
            "description": "The resource name of the object. example 'unicorns'",
            "name": "objectResourceName",
            "type": "string"
        },
        {
            "description": "true if root api",
            "name": "root",
            "type": "boolean"
        },
        {
            "description": "The entity name of the object. example 'Unicorn'.",
            "name": "entityName",
            "type": "string"
        },
        {
            "description": "Preferred label for this entity on the UI.",
            "name": "userlabel",
            "type": "string"
        },
        {
            "description": "true if the corresponding entity serves as a template",
            "name": "template",
            "type": "boolean"
        },
        {
            "description": "Applicable jobs for this entity",
            "name": "allowedJobs",
            "type": "list"
        }
    ],
    "model": {
        "description": "Represents the specification of an object.",
        "entity_name": "Specification",
        "extends": [
            "@parsable",
            "@specification"
        ],
        "resource_name": "specifications",
        "rest_name": "specification"
    }
}
