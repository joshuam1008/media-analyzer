from langdetect import detect


class LangModule:
    """An object used to determine the language of given content."""

    @classmethod
    def generate_result(cls, content=None):
        """Returns language of given content."""
        try:
            result = detect(content)
            print(result)
        except Exception:
            result = "error"  # language not detected
        return result
