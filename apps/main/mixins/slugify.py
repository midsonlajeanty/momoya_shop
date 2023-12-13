from django.db import models
from django.utils.text import slugify

class SluginfyMixin(models.Model):
    """Mixin to slugify a model's name field."""

    _slug_field = 'slug'
    _slugify_field = 'name'

    id = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override save method to slugify name field."""

        if not self.slug:
            if not hasattr(self, self._slugify_field):
                raise AttributeError('Model has no attribute named "%s"' % self._slugify_field)
            
            if not hasattr(self, self._slug_field):
                raise ValueError('Model has no attribute named "%s"' % self._slug_field)
            
            self.slug = slugify(getattr(self, self._slugify_field))

        super().save(*args, **kwargs)