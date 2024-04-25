# Проект aggr_bot:

### Создать телеграм бота, который будет принимать от пользователей текстовые сообщения содержащие JSON с входными данными и отдавать агрегированные данные в ответ.

[Тестовое задание](https://docs.google.com/document/d/14DcCb6Pj3PNsFqJzaS_hAhyePqRXF6uvmTzobp_G8PM/edit)

<br>

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Описание работы](#описание-работы)
- [Удаление](#удаление)
- [Автор](#автор)

<br>

## Технологии:

<details><summary>Подробнее</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/Python-3.12-white?logo=python)](https://www.python.org/)
[![asyncio](https://img.shields.io/badge/asyncio-464646?logo=asyncio)](https://docs.python.org/3/library/asyncio-task.html)
[![json](https://img.shields.io/badge/json-464646?logo=json)](https://docs.python.org/3/library/json.html)
[![datetime](https://img.shields.io/badge/datetime-464646?logo=datetime)](https://docs.python.org/3/library/datetime.html)
[![calendar](https://img.shields.io/badge/calendar-464646?logo=calendar)](https://docs.python.org/3/library/calendar.html)

**Фреймворк, расширения и библиотеки:**

[![Aiogram ](https://img.shields.io/badge/Aiogram-v3.5.0-blue?logo=Aiogram)](https://docs.aiogram.dev/en/latest/)


**Базы данных и инструменты работы с БД:**

[![PyMongo](https://img.shields.io/badge/PyMongo-v4.6.3-green?logo=MongoDB)](https://pymongo.readthedocs.io/en/stable/tutorial.html)

[⬆️Оглавление](#оглавление)
</details>

<br>

## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь:
 
 - создал аккаунт [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).

<h1></h1>
</details>

#### Локальный запуск

1. Клонируйте репозиторий с GitHub и введите персональные данные для переменных (значения даны для примера):
```bash
git clone https://github.com/daniilbp/Aiogram-aggr_bot.git && \
cd Aiogram-aggr_bot && \
cp aggr_bot/additions/conf_example aggr_bot/additions/p_conf.py && \
nano aggr_bot/additions/p_conf.py
```

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
   python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
   python -m venv venv && source venv/Scripts/activate
   ```

3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```

4. Выполните вставку данных в MongoDB и запустите тг бота:
   ```bash
   python aggr_bot/create_db_atlas.py && \
   python aggr_bot/tgbot.py  
   ```

5. Остановить бота можно комбинацией клавиш Ctl-C.

Работа с ботом происходит в @username_bot, который был указан в @BotFather при получении токена бота
  - /start - выведет доступные команды в формате и шаблоне

[⬆️Оглавление](#оглавление)

<br>

## Описание работы:

Модуль `aggr_bot/tgbot.py` - асинхронный телеграм бот, который будет принимает от пользователей текстовые сообщения содержащие JSON с входными данными и отдает агрегированные данные в ответ. Пример - @rlt_testtaskexample_bot.

Модуль `aggr_bot/driver.py` - асинхронный генератор задач с алгоритм агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам с проверкой входящих данных на валидность.

Модуль `aggr_bot/tools/pymongo_clients.py` - коннектор к MongoDB: локальный и ч/з Atlas.

Модуль `aggr_bot/tools/utils.py` - фсинхронные технические функции для рассчета дэльты (шага) до нового периода, указанного во входных данных. Функция с синхронным исполнением функционала + синхронные технические ф-ии.

Модуль `aggr_bot/additions/addition.py` - дополнения: справочная, текстовая, проверочная информация.

Подробнее в [Тестовом задании](#проект-aggr_bot)

[⬆️Оглавление](#оглавление)

<br>

## Удаление:
Для удаления проекта выполните следующие действия:
```bash
cd .. && rm -fr Aiogram-aggr_bot && deactivate
```
  
[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Daniil Boyko](https://github.com/daniilbp)

[⬆️В начало](#проект-aggr_bot)
