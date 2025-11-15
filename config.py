"""
Configuration loader for ByBit Trading Bot
Безопасная загрузка API ключей из переменных окружения
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные из .env файла
load_dotenv()


class Config:
    """Конфигурация бота с безопасной загрузкой API ключей"""

    # ByBit API credentials
    BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
    BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')

    # Testnet credentials
    BYBIT_TESTNET_API_KEY = os.getenv('BYBIT_TESTNET_API_KEY')
    BYBIT_TESTNET_API_SECRET = os.getenv('BYBIT_TESTNET_API_SECRET')

    # Trading settings
    USE_TESTNET = os.getenv('USE_TESTNET', 'true').lower() == 'true'
    TRADING_SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
    TRADING_MODE = os.getenv('TRADING_MODE', 'spot')

    # Risk management
    MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', '1000'))
    STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', '2.0'))
    TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT', '5.0'))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'

    @classmethod
    def validate(cls):
        """
        Проверка что все необходимые ключи настроены
        Validates that all required keys are configured
        """
        if cls.USE_TESTNET:
            required_keys = ['BYBIT_TESTNET_API_KEY', 'BYBIT_TESTNET_API_SECRET']
            api_key = cls.BYBIT_TESTNET_API_KEY
            api_secret = cls.BYBIT_TESTNET_API_SECRET
        else:
            required_keys = ['BYBIT_API_KEY', 'BYBIT_API_SECRET']
            api_key = cls.BYBIT_API_KEY
            api_secret = cls.BYBIT_API_SECRET

        # Проверяем что ключи установлены
        if not api_key or not api_secret:
            raise ValueError(
                f"\n❌ API ключи не найдены!\n"
                f"Required keys: {', '.join(required_keys)}\n\n"
                f"Пожалуйста:\n"
                f"1. Скопируйте .env.example в .env: cp .env.example .env\n"
                f"2. Откройте .env и добавьте ваши API ключи\n"
                f"3. Перезапустите бота\n"
            )

        # Проверяем что это не примеры значений
        if 'your_api_key_here' in str(api_key) or 'your_api_key_here' in str(api_secret):
            raise ValueError(
                f"\n❌ Обнаружены примеры значений в .env файле!\n"
                f"Замените 'your_api_key_here' на ваши реальные API ключи\n"
            )

        return True

    @classmethod
    def get_api_credentials(cls):
        """
        Возвращает правильные API credentials в зависимости от режима
        Returns correct API credentials depending on mode (testnet/mainnet)
        """
        cls.validate()

        if cls.USE_TESTNET:
            return {
                'api_key': cls.BYBIT_TESTNET_API_KEY,
                'api_secret': cls.BYBIT_TESTNET_API_SECRET,
                'testnet': True
            }
        else:
            return {
                'api_key': cls.BYBIT_API_KEY,
                'api_secret': cls.BYBIT_API_SECRET,
                'testnet': False
            }

    @classmethod
    def print_config(cls):
        """Выводит конфигурацию БЕЗ секретных ключей"""
        print("\n" + "="*50)
        print("⚙️  Конфигурация бота")
        print("="*50)
        print(f"Режим: {'🧪 TESTNET' if cls.USE_TESTNET else '💰 MAINNET'}")
        print(f"Торговая пара: {cls.TRADING_SYMBOL}")
        print(f"Режим торговли: {cls.TRADING_MODE}")
        print(f"Макс. размер позиции: ${cls.MAX_POSITION_SIZE}")
        print(f"Stop Loss: {cls.STOP_LOSS_PERCENT}%")
        print(f"Take Profit: {cls.TAKE_PROFIT_PERCENT}%")
        print(f"Уровень логирования: {cls.LOG_LEVEL}")

        # Проверяем что ключи установлены (но не показываем их!)
        creds = cls.get_api_credentials()
        key_preview = creds['api_key'][:8] + "..." if creds['api_key'] else "НЕ УСТАНОВЛЕН"
        print(f"API Key: {key_preview}")
        print("="*50 + "\n")


# Проверка при импорте (только если файл .env существует)
if Path('.env').exists():
    try:
        Config.validate()
    except ValueError as e:
        print(f"\n⚠️  Предупреждение при загрузке конфигурации:\n{e}")
