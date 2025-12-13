"""
Тест ассемблера УВМ
"""

import sys
import os
from pathlib import Path

# Переходим в папку src
src_dir = Path(__file__).parent.parent / "main"
os.chdir(src_dir)

# Добавляем текущую папку в путь
sys.path.insert(0, str(src_dir))

print("=== Запуск теста ассемблера ===")
print(f"Рабочая папка: {os.getcwd()}")
print()

# Проверяем файлы
print("Проверка файлов:")
for file in ['assembler.py', 'uvm_defs.py']:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - не найден")
        sys.exit(1)

# Проверяем тестовый CSV
csv_path = "../test/test_commands.csv"
if not os.path.exists(csv_path):
    # Создаем тестовый CSV если нет
    print(f"\nСоздание тестового файла: {csv_path}")
    test_csv_content = """load,787
read
store,860
cmp_ge,670"""

    os.makedirs(Path(csv_path).parent, exist_ok=True)
    with open(csv_path, 'w') as f:
        f.write(test_csv_content)
    print("Тестовый CSV создан")
else:
    print(f"\nТестовый CSV найден: {csv_path}")

# Запускаем ассемблер в режиме тестирования
print("\n" + "=" * 50)
print("Запуск ассемблера...")
print("=" * 50)

# Имитируем вызов командной строки
sys.argv = ['assembler.py', csv_path, '-o', '../bin/program.bin', '-t']

try:
    # Импортируем и запускаем main
    from assembler import main

    main()
    print("\n" + "=" * 50)
    print("Тест выполнен успешно!")

except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("\nПроверьте структуру модулей:")
    print("1. В файле assembler.py должна быть функция main()")
    print("2. В файле assembler.py должен быть импорт: from uvm_defs import ...")

except Exception as e:
    print(f"\nОшибка при выполнении: {e}")
    import traceback

    traceback.print_exc()
    print("\n" + "=" * 50)
    print("Тест не пройден")

if os.path.exists("../bin/program.bin"):
    size = os.path.getsize("../bin/program.bin")
    print(f"Размер файла: {size} байт")