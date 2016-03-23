{
    "attributes": [
        {
            "description": "The status",
            "name": "status",
            "type": "string"
        },
        {
            "allowed_choices": [
                "pull",
                "commit",
                "checkout",
                "merge_master"
            ],
            "description": "The command",
            "name": "command",
            "type": "enum"
        },
        {
            "description": "the result",
            "name": "result",
            "type": "string"
        }
    ],
    "model": {
        "description": "Represent a job",
        "entity_name": "Job",
        "extends": [],
        "package": "specifications",
        "resource_name": "jobs",
        "rest_name": "job"
    }
}