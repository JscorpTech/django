SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CAMELIZE_NAMES": True,
    "POSTPROCESSING_HOOKS": ["config.conf.spectacular.custom_postprocessing_hook"],
}


def custom_postprocessing_hook(result, generator, request, public):
    """
    Customizes the API schema to wrap all responses in a standard format.
    """
    for path, methods in result.get("paths", {}).items():
        for method, operation in methods.items():
            if "responses" in operation:
                for status_code, response in operation["responses"].items():
                    if "content" in response:
                        for content_type, content in response["content"].items():
                            # Wrap original schema
                            original_schema = content.get("schema", {})
                            response["content"][content_type]["schema"] = {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "boolean", "example": True},
                                    "data": original_schema,
                                },
                                "required": ["status", "data"],
                            }
    return result
