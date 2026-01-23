import jsonpickle
from jsonpickle.handlers import BaseHandler


class EventBus:
    def __init__(self):
        self._handlers: dict[int, list[callable]] = {}

    def subscribe(self, event_type: int, handler: callable) -> None:
        handlers = self._handlers.get(event_type)

        if handlers is not None:
            handlers.append(handler)
        else:
            self._handlers[event_type] = [handler]

    def unsubscribe(self, event_type: int, handler: callable) -> None:
        handlers = self._handlers.get(event_type)

        if handlers is not None:
            handlers.remove(handler)

    def emit(self, event_type: int, event) -> None:
        handlers = self._handlers.get(event_type)

        if handlers is not None:
            for handler in handlers:
                handler(event)