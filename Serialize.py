import jsonpickle
import Log

from collections.abc import Iterable


class Serializable:

    def postDeserialize(self):
        pass


def serialize(obj: Serializable) -> str:
    return jsonpickle.encode(obj)

def deserialize(encoded_obj: str) -> Serializable:
    return jsonpickle.decode(encoded_obj)

def save(obj: Serializable, file_name: str):
    try:
        with open(file_name,'w') as file:
            file.write(serialize(obj))
    except:
        Log.log(f"Failed to serialize object to file '{file_name}'", Log.LogLevel.WARNING)

def _isReferencedIn(obj: object, iterable: Iterable):
    for element in iterable:
        if id(element) == id(obj):
            return True

    return False

def _getObjectsInTree(obj: object, seen: list[object] = None) -> list[object]:

    if seen is None:
        seen = []

    if _isReferencedIn(obj, seen) or getattr(obj, "__dict__", None) is None:
        return seen

    seen.append(obj)

    for attr_val in vars(obj).values():

        if isinstance(attr_val, (list, tuple, set)):
            for element in attr_val:
                _getObjectsInTree(element, seen)

        elif isinstance(attr_val, dict):
            for value in attr_val.values():
                _getObjectsInTree(value, seen)

        else:
            _getObjectsInTree(attr_val, seen)
    
    return seen

def _getPostDeserializable(obj: Serializable) -> list[Serializable]:
    connected_objects = _getObjectsInTree(obj)

    postDeserializeable = []

    for obj in connected_objects:
        if getattr(obj, "postDeserialize", None) is not None:
            postDeserializeable.append(obj)

    return postDeserializeable

def load(file_name: str) -> Serializable | None:
    try:
        with open(file_name, 'r') as file:
            obj = deserialize(file.read())
            postDeserializable = _getPostDeserializable(obj)

            for element in postDeserializable:
                element.postDeserialize()

            return obj
    except:
        Log.log(f"Failed to deserialize object from file '{file_name}'", Log.LogLevel.WARNING)