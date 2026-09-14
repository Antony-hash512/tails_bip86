[English](#english) | [Русский](#russian)

---


## English

This Python script is designed to extract individual private keys for the relatively new Bitcoin taproot format (BIP-86 specification) from a 12- or 24-word mnemonic phrase and an optional passphrase. Following the instructions below, the script can be prepared for offline execution on a computer without an internet connection (for example, using a live USB with Tails OS or on an "air-gapped" PC).

Created as a companion to the offline browser utility [iancoleman/bip39](https://github.com/iancoleman/bip39), which as of 2026 still does not support the taproot format (BIP-86).
Also as of 2026:
- The Electrum Bitcoin wallet still does not support the taproot format.
- The more advanced Sparrow Bitcoin wallet supports the taproot format, but does not support displaying private keys.




### Preparing a Standalone Environment for Offline Execution (Tails / Air-gapped PC)

To run the script in an isolated environment without internet access (for example, in Tails), the following are required:

1. `py_runtime` directory — a portable standalone binary of the required Python version (CPython standalone).
2. `wheels` directory — the pre-built `bip-utils` library and all its dependencies, compatible with the Python version in `py_runtime`.

Preparation is performed on a computer with internet access using the [`uv`](https://github.com/astral-sh/uv) package manager.

---

#### Step 1. Navigate to the project directory

Connect the USB drive or open the working directory:

```bash
cd tails_bip86

```

---

#### Step 2. Download standalone Python runtime (`py_runtime`)

Download a portable standalone binary for Python 3.11, 3.12, 3.13 (or newer, once all required libraries are built into wheels), in this case for the `x86_64` architecture:

```bash
uv python install 3.12 --install-dir ./py_runtime

```

```bash
uv python install 3.13 --install-dir ./py_runtime

```

A folder like `cpython-3.13.X-linux-x86_64-gnu/` will appear in the `py_runtime` directory.

*(Optional)* If `uv` created a broken relative symlink inside `py_runtime`, remove or fix it:

```bash
cd py_runtime
rm -f cpython-3.13-linux-x86_64-gnu
ln -s cpython-3.13.*-linux-x86_64-gnu cpython-3.11-linux-x86_64-gnu
cd ..

```

---

#### Step 3. Install libraries into the `wheels` directory

Build and install the `bip-utils` library with all its dependencies into the local `./wheels` folder.

Be sure to specify the Python version flag, for example `--python 3.13`, so that C-extensions (modules like `crcmod` and `cffi`) are compiled strictly for the downloaded runtime version, rather than for the host machine's system Python:

```bash
uv pip install \
  --python 3.12 \
  --target ./wheels \
  bip-utils

```


```bash
uv pip install \
  --python 3.13 \
  --target ./wheels \
  bip-utils

```

---

#### Step 4. Verify the final file structure

Before transferring to the offline machine, make sure the `tails_bip86` directory structure looks as follows:

```text
tails_bip86/
├── py_runtime/
│   └── cpython-3.13.X-linux-x86_64-gnu/
│       └── bin/
│           └── python3
├── wheels/
│   ├── bip_utils/
│   ├── cffi/
│   ├── crcmod/
│   └── ... (remaining modules)
├── extract_key.py
└── run.sh

```

---

#### Step 5. Run on an offline machine (Tails)

1. Connect the storage drive to the isolated computer, e.g. booted from a Tails USB flash drive.
2. Navigate to the script directory in the terminal:
```bash
cd /path/to/tails_bip86
chmod +x run.sh
./run.sh

```


3. The script will run without accessing the network and without using system OS packages.

---

## Russian

Данный python-скрипт предназначен для получения отдельных приватных ключей относительного нового формата Bitcoin taproot (спецификация BIP-86) из 12-ти или 24-х слов mnemonic фразы и опционального passpharse. Следуя инструкциям ниже, скрипт можно подготовить для запуска в офлайн режиме на компьютере без подключения к интернету (например, с использованием загруженной с флешки с ОС Tails или на "air-gapped" ПК).

Создан как дополнение к браузерной офлайновой утилите [iancoleman/bip39](https://github.com/iancoleman/bip39)
которая по состоянию на 2026 год всё ещё не поддерживает формат taproot (BIP-86).
Так же по состоянию на 2026 год:
- Bitcoin-кошелёк Electrum также всё ещё не поддерживает формат taproot.
- Более продвинутый Bitcoin-кошелёк Sparrow поддерживает формат taproot, но не поддерживает отображение приватных ключей.




### Подготовка автономного окружения для офлайн-запуска (Tails / Air-gapped PC)

Для работы скрипта в изолированной среде без доступа к интернету (например, в Tails) требуются:

1. Каталог `py_runtime` — переносимый автономный бинарник Python нужной версии (CPython standalone).
2. Каталог `wheels` — предварительно собранная библиотека `bip-utils` и все её зависимости, совместимые с версией Python из `py_runtime`.

Подготовка выполняется на компьютере с доступом в интернет при помощи пакетного менеджера [`uv`](https://github.com/astral-sh/uv).

---

#### Шаг 1. Перейдите в каталог проекта

Подключите флешку или откройте рабочую директорию:

```bash
cd tails_bip86

```

---

#### Шаг 2. Загрузка автономного рантайма Python (`py_runtime`)

Скачайте переносимый автономный бинарник Python 3.11, 3.12, 3.13 (или более новой, когда все необходимые библиотеки будут собираться в wheels) в данном случае для архитектуры `x86_64`:

```bash
uv python install 3.12 --install-dir ./py_runtime

```

```bash
uv python install 3.13 --install-dir ./py_runtime

```

В каталоге `py_runtime` появится папка вида `cpython-3.13.X-linux-x86_64-gnu/`.

*(Опционально)* Если `uv` создал битый относительный симлинк внутри `py_runtime`, удалите его или почините:

```bash
cd py_runtime
rm -f cpython-3.13-linux-x86_64-gnu
ln -s cpython-3.13.*-linux-x86_64-gnu cpython-3.11-linux-x86_64-gnu
cd ..

```

---

#### Шаг 3. Установка библиотек в каталог `wheels`

Соберите и установите библиотеку `bip-utils` со всеми зависимостями в локальную папку `./wheels`.

Обязательно укажите флаг версии Python например `--python 3.13`, чтобы C-расширения (модули вроде `crcmod` и `cffi`) были скомпилированы строго под рантайм скаченной версии, а не под системный Python хост-машины:

```bash
uv pip install \
  --python 3.12 \
  --target ./wheels \
  bip-utils

```


```bash
uv pip install \
  --python 3.13 \
  --target ./wheels \
  bip-utils

```

---

#### Шаг 4. Проверка итоговой структуры файлов

Перед переносом на офлайн-машину убедитесь, что структура каталога `tails_bip86` выглядит следующим образом:

```text
tails_bip86/
├── py_runtime/
│   └── cpython-3.13.X-linux-x86_64-gnu/
│       └── bin/
│           └── python3
├── wheels/
│   ├── bip_utils/
│   ├── cffi/
│   ├── crcmod/
│   └── ... (остальные модули)
├── extract_key.py
└── run.sh

```

---

#### Шаг 5. Запуск на офлайн-машине (Tails)

1. Подключите накопитель к изолированному компьютеру например загруженному с флешки с Tails.
2. Перейдите в каталог скрипта в терминале:
```bash
cd /path/to/tails_bip86
chmod +x run.sh
./run.sh

```


3. Скрипт запустится без обращения к сети и без использования системных пакетов ОС.


---


