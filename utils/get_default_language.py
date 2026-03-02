from core.models import Language


def get_default_language():
    """
    Get the record as the default language to reference
    """
    lang, created = Language.objects.get_or_create(code="EN", name="English")

    return lang.id
