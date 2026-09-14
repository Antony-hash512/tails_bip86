#!/usr/bin/env bash
set -e

# RU: Язык по умолчанию — английский (en)
# EN: Default language is English (en)
LANG_OPT="en"

# RU: Парсинг аргументов командной строки (-l / --lang)
# EN: Parse command-line arguments (-l / --lang)
while [ $# -gt 0 ]; do
    case "$1" in
        -l|--lang)
            if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                LANG_OPT="$2"
                shift 2
            else
                echo "Error: Argument for $1 is missing." >&2
                echo "Ошибка: Отсутствует аргумент для $1." >&2
                exit 1
            fi
            ;;
        -l=*|--lang=*)
            LANG_OPT="${1#*=}"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-l|--lang ru|en]"
            echo "Использование: $0 [-l|--lang ru|en]"
            exit 0
            ;;
        *)
            echo "Error: Unknown argument '$1'." >&2
            echo "Ошибка: Неизвестный аргумент '$1'." >&2
            echo "Usage: $0 [-l|--lang ru|en]" >&2
            echo "Использование: $0 [-l|--lang ru|en]" >&2
            exit 1
            ;;
    esac
done

# RU: Проверка корректности выбранного языка
# EN: Validate selected language
case "${LANG_OPT}" in
    ru|RU)
        LANG_OPT="ru"
        ;;
    en|EN)
        LANG_OPT="en"
        ;;
    *)
        echo "Error: Unsupported language '${LANG_OPT}'. Supported values: en, ru." >&2
        echo "Ошибка: Неподдерживаемый язык '${LANG_OPT}'. Допустимые значения: en, ru." >&2
        exit 1
        ;;
esac

# RU: Определяем абсолютный путь к папке, где лежит сам скрипт
# EN: Determine the absolute path to the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# RU: Поиск локального бинарника Python
# EN: Locate local Python binary in py_runtime
PYTHON_BIN=$(find "${SCRIPT_DIR}/py_runtime" -path "*/bin/python3*" -type f 2>/dev/null | head -n 1)

# RU: Выбор целевого скрипта в зависимости от языка
# EN: Select target script depending on the chosen language
if [ "${LANG_OPT}" = "ru" ]; then
    SCRIPT_TARGET="${SCRIPT_DIR}/extract_key.py"
else
    SCRIPT_TARGET="${SCRIPT_DIR}/extract_key_en.py"
fi

# RU: Проверка наличия бинарника
# EN: Check if Python binary exists and is executable
if [ -z "${PYTHON_BIN}" ] || [ ! -x "${PYTHON_BIN}" ]; then
    if [ "${LANG_OPT}" = "ru" ]; then
        echo "Ошибка: исполняемый файл Python не найден в ${SCRIPT_DIR}/py_runtime" >&2
    else
        echo "Error: Python executable not found in ${SCRIPT_DIR}/py_runtime" >&2
    fi
    exit 1
fi

# RU: Проверка наличия целевого скрипта
# EN: Check if target script exists
if [ ! -f "${SCRIPT_TARGET}" ]; then
    if [ "${LANG_OPT}" = "ru" ]; then
        echo "Ошибка: исполняемый скрипт ${SCRIPT_TARGET} не найден." >&2
    else
        echo "Error: Target script ${SCRIPT_TARGET} not found." >&2
    fi
    exit 1
fi

# RU: Запуск скрипта через изолированный рантайм
# EN: Run the script using isolated runtime
exec "${PYTHON_BIN}" "${SCRIPT_TARGET}"
