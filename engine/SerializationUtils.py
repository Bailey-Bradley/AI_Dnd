def dictPreSerialize(dictn: dict):
    return list(dictn.items())

def dictPostDeserialize(dictn: list):
    return dict(dictn)

def callablePreSerialize(func: callable):
    pass

def callablePostDeserialize(func: callable):
    pass