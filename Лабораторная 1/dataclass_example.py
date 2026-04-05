# Базовый класс для задач с валидацией и статусами
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """Класс задачи"""
    title: str
    description: str
    priority: int
    created_at: datetime
    status: str
    assignee: Optional[str]
    tags: List[str]

    def __post_init__(self):
        if not self.title:
            raise ValueError("Заголовок не может быть пустым")
        if self.priority < 1 or self.priority > 3:
            raise ValueError("Приоритет должен быть 1, 2 или 3")

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "assignee": self.assignee,
            "tags": self.tags
        }


@dataclass
class Project:
    """Класс проекта"""
    name: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_completed_count(self):
        return len([t for t in self.tasks if t.status == "done"])

    def get_completion_rate(self):
        if not self.tasks:
            return 0.0
        return (self.get_completed_count() / len(self.tasks)) * 100


if __name__ == "__main__":
    # Создаём задачи
    task1 = Task(
        title="Написать отчёт",
        description="Подготовить ежемесячный отчёт",
        priority=1,
        created_at=datetime.now(),
        status="done",
        assignee="Иван",
        tags=["важно", "срочно"]
    )

    task2 = Task(
        title="Провести встречу",
        description="Обсудить требования",
        priority=2,
        created_at=datetime.now(),
        status="in_progress",
        assignee="Мария",
        tags=["клиент"]
    )

    task3 = Task(
        title="Обновить документацию",
        description="Дополнить README",
        priority=3,
        created_at=datetime.now(),
        status="new",
        assignee=None,
        tags=[]
    )

    # Создаём проект
    project = Project(name="Внедрение CRM")
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Выводим информацию
    print(f"Проект: {project.name}")
    print(f"Всего задач: {len(project.tasks)}")
    print(f"Выполнено: {project.get_completed_count()}")
    print(f"Готовность: {project.get_completion_rate():.1f}%")

    print("\nДетали первой задачи:")
    print(task1.to_dict())

    # Проверка валидации
    print("\nПроверка валидации:")
    try:
        invalid_task = Task(
            title="",
            description="Тест",
            priority=5,
            created_at=datetime.now(),
            status="new",
            assignee=None,
            tags=[]
        )
    except ValueError as e:
        print(f"Ошибка: {e}")