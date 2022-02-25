import json

"""Structure for serialization"""

def json_serializer(data):
    return json.dumps(data).encode("utf-8")
