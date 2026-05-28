class UniversalLanguageAgent:

    def detect_language(self, text):
        return "fr"

    def process(self, text):
        return {
            "language": self.detect_language(text),
            "response": text
        }


language_agent = UniversalLanguageAgent()