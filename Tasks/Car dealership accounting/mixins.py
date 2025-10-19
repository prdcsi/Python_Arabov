import logging

class LoggingMixin:
    def log_action(self, message: str):
        logging.info(message)


class NotificationMixin:
    def send_notification(self, message: str):
        print(f"[Уведомление] {message}")