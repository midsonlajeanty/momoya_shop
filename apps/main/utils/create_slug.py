from django.utils.text import slugify

from apps.main.utils import random_number
from apps.main.utils import random_string

def create_slug(instance, field_name=None, slug=None):
    """Create model slug

    Args:
        instance (Model): instance model
        field_name (str): field to create slug

    Returns:
        string: slug
    """

    if not slug is None:
        slug = slugify(slug) + '-' + str(random_number(6))
    else:

        if not hasattr(instance, field_name):
            raise AttributeError('Model has no attribute named "%s"' % field_name)

        if field_name is None:
            slug = random_string(32)
        else:
            slug = slugify(getattr(instance, field_name))
            slug = slug.replace('_', '-')

    Klass = instance.__class__

    if Klass.objects.filter(slug=slug).exists():
        return create_slug(instance, slug=slug)

    return slug