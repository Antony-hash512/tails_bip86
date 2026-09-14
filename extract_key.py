#!/usr/bin/env python3
import getpass
import sys
from pathlib import Path

# Добавляем соседнюю папку wheels в sys.path для офлайн-импорта библиотек
WHEELS_DIR = Path(__file__).resolve().parent / "wheels"
if not WHEELS_DIR.exists():
    print(f"Ошибка: каталог с зависимостями не найден по пути: {WHEELS_DIR}")
    sys.exit(1)

sys.path.insert(0, str(WHEELS_DIR))

try:
    from bip_utils import (
        Bip39MnemonicValidator,
        Bip39SeedGenerator,
        Bip44Changes,
        Bip86,
        Bip86Coins,
    )
except ImportError as err:
    print(f"Ошибка загрузки библиотек из {WHEELS_DIR}: {err}")
    sys.exit(1)


def parse_indices(input_str: str) -> list[int]:
    """Парсит строки вида '0-5', '3', '0, 2, 5-8' в отсортированный список уникальных int."""
    indices = set()
    parts = [p.strip() for p in input_str.split(",") if p.strip()]
    
    for part in parts:
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start, end = int(start_str.strip()), int(end_str.strip())
            if start > end:
                start, end = end, start
            indices.update(range(start, end + 1))
        else:
            indices.add(int(part))
            
    return sorted(list(indices))


def main():
    print("=" * 70)
    print("  BIP86 (Taproot) Private Key Extractor — Диапазон индексов")
    print("=" * 70)

    # 1. Ввод мнемоники (ввод скрывается для безопасности)
    while True:
        mnemonic = getpass.getpass("Введите или скопируйте мнемонику BIP39 (слова через пробел): ").strip()
        if not mnemonic:
            print("Мнемоника не может быть пустой.")
            continue
        try:
            Bip39MnemonicValidator().Validate(mnemonic)
            break
        except Exception as e:
            print(f"Некорректная мнемоника ({e}). Попробуйте еще раз.")

    # 2. Passphrase (13-е / 25-е слово), если задавалось
    passphrase = getpass.getpass("Введите BIP39 Passphrase (нажмите Enter, если нет): ").strip()

    print("\nПараметры деривации (как в Sparrow):")

    # 3. Аккаунт (по умолчанию 0)
    acc_raw = input("Account index [0]: ").strip()
    account_idx = int(acc_raw) if acc_raw else 0

    # 4. Ветка: 0 = Receive, 1 = Change
    change_raw = input("Chain (0 для Receive / 1 для Change) [0]: ").strip()
    is_change = int(change_raw) if change_raw else 0

    # 5. Диапазон индексов
    while True:
        raw_idx = input("Индексы адресов (например, '0-5', '3' или '0, 2, 5-10'): ").strip()
        try:
            target_indices = parse_indices(raw_idx)
            if not target_indices:
                print("Список индексов пуст. Попробуйте еще раз.")
                continue
            break
        except ValueError:
            print("Некорректный формат. Используйте числа, дефисы и запятые (например, 0-10 или 1,3,5).")

    # Вычисление мастер-ключа (делается 1 раз)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    bip86_mst = Bip86.FromSeed(seed_bytes, Bip86Coins.BITCOIN)

    bip86_acc = bip86_mst.Purpose().Coin().Account(account_idx)
    change_type = Bip44Changes.CHAIN_INT if is_change == 1 else Bip44Changes.CHAIN_EXT
    chain_node = bip86_acc.Change(change_type)

    chain_name = "Change" if is_change == 1 else "Receive"
    print("\n" + "=" * 110)
    print(f"Аккаунт: {account_idx} | Ветка: {is_change} ({chain_name}) | Индексов к выводу: {len(target_indices)}")
    print("=" * 110)

    for idx in target_indices:
        addr_node = chain_node.AddressIndex(idx)
        path = f"m/86'/0'/{account_idx}'/{is_change}/{idx}"
        addr = addr_node.PublicKey().ToAddress()
        wif = addr_node.PrivateKey().ToWif()
        hex_key = addr_node.PrivateKey().Raw().ToHex()

        print(f"[{path}]")
        print(f"  Address: {addr}")
        print(f"  WIF:     {wif}")
        print(f"  HEX:     {hex_key}")
        print("-" * 110)


if __name__ == "__main__":
    main()
