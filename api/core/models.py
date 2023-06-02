import logging

from django.db import models
from django.db.models.functions import Length

from rest_framework.utils import model_meta


logger = logging.getLogger(__name__)


class CreateUpdateMixin(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True

class BaseModel(CreateUpdateMixin):
    class Meta:
        abstract = True

    def _set_data(self, data: dict) -> None:
        info = model_meta.get_field_info(self)

        m2m_fields_reverse = []
        m2m_fields = []
        for attr, value in data.items():
            if attr in info.relations and info.relations[attr].to_many:
                if info.relations[attr].reverse:
                    m2m_fields_reverse.append((attr, value))
                else:
                    m2m_fields.append((attr, value))
            else:
                setattr(self, attr, value)

        for attr, value in m2m_fields_reverse:
            field = getattr(self, attr)
            field.set(value, bulk=False)

        for attr, value in m2m_fields:
            field = getattr(self, attr)
            field.set(value)
