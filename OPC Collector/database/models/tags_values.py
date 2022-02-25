from mongoengine import Document, DateTimeField, EmbeddedDocument, ListField, EmbeddedDocumentField, DynamicField, \
    DictField, StringField


class TagsValuesModel(Document):
    timestamp = StringField()
    read = DictField(DynamicField())
    predicted = DictField(DynamicField())

    meta = {
        'collection': 'tags_values',
        'indexes': ['timestamp']
    }
