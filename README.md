# AtomicHabits

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. 
<br/>
Данный проект представляет из себя бэкенд-часть SPA веб-приложения, реализующая напоминания пользователям о необходимости выполнения действий для выработки привычек
<br/><br/>
<h4>В проекте реализован следующий функционал:</h4>
- Регистрация
- Авторизация посредством bearer токена
- Создание привычки (для любого зарегистрированный пользователя кроме модератора)
- Вывод списка привычек текущего пользователя с пагинацией
- Вывод списка всех привычек (для модератора)
- Просмотр привычки (для создателя или модератора и для всей зарегистрированных если привычка публичная)
- Вывод списка публичных привычек
- Редактирование привычки (для создателя или модератора)
- Удаление привычки (только для создателя)
<br/><br/>
В проекте предусмотренны настройки безопасности CORS. По умолчанию, доступ к приложению только с localhost
<br/><br/>

<h4>Ограничения:</h4>
- Исключен одновременный выбор связанной привычки и указания вознаграждения
- Время выполнения должно быть не больше 120 секунд
- В связанные привычки могут попадать только привычки с признаком приятной привычки
- У приятной привычки не может быть вознаграждения или связанной привычки
- Нельзя выполнять привычку реже, чем 1 раз в 7 дней
<br/><br/>

<h3>Запуск проекта:</h3>

1. Клонируйте репозиторий;
2. Создайте Telegram бота и получите его токен;
3. Создайте в корне проекта и заполните файл .env:

```
DEBUG=on
SECRET_KEY=

DATABASE_NAME=atomic_habits
DATABASE_USER=
DATABASE_PASSWORD=

TELEGRAM_BOT_TOKEN=
```
4. Установите зависимости poetry:

```bash
poetry install
```

5. Активируйте виртуальное окружение:

```bash
poetry shell
```

6. Создайте новую базу данных с именем к примеру atomic_habits

```bash
psql
#CREATE DATABASE atomic_habits;
#\q
```

7. Примените миграции:

```bash
python3 manage.py migrate
```

8. В отдельном окне терминала запустите celery worker

```bash
celery -A config worker -l INFO
```

9. В отдельном окне терминала запустите celery beat

```bash
celery -A config beat -l INFO -S django
```

10. Для получения документации, запустите проект и при помощи браузера перейдите по адресу:
http://127.0.0.1:8000/swagger/
<br/><br/>

Проект готов к заполнению базы данных.

<h3>Инструкция для быстрого заполнения базы данных:</h3>

<h4>Заполнение базы данных из фикстур</h4>

```bash
python3 manage.py loaddata fixtures/db.json
```
Далее необходимо указать Telegram ID для всех тестовых пользователей:

```bash
python3 manage.py settg --tg TelegramID
```

Где "TelegramID" необходимо заменить на ваш ID, например 123456789
<br/><br/>
По умолчанию, пользователи в базе данных имеют следующие параметры:
<br/>
Администратор:
```
email = 'admin@sky.pro'
password = 'admin'
```
Пользователи:
```
ivanov@sky.pro - MODERATOR
petrov@sky.pro
sidorov@sky.pro

password - 123qwe
```

<h4>Cоздание демонстрационных пользователей</h3>

Если вы желаете заполнить базу привычками самостоятельно, то можно упростить задачу создав тестовых пользователей.
<br/>
Пользователи создаются с параметром --tg. В нем указывается Telegram ID на который будут приходить сообщения.
<br/>
Админ:

```bash
python3 manage.py ccsu --tg 123456789
```
Обычные пользователи и 1 из них модератор:

```bash
python3 manage.py ccusers --tg 123456789
```
При создании пользователей в консоль выведутся email, пароли, привилегии и Telegram ID