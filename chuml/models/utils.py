from chuml.utils.db import Column, Integer, ForeignKey, relationship

def snakized(name):
    snakized = [name[0].lower()]
    for char in name[1:]:
        snakized.append(char.lower())
        if char.isupper():
            snakized.append("_")
    return "".join(snakized)

def gen_attributes(locals, attributes):
    for key, model in attributes.items():
        print(f"k: {key} v: {model}")
        print(f"k: {type(key)} v: {type(model)}")
        locals[key+"_id"] = Column(Integer, ForeignKey(model.__tablename__+".id"))
        locals[key] = relationship(model.__name__, foreign_keys=[locals[key+"_id"]])

    locals["attributes"] = attributes


def with_arg(arg_name, arg_type=None, required=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            arg = request.args.get(arg_name)
            if arg is None:
                if required:
                    return f"argument <i>{arg_name}</i> required"
            elif arg_type is not None:
                try:
                    arg = arg_type(arg)
                except ValueError:
                    return f"argument <i>{arg_name}</i> must be {arg_type}"

            return f(*args, {**kwargs, arg_name: arg})

        return wrapper


def with_node(arg_name, node_type, request=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            id = request.args.get(arg_name)
            if id is None:
                if required:
                    return f"argument <i>{arg_name}</i> required"
            else:
                try:
                    id = int(id)
                except ValueError:
                    return f"argument <i>{arg_name}</i> must be integer"

                node = db.query(node_type).get(id)
                if node is None:
                    return f"node {id} not found"

            return f(*args, {**kwargs, arg_name: node})

        return wrapper
