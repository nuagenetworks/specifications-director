{
    "model": {
        "RESTName": "childapi",
        "resourceName": "childapis",
        "description": "Represents an child api.",
        "entityName": "ChildAPI",
        "extends": ["@api", "@parsable"],
        "attributes": {
            "associatedParentAPIID": {
                "allowedChars": null,
                "allowedChoices": null,
                "autogenerated": false,
                "availability": null,
                "channel": null,
                "creationOnly": false,
                "defaultOrder": true,
                "defaultValue": null,
                "description": "the related reverse API",
                "exposed": true,
                "filterable": false,
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
                "unique": false
            }
        }
    }
}