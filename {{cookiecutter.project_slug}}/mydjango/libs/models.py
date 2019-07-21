from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, Model


class BaseModelManager(Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_by_id(self, id_):
        return self.get_or_none(pk=id_)


class BaseModel(Model):

    class Meta:
        abstract = True

    JSON_FIELDS = {'id'}
    objects = BaseModelManager()

    @classmethod
    def get_or_none(cls, **kwargs):
        return cls.objects.get_or_none(**kwargs)

    @classmethod
    def get_by_id(cls, id_):
        return cls.get_or_none(pk=id_)

    def update(self, **kwargs):
        for field, val in kwargs.items():
            setattr(self, field, val)
        self.save()

    def json(self, fields=None):
        if not fields:
            fields = self.JSON_FIELDS

        json_dict = {}
        for field in fields:
            json_dict[field] = val = getattr(self, field)
            type_name = type(val).__name__
            if type_name in ['RelatedManager', 'ManyRelatedManager']:
                json_dict[field] = [v.json() for v in val.all()]
            elif isinstance(val, BaseModel):
                json_dict[field] = val.json()
            elif hasattr(val, 'json'):
                json_dict[field] = val.json()

        return json_dict
