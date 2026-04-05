#Разные способы форматирования текста (Markdown, HTML, Plain)
from abc import ABC, abstractmethod


class TextFormatter(ABC):
    @abstractmethod
    def format(self, text: str) -> str:
        pass


class MarkdownFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return f"**{text}**"


class HTMLFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return f"<strong>{text}</strong>"


class PlainFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return text


class TextEditor:
    def __init__(self, formatter: TextFormatter):
        self.formatter = formatter

    def set_formatter(self, formatter: TextFormatter):
        self.formatter = formatter

    def publish(self, text: str):
        formatted = self.formatter.format(text)
        print(f"Output: {formatted}")


if __name__ == "__main__":
    editor = TextEditor(MarkdownFormatter())
    editor.publish("Hello World")

    editor.set_formatter(HTMLFormatter())
    editor.publish("Hello World")