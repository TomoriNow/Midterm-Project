from django import template
register = template.Library()

@register.simple_tag
def get_book(entry):
    if hasattr(entry, "custom_entry"):
        return entry.custom_entry
    elif hasattr(entry, "catalog_entry"):
        return entry.catalog_entry.book