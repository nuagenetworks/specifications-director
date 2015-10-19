{
    "apis": {
        "children": {
            "/[__RESOURCE_NAME__]/{id}/attributes": {
                "RESTName": "attribute",
                "resourceName": "attributes",
                "entityName": "Attribute",
                "operations": [
                    {
                        "availability": null,
                        "method": "GET"
                    },
                    {
                        "availability": null,
                        "method": "POST"
                    }
                ]
            },
            "/[__RESOURCE_NAME__]/{id}/childapis": {
                "RESTName": "childapi",
                "resourceName": "childapis",
                "entityName": "ChildAPI",
                "operations": [
                    {
                        "availability": null,
                        "method": "GET"
                    }
                ]
            },
            "/[__RESOURCE_NAME__]/{id}/parentapis": {
                "RESTName": "parentapi",
                "resourceName": "parentapis",
                "entityName": "ParentAPI",
                "operations": [
                    {
                        "availability": null,
                        "method": "GET"
                    },
                    {
                        "availability": null,
                        "method": "POST"
                    }
                ]
            }
        },
        "parents": {
            "/repositories/{id}/[__RESOURCE_NAME__]": {
                "RESTName": "[__REST_NAME__]",
                "resourceName": "[__RESOURCE_NAME__]",
                "entityName": "[__ENTITY_NAME__]",
                "operations": [
                    {
                        "availability": null,
                        "method": "GET"
                    },
                    {
                        "availability": null,
                        "method": "POST"
                    }
                ]
            }
        },
        "self": {
            "/[__RESOURCE_NAME__]/{id}": {
                "RESTName": "[__REST_NAME__]",
                "resourceName": "[__RESOURCE_NAME__]",
                "entityName": "[__ENTITY_NAME__]",
                "operations": [
                    {
                        "availability": null,
                        "method": "PUT"
                    },
                    {
                        "availability": null,
                        "method": "DELETE"
                    },
                    {
                        "availability": null,
                        "method": "GET"
                    }
                ]
            }
        }
    },
    "model": {
        "package": "specifications",

        "attributes": {
            "rootRESTName": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "the api root name",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": false
            },
            "name": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The name of the specification. example 'unicorn'",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": true,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "description": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The description of the specification. example 'unicorn is some kind of horse'",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "package": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The package of the specification",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "objectRESTName": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The rest name of the object. example 'unicorn'",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "objectResourceName": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The resource name of the object. example 'unicorns'",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": false,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "entityName": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": null,
                "description": "The entoty name of the object. example 'Unicorn'.",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": false,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "string",
                "unique": true
            },
            "extends": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": [],
                "description": "The other specifications this class extends",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": false,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "list",
                "unique": true
            },
            "allowsGet": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": false,
                "description": "Defines if teh available operations",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "bool",
                "unique": false
            },
            "allowsUpdate": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": false,
                "description": "Defines if teh available operations",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "bool",
                "unique": false
            },
            "allowsDelete": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": false,
                "defaultValue": false,
                "description": "Defines if teh available operations",
                "exposed": true,
                "filterable": true,
                "format": null,
                "maxLength": null,
                "maxValue": null,
                "minLength": null,
                "minValue": null,
                "orderable": true,
                "readOnly": false,
                "required": false,
                "transient": false,
                "type": "bool",
                "unique": false
            }
        }
    }
}