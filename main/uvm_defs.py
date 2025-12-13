"""
Спецификация учебной виртуальной машины (УВМ)
"""

class UVMCommand:
    def __init__(self, name, opcode, field_bits, size_bytes):
        self.name = name            # Имя команды
        self.opcode = opcode        # Код операции
        self.field_bits = field_bits  # Биты полей: {'A': (0,6), 'B': (7,22), ...}
        self.size_bytes = size_bytes  # Размер в байтах

# Команды УВМ
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
def encode_command(cmd_name, fields):
    #Кодирование команды в байты согласно битовой раскладке.
    #Возвращает список байтов.
    if cmd_name not in COMMANDS:
        raise ValueError(f"Неизвестная команда: {cmd_name}")

    cmd = COMMANDS[cmd_name]
    total_bits = cmd.size_bytes * 8
    bit_array = [0] * total_bits

    # Устанавливаем поле A (opcode)
    a_bits = cmd.field_bits['A']
    a_value = cmd.opcode
    _set_bits(bit_array, a_bits[0], a_bits[1], a_value)

    # Устанавливаем остальные поля
    if cmd_name == 'load':
        b_value = fields.get('B', 0)
        b_bits = cmd.field_bits['B']
        _set_bits(bit_array, b_bits[0], b_bits[1], b_value)

    elif cmd_name == 'store':
        b_value = fields.get('B', 0)
        b_bits = cmd.field_bits['B']
        _set_bits(bit_array, b_bits[0], b_bits[1], b_value)

    elif cmd_name == 'cmp_ge':
        b_value = fields.get('B', 0)
        b_bits = cmd.field_bits['B']
        _set_bits(bit_array, b_bits[0], b_bits[1], b_value)

    # Чтение из памяти (read) не имеет полей кроме A

    # Преобразуем биты в байты
    return _bits_to_bytes(bit_array)


def _set_bits(bit_array, start, end, value):
    #Устанавливает биты в массиве bit_array с позиции start до end (включительно).
    for i in range(start, end + 1):
        if i >= len(bit_array):
            raise IndexError(f"Бит {i} выходит за пределы массива")
        bit_value = (value >> (i - start)) & 1
        bit_array[i] = bit_value


def _bits_to_bytes(bit_array):
    byte_count = len(bit_array) // 8
    bytes_list = []
    for byte_idx in range(byte_count):
        byte_val = 0
        for bit_idx in range(8):
            pos = byte_idx * 8 + (7 - bit_idx)
            byte_val |= (bit_array[pos] << (7 - bit_idx))
        bytes_list.append(byte_val)
    return bytes_list