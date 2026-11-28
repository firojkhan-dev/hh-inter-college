from django import template


register = template.Library()


@register.simple_tag
def translated(instance, field_name, language):
    english_value = getattr(instance, field_name, "")
    if language == "hi":
        hindi_value = getattr(instance, f"{field_name}_hi", "")
        if hindi_value:
            return hindi_value
    return english_value
