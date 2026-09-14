#!/usr/bin/env bash
set -e

# Определяем абсолютный путь к папке, где лежит сам скрипт
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Поиск локального бинарника Python
PYTHON_BIN=$(find "${SCRIPT_DIR}/py_runtime" -path "*/bin/python3*" -type f 2>/dev/null | head -n 1)
SCRIPT_TARGET="${SCRIPT_DIR}/extract_key.py"

# Проверка наличия бинарника
if [ -z "${PYTHON_BIN}" ] || [ ! -x "${PYTHON_BIN}" ]; then
    echo "Ошибка: исполняемый файл Python не найден в ${SCRIPT_DIR}/py_runtime"
    exit 1
fi

# Проверка наличия целевого скрипта
if [ ! -f "${SCRIPT_TARGET}" ]; then
    echo "Ошибка: исполняемый скрипт ${SCRIPT_TARGET} не найден."
    exit 1
fi

# Запуск скрипта через изолированный рантайм, передавая все аргументы
exec "${PYTHON_BIN}" "${SCRIPT_TARGET}" "$@"
