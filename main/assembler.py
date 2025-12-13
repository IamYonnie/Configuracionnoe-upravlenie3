#!/usr/bin/env python3
"""
Ассемблер для УВМ (Вариант №3) - Этап 1
Промежуточное представление из CSV формата
"""

import sys
import csv
import argparse
from uvm_defs import COMMANDS, SPEC_TESTS, print_intermediate_representation


def parse_csv_program(csv_path):
    """
    Чтение программы из CSV файла.
    Формат CSV: команда,аргумент1,аргумент2,...
    Пример: load,787
    """
    ir = []  # промежуточное представление

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith('#'):  # пропуск комментариев
                continue

            cmd_name = row[0].strip().lower()
            if cmd_name not in COMMANDS:
                raise ValueError(f"Неизвестная команда: {cmd_name}")

            cmd = COMMANDS[cmd_name]
            fields = {}

            # Парсинг аргументов в зависимости от команды
            if cmd_name == 'load':
                if len(row) > 1:
                    fields['B'] = int(row[1].strip())
            elif cmd_name == 'read':
                # Без аргументов
                pass
            elif cmd_name in ['store', 'cmp_ge']:
                if len(row) > 1:
                    fields['B'] = int(row[1].strip())

            ir.append({
                'name': cmd_name,
                'opcode': cmd.opcode,
                'fields': fields,
                'size_bytes': cmd.size_bytes,
                'field_bits': cmd.field_bits
            })

    return ir


def generate_intermediate_representation(ir):
    """
    Генерация промежуточного представления
    Возвращает список словарей с полями A, B, C (если есть)
    """
    intermediate = []

    for cmd_data in ir:
        cmd_name = cmd_data['name']
        cmd = COMMANDS[cmd_name]
        fields = cmd_data['fields']

        # Создаем структуру полей A, B, C...
        ir_fields = {'A': cmd.opcode}

        # Заполняем поля согласно спецификации
        if 'B' in fields:
            ir_fields['B'] = fields['B']

        intermediate.append({
            'command': cmd_name,
            'fields': ir_fields,
            'size': cmd.size_bytes
        })

    return intermediate


def run_spec_tests():
    """Запуск тестов из спецификации УВМ"""
    print("=== Тесты из спецификации УВМ ===")

    for test in SPEC_TESTS:
        cmd_name = test['cmd']
        cmd = COMMANDS[cmd_name]

        # Создаем промежуточное представление для теста
        ir_item = {
            'name': cmd_name,
            'opcode': cmd.opcode,
            'fields': test['args'],
            'size_bytes': cmd.size_bytes,
            'field_bits': cmd.field_bits
        }

        print(f"\nТест: {cmd_name}")
        print(f"  Поля: A={cmd.opcode}, ", end="")
        for field, value in test['args'].items():
            print(f"{field}={value}, ", end="")
        print(f"\n  Ожидаемые байты: {[hex(b) for b in test['expected_bytes']]}")

    return True


def main():
    parser = argparse.ArgumentParser(description='Ассемблер УВМ (Вариант 3) - Этап 1')
    parser.add_argument('input', help='Путь к CSV файлу с программой')
    parser.add_argument('-o', '--output', help='Путь для выходного файла (бинарный)')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Режим тестирования: вывести промежуточное представление')
    parser.add_argument('--spec-tests', action='store_true',
                        help='Запустить тесты из спецификации УВМ')

    args = parser.parse_args()

    if args.spec_tests:
        run_spec_tests()
        return

    try:
        # 1. Чтение и парсинг CSV программы
        ir = parse_csv_program(args.input)

        # 2. Генерация промежуточного представления
        intermediate = generate_intermediate_representation(ir)

        # 3. Вывод в режиме тестирования
        if args.test:
            print("=== Промежуточное представление ===")
            for item in intermediate:
                print(f"Команда: {item['command']}")
                for field, value in item['fields'].items():
                    print(f"  {field}: {value} (0x{value:X})")
                print(f"  Размер: {item['size']} байт")
                print()

        # 4. Сохранение в файл (для следующих этапов)
        if args.output:
            import pickle
            with open(args.output, 'wb') as f:
                pickle.dump({
                    'ir': ir,
                    'intermediate': intermediate
                }, f)
            print(f"Промежуточное представление сохранено в {args.output}")

        print(f"Успешно ассемблировано {len(ir)} команд")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()