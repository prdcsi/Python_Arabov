import os
import re
import chardet
from collections import Counter

def detect_encoding(file_path):
    """Определяет кодировку файла."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            encoding = 'utf-8'  # fallback
        return encoding

def read_text_file(file_path):
    """Читает текст из файла с автоматическим определением кодировки."""
    encoding = detect_encoding(file_path)
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Если chardet ошибся, пробуем utf-8 и latin-1 как fallback
        for enc in ['utf-8', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError("Не удалось прочитать файл с известными кодировками.")

def analyze_text(text):
    """Анализирует текст и возвращает словарь с метриками."""
    # Общее количество символов
    total_chars_with_spaces = len(text)
    total_chars_without_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))

    # Слова: только буквенно-цифровые последовательности
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = set(words)
    num_unique_words = len(unique_words)

    # Предложения
    sentences = re.split(r'[.!?]+', text)
    # Убираем пустые строки после split
    sentences = [s.strip() for s in sentences if s.strip()]
    total_sentences = len(sentences)

    # Топ-10 слов
    word_counts = Counter(words)
    top_10_words = word_counts.most_common(10)

    return {
        'total_words': total_words,
        'total_chars_with_spaces': total_chars_with_spaces,
        'total_chars_without_spaces': total_chars_without_spaces,
        'total_sentences': total_sentences,
        'unique_words_count': num_unique_words,
        'top_10_words': top_10_words
    }

def generate_report(analysis, original_file):
    """Генерирует текстовый отчёт."""
    report = []
    report.append("📄 Отчёт по анализу текста")
    report.append("=" * 40)
    report.append(f"Исходный файл: {os.path.basename(original_file)}")
    report.append("")
    report.append(f"🔹 Общее количество слов: {analysis['total_words']}")
    report.append(f"🔹 Общее количество символов (с пробелами): {analysis['total_chars_with_spaces']}")
    report.append(f"🔹 Общее количество символов (без пробелов): {analysis['total_chars_without_spaces']}")
    report.append(f"🔹 Количество предложений: {analysis['total_sentences']}")
    report.append(f"🔹 Количество уникальных слов: {analysis['unique_words_count']}")
    report.append("")
    report.append("🔥 Топ-10 самых часто встречающихся слов:")
    for i, (word, count) in enumerate(analysis['top_10_words'], 1):
        report.append(f"  {i}. '{word}' — {count} раз(а)")
    report.append("")
    report.append("Сгенерировано автоматически программой «Анализатор текста».")
    return "\n".join(report)

def save_report(report_text, original_file):
    """Сохраняет отчёт в файл с именем report_<original>.txt"""
    base_name = os.path.splitext(os.path.basename(original_file))[0]
    report_file = f"report_{base_name}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    return report_file

def main():
    print("🔍 Анализатор текста")
    print("-" * 30)
    file_path = input("Введите путь к текстовому файлу: ").strip()

    if not os.path.isfile(file_path):
        print("❌ Файл не найден. Проверьте путь и повторите попытку.")
        return

    try:
        print("⏳ Чтение файла и определение кодировки...")
        text = read_text_file(file_path)

        print("📊 Анализ текста...")
        analysis = analyze_text(text)

        print("📝 Генерация отчёта...")
        report = generate_report(analysis, file_path)

        report_file = save_report(report, file_path)
        print(f"✅ Отчёт успешно сохранён в файл: {report_file}")

    except Exception as e:
        print(f"❌ Ошибка при обработке файла: {e}")

if __name__ == "__main__":
    main()