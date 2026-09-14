#!/usr/bin/env python3
import getpass
import sys
from pathlib import Path

# Add adjacent wheels directory to sys.path for offline library imports
WHEELS_DIR = Path(__file__).resolve().parent / "wheels"
if not WHEELS_DIR.exists():
    print(f"Error: dependency directory not found at: {WHEELS_DIR}")
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
    print(f"Error loading libraries from {WHEELS_DIR}: {err}")
    sys.exit(1)


def parse_indices(input_str: str) -> list[int]:
    """Parses strings like '0-5', '3', '0, 2, 5-8' into a sorted list of unique ints."""
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
    print("  BIP86 (Taproot) Private Key Extractor — Index Range")
    print("=" * 70)

    # 1. Mnemonic input (input is hidden for security)
    while True:
        mnemonic = getpass.getpass("Enter or paste BIP39 mnemonic (space-separated words): ").strip()
        if not mnemonic:
            print("Mnemonic cannot be empty.")
            continue
        try:
            Bip39MnemonicValidator().Validate(mnemonic)
            break
        except Exception as e:
            print(f"Invalid mnemonic ({e}). Please try again.")

    # 2. Passphrase (13th / 25th word), if specified
    passphrase = getpass.getpass("Enter BIP39 Passphrase (press Enter if none): ").strip()

    print("\nDerivation parameters (as in Sparrow):")

    # 3. Account (default is 0)
    acc_raw = input("Account index [0]: ").strip()
    account_idx = int(acc_raw) if acc_raw else 0

    # 4. Chain: 0 = Receive, 1 = Change
    change_raw = input("Chain (0 for Receive / 1 for Change) [0]: ").strip()
    is_change = int(change_raw) if change_raw else 0

    # 5. Address index range
    while True:
        raw_idx = input("Address indices (e.g., '0-5', '3' or '0, 2, 5-10'): ").strip()
        try:
            target_indices = parse_indices(raw_idx)
            if not target_indices:
                print("Index list is empty. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid format. Use numbers, hyphens, and commas (e.g., 0-10 or 1,3,5).")

    # Calculate master key (performed once)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    bip86_mst = Bip86.FromSeed(seed_bytes, Bip86Coins.BITCOIN)

    bip86_acc = bip86_mst.Purpose().Coin().Account(account_idx)
    change_type = Bip44Changes.CHAIN_INT if is_change == 1 else Bip44Changes.CHAIN_EXT
    chain_node = bip86_acc.Change(change_type)

    chain_name = "Change" if is_change == 1 else "Receive"
    print("\n" + "=" * 110)
    print(f"Account: {account_idx} | Chain: {is_change} ({chain_name}) | Indices to output: {len(target_indices)}")
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
