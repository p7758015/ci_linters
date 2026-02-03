# CI + линтеры для Python-проекта

Учебный репозиторий, в котором я настроил полный набор инструментов качества кода и CI для Python-проекта.

## Что сделано

- Настроены линтеры и форматтеры:
  - flake8 — стиль кода и базовые ошибки.
  - black — автоформатирование.
  - isort — сортировка импортов.
  - mypy — статическая типизация.
- Написаны и поправлены unit-тесты под pytest.
- Настроен CI в GitHub Actions:
  - установка зависимостей из `requirements.txt`;
  - запуск flake8, black, isort, mypy и pytest на каждый push/pull request в ветку `main`;
  - сбор отчетов о прохождении шагов.

## Технологии

- Python 3.11
- pytest
- flake8
- black
- isort
- mypy
- GitHub Actions (`.github/workflows/`)

## Как запустить проверки локально

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Линтеры и форматирование
flake8 homework
black homework
isort homework

# Статическая типизация
mypy homework

# Тесты
pytest


На основе этого репозитория я могу:

подключить линтеры и форматирование к любому Python-проекту;

настроить GitHub Actions (или GitLab CI) под конкретный стек;

починить типизацию и тесты так, чтобы пайплайн проходил без ошибок;

оставить понятную инструкцию по запуску проверок для команды.
