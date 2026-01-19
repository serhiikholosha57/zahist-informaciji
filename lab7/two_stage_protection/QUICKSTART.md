# Швидкий старт

## Крок 1: Встановлення

```bash
cd two_stage_protection
pip install -r requirements.txt --break-system-packages
```

## Крок 2: Створення тестових файлів

```bash
python create_test_files.py
```

## Крок 3: Запуск повного тестування

```bash
python main.py test test_secret.txt test_cover.png MyPassword123
```

Ви побачите:
- Процес шифрування та стеганографії
- Процес відновлення даних
- Перевірку цілісності
- Детальний звіт з метриками

Звіт буде збережено у файл `report.txt`

## Крок 4: Демонстрація безпеки

```bash
python demo_security.py demo_stego.png MyPassword123
```

Показує, що для доступу потрібні обидва етапи.

## Основні команди

### Захист файлу
```bash
python main.py protect <файл> <зображення> <вихід> <пароль>
```

### Відновлення файлу
```bash
python main.py recover <стего_зображення> <вихідний_файл> <пароль>
```

### Повне тестування
```bash
python main.py test <файл> <зображення> <пароль>
```

## Приклад реального використання

```bash
# 1. Створіть своє зображення-контейнер (PNG, мінімум 200x200)
# 2. Підготуйте файл для захисту
# 3. Виконайте захист
python main.py protect mydocument.txt myimage.png secret_image.png StrongPassword123

# 4. Передайте secret_image.png (виглядає як звичайне зображення!)
# 5. Для відновлення потрібен пароль
python main.py recover secret_image.png restored_document.txt StrongPassword123
```

## Що далі?

- Прочитайте `README.md` для детальної документації
- Перегляньте `TECHNICAL.md` для розуміння реалізації
- Використовуйте `DEMO.md` для демонстрації можливостей

## Вимоги

- Python 3.7+
- cryptography >= 41.0.7
- pillow >= 10.1.0
- numpy >= 1.24.3
