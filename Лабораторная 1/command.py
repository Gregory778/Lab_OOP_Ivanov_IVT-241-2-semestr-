# Операции с файлами с поддержкой отмены
from abc import ABC, abstractmethod
import os
import shutil


class FileCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class CreateFileCommand(FileCommand):
    def __init__(self, filepath: str, content: str = ""):
        self.filepath = filepath
        self.content = content

    def execute(self):
        with open(self.filepath, 'w') as f:
            f.write(self.content)
        print(f"Создан файл: {self.filepath}")

    def undo(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            print(f"Удалён файл: {self.filepath}")


class DeleteFileCommand(FileCommand):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.backup_content = None

    def execute(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                self.backup_content = f.read()
            os.remove(self.filepath)
            print(f"Удалён файл: {self.filepath}")

    def undo(self):
        if self.backup_content is not None:
            with open(self.filepath, 'w') as f:
                f.write(self.backup_content)
            print(f"Восстановлен файл: {self.filepath}")


class RenameFileCommand(FileCommand):
    def __init__(self, old_path: str, new_path: str):
        self.old_path = old_path
        self.new_path = new_path

    def execute(self):
        if os.path.exists(self.old_path):
            shutil.move(self.old_path, self.new_path)
            print(f"Переименован: {self.old_path} -> {self.new_path}")

    def undo(self):
        if os.path.exists(self.new_path):
            shutil.move(self.new_path, self.old_path)
            print(f"Отмена: {self.new_path} -> {self.old_path}")


class WriteFileCommand(FileCommand):
    def __init__(self, filepath: str, new_content: str):
        self.filepath = filepath
        self.new_content = new_content
        self.old_content = None

    def execute(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                self.old_content = f.read()
        with open(self.filepath, 'w') as f:
            f.write(self.new_content)
        print(f"Записано в файл: {self.filepath}")

    def undo(self):
        if self.old_content is not None:
            with open(self.filepath, 'w') as f:
                f.write(self.old_content)
            print(f"Восстановлено содержимое: {self.filepath}")


class CommandManager:
    def __init__(self):
        self.history = []

    def execute(self, command: FileCommand):
        command.execute()
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("Нечего отменять")


if __name__ == "__main__":
    manager = CommandManager()
    test_file = "test.txt"

    # Создаём файл
    manager.execute(CreateFileCommand(test_file, "Hello World"))

    # Записываем новое содержимое
    manager.execute(WriteFileCommand(test_file, "New content"))

    # Отменяем запись
    print("\n=== Отмена записи ===")
    manager.undo()

    # Переименовываем
    manager.execute(RenameFileCommand(test_file, "renamed.txt"))

    # Удаляем
    manager.execute(DeleteFileCommand("renamed.txt"))

    # Отменяем удаление
    print("\n=== Отмена удаления ===")
    manager.undo()

    # Очистка
    if os.path.exists("renamed.txt"):
        os.remove("renamed.txt")