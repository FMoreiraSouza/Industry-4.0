from mongoengine import Document, StringField, EmbeddedDocumentField, ListField, EmbeddedDocument, EnumField, \
    BooleanField, IntField

from modules.enums import State


class TagModel(EmbeddedDocument):
    tag_name = StringField(required=True)
    tag_id = StringField(required=True)
    tag_system = StringField(required=True)
    tag_mv = BooleanField(default=False)
    tag_const = BooleanField(default=False)
    tag_status = BooleanField(default=False)
    tag_active = BooleanField(default=False)
    low_value = IntField(default=0)
    high_value = IntField(default=0)
    max_increase = IntField(default=0)
    max_decrease = IntField(default=0)
    low_suggestion = IntField(default=0)
    high_suggestion = IntField(default=0)
    suggest_increase = IntField(default=0)
    suggest_decrease = IntField(default=0)
    trend = IntField(default=0)
    expec_value = IntField(default=0)
    tag_description = StringField(default="")

class TagsModel(Document):
    server = StringField(required=True, unique=True)
    tags = ListField(EmbeddedDocumentField(TagModel))

    meta = {
        'collection': 'tags',
        'indexes': [
            '*tags.tag_id',
        ]
    }
