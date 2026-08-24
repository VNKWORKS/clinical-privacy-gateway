class MockLLMClient:
    def __init__(self):
        self.received_texts: list[str] = []

    def generate(self, text: str) -> str:
        self.received_texts.append(text)

        return (
            "Clinical summary: "
            + text
        )
