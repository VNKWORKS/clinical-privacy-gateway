from presidio_analyzer import AnalyzerEngine


class PHIDetector:
    def __init__(self):
        self.analyzer = AnalyzerEngine()

    def analyze(self, text: str):
        return self.analyzer.analyze(
            text=text,
            language="en",
        )