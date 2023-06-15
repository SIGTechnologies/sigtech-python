import re


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def singlar(name):
    if name == "status":
        pass
    elif name.endswith('s'):
        name = name[:-1]
    return name.title()


def snake_to_camel(name):
    words = [word.title() for word in name.split('_')]
    words[0] = words[0].lower()
    return ''.join(words)
