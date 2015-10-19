{
    "apis": {
        "children": {
            "/specifications/{id}/abstracts": {
                "RESTName": "abstract",
                "resourceName": "abstracts",
                "entityName": "Abstract",
                "relationship": "member",
                "operations": [
                    {
                        "availability": null,
                        "method": "GET"
                    },
                    {
                        "availability": null,
                        "method": "PUT"
                    }
                ]
            }
        }
    },
    "model": {
        "RESTName": "specification",
        "resourceName": "specifications",
        "entityName": "Specification",
        "description": "Represents the specification of an object.",
        "extends": ["@parsable", "@specification"]
    }
}