import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os

# Тестовые данные
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrong_password"
INVALID_USER = "invalid_user"

ERROR_MESSAGES = {
    "empty": "Epic sadface: Username is required",
    "invalid_creds": "Epic sadface: Username and password do not match any user in this service",
    "locked": "Epic sadface: Sorry, this user has been locked out."
}

class SauceDemoLoginTest(unittest.TestCase):

    def setUp(self):
        """Инициализация драйвера перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://www.saucedemo.com"
        
        # Создаем папку для скриншотов, если её нет
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def test_valid_login(self):
        """Тест 1: Успешный вход с валидными данными"""
        driver = self.driver
        driver.get(self.base_url)

        # Ввод данных
        driver.find_element(By.ID, "user-name").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        try:
            # Ожидание загрузки каталога товаров
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )

            # Проверка заголовка страницы
            title_element = driver.find_element(By.CLASS_NAME, "title")
            self.assertIn("Products", title_element.text, "Заголовок страницы не содержит 'Products'")

            # Проверка URL после редиректа
            expected_url = f"{self.base_url}/inventory.html"
            self.assertEqual(
                driver.current_url,
                expected_url,
                f"Неправильный URL после входа. Ожидалось: {expected_url}"
            )

            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 1 PASSED: Успешный вход")

        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 1 FAILED: {str(e)}")
            raise e

    def test_empty_fields(self):
        """Тест 2: Пустые поля → сообщение об ошибке"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Нажимаем кнопку входа без ввода данных
        driver.find_element(By.ID, "login-button").click()

        # Ожидание появления сообщения об ошибке
        wait = WebDriverWait(driver, 10)
        error_container = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Проверка текста сообщения
        self.assertIn(
            ERROR_MESSAGES["empty"],
            error_container.text,
            f"Неверное сообщение об ошибке. Ожидалось: {ERROR_MESSAGES['empty']}"
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 2 PASSED: Сообщение при пустых полях")

    def test_invalid_password(self):
        """Тест 3: Неверный пароль → сообщение об ошибке"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Ввод данных
        driver.find_element(By.ID, "user-name").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASSWORD)
        driver.find_element(By.ID, "login-button").click()


        # Ожидание сообщения об ошибке
        wait = WebDriverWait(driver, 10)
        error_container = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Проверка текста сообщения
        self.assertIn(
            ERROR_MESSAGES["invalid_creds"],
            error_container.text,
            f"Неверное сообщение об ошибке. Ожидалось: {ERROR_MESSAGES['invalid_creds']}"
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 3 PASSED: Сообщение при неверном пароле")


    def test_invalid_username(self):
        """Тест 4: Неверный логин → сообщение об ошибке"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Ввод данных
        driver.find_element(By.ID, "user-name").send_keys(INVALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        driver.find_element(By.ID, "login-button").click()


        # Ожидание сообщения об ошибке
        wait = WebDriverWait(driver, 10)
        error_container = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Проверка текста сообщения
        self.assertIn(
            ERROR_MESSAGES["invalid_creds"],
            error_container.text,
            f"Неверное сообщение об ошибке. Ожидалось: {ERROR_MESSAGES['invalid_creds']}"
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 4 PASSED: Сообщение при неверном логине")

    def test_locked_user(self):
        """Тест 5: Заблокированный пользователь → специальное сообщение"""
        driver = self.driver
        driver.get(self.base_url)
        
        # Ввод данных заблокированного пользователя
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        # Ожидание сообщения об ошибке
        wait = WebDriverWait(driver, 10)
        error_container = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Проверка текста сообщения
        self.assertIn(
            ERROR_MESSAGES["locked"],
            error_container.text,
            f"Неверное сообщение для заблокированного пользователя. Ожидалось: {ERROR_MESSAGES['locked']}"
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] TEST 5 PASSED: Сообщение для заблокированного пользователя")

    def tearDown(self):
        """Завершение теста: закрытие драйвера и сохранение скриншота при ошибке"""
        # Проверяем, был ли тест неудачным
        has_errors = False
        if hasattr(self, '_resultForDoCleanups'):
            result = self._resultForDoCleanups
            if result.failures or result.errors:
                has_errors = True

        if has_errors:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshots/fail_{self._testMethodName}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Скриншот ошибки сохранен: {screenshot_name}")


        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
