# Инструкция по запуску проекта


 **Клонируйте репозиторий**

`git clone https://github.com/nukce1/litestar-testing.git`

 **Перейдите в репозиторий**

`cd litestar-testing/`
 
**Переименуйте файл конфигурации**

`mv .env_example .env`

**Запустите контейнеры**

`sudo docker compose up --build`

# Проверка работоспособности


 **Для отправки запросов используйте документацию Swagger**

 `http://127.0.0.1:8000/schema#`
