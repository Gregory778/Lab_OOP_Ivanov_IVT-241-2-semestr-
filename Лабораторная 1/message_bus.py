# Рассылка событий между компонентами приложения
from typing import Dict, List, Callable
from datetime import datetime


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        print(f"Подписка: {callback.__name__} на {event_type}")

    def publish(self, event_type: str, data: dict):
        if event_type in self.subscribers:
            print(f"Событие: {event_type} - {data}")
            for callback in self.subscribers[event_type]:
                callback(data)
        else:
            print(f"Нет подписчиков на {event_type}")


# Обработчики событий
def email_notification(data):
    user = data.get('user')
    message = data.get('message')
    print(f"  -> Email отправлен {user}: {message}")


def sms_notification(data):
    user = data.get('user')
    message = data.get('message')
    print(f"  -> SMS отправлена {user}: {message}")


def push_notification(data):
    user = data.get('user')
    message = data.get('message')
    print(f"  -> Push уведомление {user}: {message}")


def audit_log(data):
    action = data.get('action')
    user = data.get('user')
    print(f"  -> Аудит: {user} выполнил {action}")


def analytics_track(data):
    event = data.get('event')
    print(f"  -> Аналитика: событие {event} записано")


if __name__ == "__main__":
    bus = EventBus()

    # Подписываем обработчики
    bus.subscribe("user_registered", email_notification)
    bus.subscribe("user_registered", audit_log)
    bus.subscribe("user_registered", analytics_track)

    bus.subscribe("order_created", sms_notification)
    bus.subscribe("order_created", push_notification)
    bus.subscribe("order_created", analytics_track)

    bus.subscribe("payment_received", email_notification)
    bus.subscribe("payment_received", audit_log)

    # Генерируем события
    print("\n--- Регистрация пользователя ---")
    bus.publish("user_registered", {
        "user": "alice@example.com",
        "action": "register",
        "event": "user_signup"
    })

    print("\n--- Создание заказа ---")
    bus.publish("order_created", {
        "user": "+79123456789",
        "message": "Ваш заказ #1234 создан",
        "event": "order_create"
    })

    print("\n--- Получение оплаты ---")
    bus.publish("payment_received", {
        "user": "alice@example.com",
        "message": "Оплата 1500 руб. получена",
        "action": "payment"
    })