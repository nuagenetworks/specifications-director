{
    "model": {
        "rest_name": "job",
        "resource_name": "jobs",
        "description": "Represent a job",
        "entity_name": "Job",
        "package": "specifications",
        "extends": []
    },

    "attributes": {
        "command": {
            "description": "The command",
            "allowed_choices": ["pull", "commit", "checkout"],
            "type": "enum"
        },
        "status": {
            "description": "The status",
            "type": "string"
        },
        "result": {
            "description": "the result",
            "type": "string"
        }
    }
}