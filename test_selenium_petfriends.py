import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='class')
def testing_auth_and_all_pets_page():
    try:
        pytest.driver = webdriver.Chrome('./chromedriver.exe')
        pytest.driver.implicitly_wait(10)
        pytest.driver.get('https://petfriends.skillfactory.ru')

        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()  # Кнопка "Зарегистрироваться"
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/new_user'

        pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]').click()  # Ссылка "У меня уже есть аккаунт"
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/login'

        pytest.driver.find_element(By.ID, 'email').send_keys('email')  # Поле "Электронная почта"
        pytest.driver.find_element(By.ID, 'pass').send_keys('password')  # Поле "Пароль"
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()  # Кнопка "Войти"
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
        assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

        yield

    finally:
        pytest.driver.quit()


@pytest.fixture(scope='class')
def testing_auth_and_my_pets_page():
    try:
        pytest.driver = webdriver.Chrome('./chromedriver.exe')
        pytest.driver.get('https://petfriends.skillfactory.ru')

        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-success')))
        # Кнопка "Зарегистрироваться"
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/new_user'

        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/login"]')))
        # Ссылка "У меня уже есть аккаунт"
        pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]').click()
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/login'

        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))
        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.ID, 'pass')))
        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-success')))
        # Поля "Электронная почта" и "Пароль", кнопка "Войти"
        pytest.driver.find_element(By.ID, 'email').send_keys('email')
        pytest.driver.find_element(By.ID, 'pass').send_keys('password')
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()  # Кнопка "Войти"
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
        assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

        WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]')))
        # Ссылка "Мои питомцы"
        pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

        yield

    finally:
        pytest.driver.quit()


@pytest.mark.usefixtures('testing_auth_and_all_pets_page')
class TestAllPetsPage:
    def test_images_all_pets(self):
        pytest.driver.implicitly_wait(10)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
        images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')

        for i in range(len(names)):
            assert images[i].get_attribute('src') != ''  # or images[i].get_attribute('src') == ''

    def test_names_all_pets(self):
        pytest.driver.implicitly_wait(10)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')

        for i in range(len(names)):
            assert names[i].text != ''  # or names[i].text == ''

    def test_description_all_pets(self):
        pytest.driver.implicitly_wait(10)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
        descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

        for i in range(len(names)):
            assert descriptions[i].text != ''  # or descriptions[i].text == ''
            assert ', ' in descriptions[i].text
            parts = descriptions[i].text.split(", ")
            assert len(parts[0]) > 0  # or len(parts[0]) == 0
            assert len(parts[1]) > 0  # or len(parts[1]) == 0


@pytest.mark.usefixtures('testing_auth_and_my_pets_page')
class TestMyPetsPage:
    def test_my_pets_count(self):
        """Проверяется, что в таблице есть все питомцы пользователя"""

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 '//div[@class=".col-sm-4 left"]')))
        # Статистика пользователя
        user_statistics_str = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text
        user_statistics_list = user_statistics_str.split('\n')
        my_pets_count_statistics = None

        for i in user_statistics_list:
            if 'Питомцев' in i:
                my_pets_count_statistics = int(i.split(': ')[1])

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
        # Данные питомцев в таблице
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)
        assert my_pets_count_statistics == my_pets_count_table

    def test_images_my_pets(self):
        """Проверяется, что хотя бы у половины питомцев есть фото"""

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
        # Данные питомцев в таблице
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)

        WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img')))
        # Данные питомцев в таблице
        images_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
        images_my_pets_count = 0

        for i in range(my_pets_count_table):
            if images_my_pets[i].get_attribute('src') != '':
                images_my_pets_count += 1

        assert images_my_pets_count >= my_pets_count_table / 2

    def test_names_species_ages_my_pets(self):
        """Проверяется, что у всех питомцев есть имя, возраст и порода"""

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
        # Данные питомцев в таблице
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[2]')))
        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[3]')))
        # Имена, порода и возраст питомцев
        names_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        species_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        ages_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

        for i in range(my_pets_count_table):
            assert names_my_pets[i].text != ''
            assert species_my_pets[i].text != ''
            assert ages_my_pets[i].text != ''

    def test_names_difference_my_pets(self):
        """Проверяется, что у всех питомцев разные имена"""

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
        # Данные питомцев в таблице
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
        # Имена питомцев
        names_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        names_my_pets_list = [names_my_pets[i].text for i in range(my_pets_count_table)]
        names_my_pets_set = set(names_my_pets_list)
        assert len(names_my_pets_list) == len(names_my_pets_set)

    def test_pets_difference_my_pets(self):
        """Проверяется, что в списке нет повторяющихся питомцев"""

        WebDriverWait(pytest.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
        # Данные питомцев в таблице
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)
        my_pets_list = [my_pets[i].text for i in range(my_pets_count_table)]
        my_pets_set = set(my_pets_list)
        assert len(my_pets_list) == len(my_pets_set)