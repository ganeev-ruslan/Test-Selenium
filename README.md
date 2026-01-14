"""
# SauceDemo Automation Tests

## Назначение
Автоматизированные тесты для проверки функционала страницы авторизации SauceDemo.

## Как запустить
1. Установите зависимости:
   pip install -r requirements.txt
2. Убедитесь, что ChromeDriver доступен в PATH.
3. Запустите тесты:
   python test_login.py

## Структура тестов

1. test_valid_login
   - Проверяет успешный вход с корректными данными (standard_user / secret_sauce).
   - Ожидаемые результаты:
     - Редирект на /inventory.html
     - Наличие заголовка "Products"
     - Видимость списка товаров (inventory_list)

2. test_empty_fields
   - Проверяет обработку пустых полей.
   - Ожидаемое сообщение: "Epic sadface: Username is required"

3. test_invalid_password
   - Проверяет реакцию на неверный пароль.
   - Ожидаемое сообщение: "Epic sadface: Username and password do not match..."

4. test_invalid_username
   - Проверяет реакцию на неверный логин.
   - Ожидаемое сообщение: аналогично test_invalid_password

5. test_locked_user
   - Проверяет сообщение для заблокированного пользователя (locked_out_user).
   - Ожидаемое сообщение: "Epic sadface: Sorry, this user has been locked out."


## Ожидаемые результаты
- OK: все тесты пройдены
- FAIL: хотя бы один тест не пройден (детали в логах)
- Скриншоты ошибок сохраняются в папку screenshots/


## Настройки (опционально)
- Измените base_url в setUp(), если нужен другой стенд
- Добавьте новые тесты в том же стиле
- Для отчётов подключите HTMLTestRunner или unittest-xml-reporting


## Зависимости (requirements.txt)
selenium>=4.0.0
unittest-xml-reporting  # для XML-отчётов (опционально)

## Ссылки
- SauceDemo: https://www.saucedemo.com
- Selenium Docs: https://www.selenium.dev/documentation/
- ChromeDriver: https://sites.google.com/chromium.org/driver/
"""
