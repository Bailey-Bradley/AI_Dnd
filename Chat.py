import openai
from openai import OpenAI

_client = OpenAI()

class ChatSession:
    def __init__(self, system_message: str = None, tools: list[dict] = [], model: str = "gpt-5-nano"):
        self._chat_history: list[dict] = []
        self._tools: list[dict] = tools
        self._model: str = model

        if system_message is not None:
            self._chat_history.append({
                "role": "system",
                "content": system_message
            })

    def sendMessage(self, message_text: str, role: str ="user"):

        message = {
            "role": role,
            "content": message_text
        }

        response = _client.responses.create(
            model= self._model,
            input= self._chat_history + [message],
            tools= self._tools
        )

        self._chat_history.append(message)

        response_message = {
            "role": "assistant",
            "content": response.output_text
        }

        self._chat_history.append(response_message)

        return response

    def addTool(self, tool: dict) -> None:
        self._tools.append(tool)

    def removeTool(self, tool: dict) -> None:
        self._tools.remove(tool)


def extractToolCalls(self, message):
    pass


if __name__ == '__main__':

    chat = ChatSession()

    while True:
        print("==> ", end='')
        message = input()

        response = chat.sendMessage(message)
        print(response.output_text)