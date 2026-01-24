
# Loading and saving layers
# Loading and saving entire games (GameLayerStacks and chat info i guess?)
# Changing the screen mode (responding to narrator voice, showing image, etc.)
# Playing sound effect
# Playing background music
# Spawning NPCs in
# Messing with player inventory
# Messing with player stats


_handlers: dict[str, list[callable]] = {}

def subscribe(self, tool_name, handler):
    handler_list = self._handlers.get(tool_name)

    if handler_list is not None:
        handler_list.append(handler)

    else:
        self._handlers[tool_name] = [handler]

def unsubscribe(self, tool_name, handler):
    handler_list = self._handlers.get(tool_name)

    if handler_list is not None:
        handler_list.remove(handler)

def emit(self, tool_name):
    handler_list = self._handlers.get(tool_name)

    if handler_list is not None:
        for handler in handler_list:
            handler()