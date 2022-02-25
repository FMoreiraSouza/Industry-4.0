from mongoengine import Document, DateTimeField, EmbeddedDocument, ListField, EmbeddedDocumentField, DynamicField, DictField

class TagsValuesModel(Document):
    timestamp = DateTimeField()
    read = DictField(DynamicField())
    predicted = DictField(DynamicField())

    meta = {
        'collection': 'tags_values',
        'indexes': ['timestamp']
    }
