set -e  

PROJECT_DIR="."

echo "=== Шаг 1: Проверка кода ==="
cd "$PROJECT_DIR"

echo "=== Шаг 2: Подготовка окружения и сборка тестов ==="

if [ ! -d "venv" ]; then
    python -m venv venv
fi

if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate  
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate     
else
    echo "Не найден файл активации виртуального окружения"
    exit 1
fi

python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install pytest
fi

echo "=== Шаг 3: Запуск unit-тестов ==="
python -m pytest tests.py -v
if [ $? -ne 0 ]; then
    echo "Тесты не прошли. CI прерван."
    exit 1
else
    echo "Все тесты пройдены успешно."
fi

echo "=== Шаг 4: Создание установочного пакета (wheel) ==="

if ! grep -q "def main()" Calculator.py; then
    echo "Добавляем функцию main() в Calculator.py..."
    cat >> Calculator.py << 'EOF'

def main():
    Main_Form.mainloop()

if __name__ == "__main__":
    main()
EOF
fi

cat > setup.py << EOF
from setuptools import setup

setup(
    name="calculator_app",
    version="1.4.1",
    author="Родион и Леха",
    description="Графический калькулятор на Tkinter",
    py_modules=["Calculator"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'calculator=Calculator:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
EOF

pip install setuptools wheel

python setup.py sdist bdist_wheel
echo "Установочный пакет создан в папке dist/"

echo "=== Шаг 5: Установка приложения локально ==="

LATEST_WHEEL=$(ls -t dist/*.whl | head -1)
pip install "$LATEST_WHEEL" --force-reinstall
echo "Приложение успешно установлено."

deactivate
echo "=== CI успешно завершён ==="
echo "Для запуска калькулятора перейдите в директорию: cd calculator_project"
echo "И выполните команду: python -m Calculator.py"
