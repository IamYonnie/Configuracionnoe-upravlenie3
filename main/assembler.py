#!/usr/bin/env python3
"""
Ассемблер для УВМ
"""
import os
import sys
import csv
import argparse
from uvm_defs import COMMANDS, SPEC_TESTS, encode_command, print_intermediate_representation


def parse_csv_program(csv_path):
    #Чтение программы из CSV файла.
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
    #Возвращает список словарей с полями A, B, C (если есть)
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


def assemble_to_binary(ir, output_path):
    #Преобразует промежуточное представление (IR) в машинный код и записывает в бинарный файл.
    all_bytes = []
    for cmd_data in ir:
        cmd_name = cmd_data['name']
        fields = cmd_data['fields']
        encoded = encode_command(cmd_name, fields)
        all_bytes.extend(encoded)
        print(f"  {cmd_name}: {[hex(b) for b in encoded]}")

    # Создаем папку если её нет
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  Создана папка: {output_dir}")

    # Записываем в файл
    with open(output_path, 'wb') as f:
        f.write(bytearray(all_bytes))

    return all_bytes


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

        # Кодируем и проверяем
        encoded = encode_command(cmd_name, test['args'])
        print(f"  Полученные байты: {[hex(b) for b in encoded]}")
        if encoded == test['expected_bytes']:
            print("Тест пройден")
        else:
            print("Тест не пройден")

    return True


def main():
    parser = argparse.ArgumentParser(description='Ассемблер УВМ (Вариант 3) - Этап 2')
    parser.add_argument('input', help='Путь к CSV файлу с программой')
    parser.add_argument('-o', '--output', required=True, help='Путь для выходного файла (бинарный)')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Режим тестирования: вывести байтовое представление')
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

        # 3. Кодирование в машинный код и запись в файл
        print(f"Ассемблирование {len(ir)} команд...")
        binary_data = assemble_to_binary(ir, args.output)

        # 4. Вывод статистики
        print(f"\nРезультат:")
        print(f"  Число команд: {len(ir)}")
        print(f"  Размер файла: {len(binary_data)} байт")

        # 5. Вывод байтов в тестовом режиме
        if args.test:
            print("\nБайтовое представление:")
            for i, byte in enumerate(binary_data):
                print(f"  {i:3d}: {hex(byte)}")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()