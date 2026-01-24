from Container import ReadOnlyList

class ObjectHierarchy:
    def __init__(self):
        self._objects: list[object] = []
        self._hierarchy: dict[object, list[object]] = {}

    def getObjects(self):
        return ReadOnlyList(self._objects)

    def getParent(self, obj):
        for parent, children in self._hierarchy:
            for child in children:
                if child is obj:
                    return parent

    def getChildren(self, obj):
        return self._hierarchy.get(obj)

    def addChild(self, parent, child):
        children = self._hierarchy.get(parent)

        if children is not None:
            children.append(child)
        else:
            self._hierarchy[parent] = [child]

    def addObject(self, obj):
        self._objects.append(obj)

    def removeObject(self, obj):
        self._objects.remove(obj)

        children = self._hierarchy.get(obj)

        if children is not None:
            while len(children) > 0:
                new_children = []

                for child in children:
                    self._objects.remove(child)
                    
                    child_children = self._hierarchy.get(child)

                    if child_children is not None:
                        new_children += child_children

                children = new_children
