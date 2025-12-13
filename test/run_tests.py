#!/usr/bin/env python3
"""
Самый простой тест - минимальный код
"""

import sys
import os
from pathlib import Path

# Переходим в папку src
src_dir = Path(__file__).parent.parent / "main"
os.chdir(src_dir)

# Добавляем текущую папку в путь
sys.path.insert(0, str(src_dir))

# Проверяем файлы
print("Проверка файлов в папке main:")
for file in os.listdir('.'):
    if file.endswith('.py'):
        print(f"{file}")

# Исправляем CSV
csv_path = "../test/test_commands.csv"
if os.path.exists(csv_path):
    with open(csv_path, 'r') as f:
        content = f.read()

    if ';' in content:
        print("\nИсправление CSV...")
        content = content.replace(';', ',')
        with open(csv_path, 'w') as f:
            f.write(content)

# Запускаем ассемблер
print("\nЗапуск ассемблера...")
print("=" * 40)

sys.argv = ['assembler.py', csv_path, '-t']

try:
    with open('assembler.py', 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code)
    print("\nУспешно!")
except Exception as e:
    print(f"\nОшибка: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)