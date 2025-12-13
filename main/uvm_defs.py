"""
Спецификация учебной виртуальной машины (УВМ) для Варианта №3
"""

class UVMCommand:
    def __init__(self, name, opcode, field_bits, size_bytes):
        self.name = name            # Имя команды
        self.opcode = opcode        # Код операции
        self.field_bits = field_bits  # Биты полей: {'A': (0,6), 'B': (7,22), ...}
        self.size_bytes = size_bytes  # Размер в байтах

# Команды УВМ для Варианта №3
COMMANDS = {
    'load': UVMCommand('load', 104, {'A': (0,6), 'B': (7,22)}, 3),
    'read': UVMCommand('read', 4, {'A': (0,6)}, 1),
    'store': UVMCommand('store', 110, {'A': (0,6), 'B': (7,38)}, 5),
    'cmp_ge': UVMCommand('cmp_ge', 74, {'A': (0,6), 'B': (7,38)}, 5)
}

# Тесты из спецификации УВМ
SPEC_TESTS = [
    # Тест загрузки константы: A=104, B=787
    {'cmd': 'load', 'args': {'B': 787}, 'expected_bytes': [0xE8, 0x89, 0x01]},
    # Тест чтения из памяти: A=4
    {'cmd': 'read', 'args': {}, 'expected_bytes': [0x84]},
    # Тест записи в память: A=110, B=860
    {'cmd': 'store', 'args': {'B': 860}, 'expected_bytes': [0x6E, 0xAE, 0x01, 0x00, 0x00]},
    # Тест сравнения >=: A=74, B=670
    {'cmd': 'cmp_ge', 'args': {'B': 670}, 'expected_bytes': [0x4A, 0x4F, 0x81, 0x80, 0x00]}
]

def print_intermediate_representation(ir):
    """Вывод промежуточного представления в формате полей и значений"""
    for cmd_data in ir:
        print(f"Команда: {cmd_data['name']}")
        print(f"  Opcode: {cmd_data['opcode']}")
        for field, value in cmd_data['fields'].items():
            print(f"  {field}: {value}")
        print()