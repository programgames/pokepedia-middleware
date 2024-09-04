from django.core.exceptions import ObjectDoesNotExist


def get_object_or_none(model, identifier):
    try:
        return model.objects.get(identifier=identifier)
    except ObjectDoesNotExist:
        return None

