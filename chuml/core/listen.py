_pattern = """
on_node_{name} = []

def on_node_{name}(func):
    on_node_{name}.append(func)
    return func
"""

exec(_pattern.format(name="created"))
exec(_pattern.format(name="viewed"))
exec(_pattern.format(name="edited"))
exec(_pattern.format(name="removed"))
