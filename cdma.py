import numpy as np

codes = {
    "A": [-1, -1, -1, +1, +1, -1, +1, +1],
    "B": [-1, -1, +1, -1, +1, +1, +1, -1],
    "C": [-1, +1, -1, +1, +1, +1, -1, -1],
    "D": [-1, +1, -1, -1, -1, -1, +1, -1],
}

messages = {
    "A": "GOD",
    "B": "CAT",
    "C": "HAM",
    "D": "SUN",
}


def message_to_signs(message: str) -> list[int]:
    """Преобразует сообщение в знаки (+1 и -1), используя двоичный код ASCII.

    Args:
        message (str): Сообщение для кодирования.

    Returns:
        list[int]: Список из +1 и -1, представляющих двоичный код сообщения.
    """
    signs: list[int] = []
    for char in message:
        ascii_code = ord(char)
        binary_representation = format(ascii_code, "08b")
        for bit in binary_representation:
            signs.append(+1 if bit == "1" else -1)
    return signs


def spread_symbols(signs: list[int], code: list[int]) -> list[int]:
    """Передает сообщение, распространяя символы на основании знаков и кода станции.

    Args:
        signs (list[int]): Список знаков (+1 и -1), представляющих сообщение.
        code (list[int]): Код базовой станции.

    Returns:
        list[int]: Распространенный сигнал (последовательность символов, умноженных на код).
    """
    spread_signal = []
    for sign in signs:
        spread = [sign * c for c in code]
        spread_signal.extend(spread)
    return spread_signal


def despread_signal(combined_signal: list[int], code: list[int]) -> list[int]:
    """Восстанавливает сигнал для определенной станции из общего сигнала.

    Args:
        combined_signal (list[int]): Суммарный сигнал, переданный всеми станциями.
        code (list[int]): Код базовой станции для восстановления.

    Returns:
        list[int]: Оцененные символы для восстановления исходного сообщения.
    """
    code_length = len(code)
    num_symbols = len(combined_signal) // code_length
    estimated_symbols = []
    for i in range(num_symbols):
        segment = combined_signal[i * code_length : (i + 1) * code_length]
        product = np.multiply(segment, code)
        symbol = sum(product)
        estimated_symbols.append(symbol)
    return estimated_symbols


def symbols_to_message(symbols: list[int]) -> str:
    """Преобразует оцененные символы в сообщение (строку).

    Args:
        symbols (list[int]): Список оцененных символов.

    Returns:
        str: Восстановленное сообщение.
    """
    binary_message = ""
    for symbol in symbols:
        binary_message += "1" if symbol > 0 else "0"

    chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i : i + 8]
        ascii_code = int(byte, 2)
        chars.append(chr(ascii_code))

    return "".join(chars)


spread_signals = {}

for base_station, message in messages.items():
    print(f"Исходное сообщение для станции {base_station}: '{message}'")
    signs = message_to_signs(message)
    code = codes[base_station]
    spread_signal = spread_symbols(signs, code)
    spread_signals[base_station] = spread_signal

print("Передача сообщений по общему каналу...")
combined_signal = np.sum(list(spread_signals.values()), axis=0)

for base_station in messages:
    code = codes[base_station]
    symbols = despread_signal(combined_signal, code)
    recovered_message = symbols_to_message(symbols)
    print(
        f"Восстановленное сообщение для станции {base_station}: '{recovered_message}'"
    )
