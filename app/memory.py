class ConversationMemory:

    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages

    def add_user(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message,
        })

        self._trim()

    def add_assistant(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message,
        })

        self._trim()

    def get_messages(self):
        return self.messages.copy()

    def clear(self):
        self.messages.clear()

    def _trim(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]