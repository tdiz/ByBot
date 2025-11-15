# 🔐 Реальная защита API ключей

## ⚠️ Правда о безопасности

`.gitignore` - это **первая линия защиты**, но не панацея.

### Что может пойти не так:

1. **Ключи в коде:**
   ```python
   # ❌ НИКОГДА так не делайте!
   API_KEY = "your_actual_key_here"
   ```

2. **Force add:**
   ```bash
   git add -f .env  # Обходит .gitignore!
   ```

3. **Файл уже в истории:**
   - Если `.env` был закоммичен ДО добавления в `.gitignore`
   - Остаётся в истории git навсегда

4. **Переименование:**
   ```bash
   mv .env config.env  # .gitignore не сработает
   ```

## ✅ Многоуровневая защита

### Уровень 1: .gitignore (уже настроен)
Защищает от случайных ошибок.

### Уровень 2: Pre-commit hooks
```bash
# Установка
pip install pre-commit detect-secrets
pre-commit install

# Создание baseline
detect-secrets scan > .secrets.baseline

# Теперь pre-commit будет сканировать каждый коммит
```

### Уровень 3: Проверка перед каждым push
```bash
# Всегда проверяйте ЧТО вы пушите:
git diff origin/main

# Ищите подозрительные строки:
git diff origin/main | grep -i "key\|secret\|password\|token"
```

### Уровень 4: Регулярный аудит
```bash
# Проверка что .env не в истории:
git log --all --full-history -- .env

# Если что-то найдено - НЕМЕДЛЕННО:
# 1. Отзовите ключи на бирже
# 2. Очистите историю git
```

### Уровень 5: Ограничение прав API ключей

На ByBit:
- ✅ READ - для получения данных
- ✅ TRADE - для торговли
- ❌ WITHDRAW - **НИКОГДА** не давайте это право
- ✅ IP Whitelist - ограничьте доступ по IP

## 🚨 Если ключи утекли:

1. **СРАЗУ** отзовите ключи в [API Management](https://www.bybit.com/app/user/api-management)
2. Создайте новые ключи
3. Очистите git историю:
   ```bash
   # Вариант 1: BFG Repo Cleaner
   bfg --replace-text passwords.txt

   # Вариант 2: git filter-branch (старый способ)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
4. Force push (координируйте с командой!)

## 📋 Чеклист безопасности

- [ ] `.gitignore` настроен
- [ ] `.env.example` создан (БЕЗ реальных ключей)
- [ ] `.env` создан локально (не в git)
- [ ] Pre-commit hooks установлены
- [ ] API ключи с ограниченными правами
- [ ] IP whitelist настроен
- [ ] Регулярно проверяется история git
- [ ] Код ревью перед merge

## 🎓 Золотое правило

> **Никогда не доверяйте одной защите. Используйте несколько уровней.**

Даже с `.gitignore` - всегда проверяйте `git status` перед коммитом!
