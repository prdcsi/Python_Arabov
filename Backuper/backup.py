import os
import zipfile
import logging
from datetime import datetime
import sys

# Настройка логгера
logging.basicConfig(
    filename='backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def get_user_input():
    """Запрашивает у пользователя пути к исходной папке и папке назначения."""
    source = input("Введите путь к исходной папке: ").strip()
    destination = input("Введите путь для сохранения архива: ").strip()
    return source, destination

def validate_paths(source, destination):
    """Проверяет существование исходной папки и доступность папки назначения."""
    if not os.path.exists(source):
        raise FileNotFoundError(f"Исходная папка не найдена: {source}")
    if not os.path.isdir(source):
        raise NotADirectoryError(f"Указанный путь не является папкой: {source}")
    if not os.path.exists(destination):
        os.makedirs(destination)
        logging.info(f"Создана папка назначения: {destination}")

def create_zip_archive(source, destination):
    """Создаёт ZIP-архив с сохранением структуры папок."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.zip"
    archive_path = os.path.join(destination, archive_name)

    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Сохраняем относительный путь от source
                    arcname = os.path.relpath(file_path, source)
                    zipf.write(file_path, arcname)
                    logging.info(f"Добавлен файл: {arcname}")
        logging.info(f"Архив успешно создан: {archive_path}")
        print(f"✅ Резервная копия успешно создана: {archive_path}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при создании архива: {e}")
        print(f"❌ Ошибка: {e}")
        return False

def main():
    try:
        print("🗃️ Утилита резервного копирования")
        source, destination = get_user_input()
        validate_paths(source, destination)
        create_zip_archive(source, destination)
    except KeyboardInterrupt:
        logging.warning("Операция прервана пользователем.")
        print("\n⚠️ Операция отменена.")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()