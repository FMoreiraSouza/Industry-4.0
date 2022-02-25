from mongoengine import Document, DateTimeField, DictField, DynamicField

class TagsValuesModel(Document):
    timestamp = DateTimeField()
    read = DictField(DynamicField())
    predicted = DictField(DynamicField())

    meta = {
        'collection': 'tags_values',
        'indexes': ['timestamp']
    }

