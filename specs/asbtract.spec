{
    "apis": {
        "parents": {
            "/abstracts/{id}/specifications": {
                "RESTName": "specification",
                "resourceName": "specifications",
                "entityName": "Specification",
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
        "RESTName": "abstract",
        "resourceName": "abstracts",
        "entityName": "Abstract",
        "description": "Represents the abstract specification of an object.",
        "extends": ["@parsable", "@specification"]
    }
}