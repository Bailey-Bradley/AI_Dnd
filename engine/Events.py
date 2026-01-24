from engine.Serialize import Serializable


class EventBus(Serializable):
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

    def __getstate__(self):
        state = {}
        state["state"] = self.__dict__
        serial_handlers_dict: dict[str, list[(object, str)]] = {}

        for event_id, handler_list in self._handlers.items():
            serial_handler_list = []

            for event_handler in handler_list:
                bound_object = event_handler.__self__
                handler_name = event_handler.__qualname__.split('.')[1]

                serial_handler_list.append((bound_object, handler_name))

            serial_handlers_dict[str(event_id)] = serial_handler_list

        state["serial_handlers"] = serial_handlers_dict

        return state

    def __setstate__(self, state):
        self.__dict__ = state["state"]

        self._handlers = {}

        for event_id, serial_handler_list in state["serial_handlers"].items():
            handler_list = []

            for serial_handler in serial_handler_list:
                obj = serial_handler[0]
                method = getattr(obj, serial_handler[1])
                handler_list.append(method)

            self._handlers[int(event_id)] = handler_list