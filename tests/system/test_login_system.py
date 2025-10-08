
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"

def do_login(driver, user, password):
    driver.delete_all_cookies()
    driver.get(BASE_URL)
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def test_login_valido(driver):
    do_login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "inventory_container"))
    )
    assert "inventory" in driver.current_url

def test_login_invalido_senha_errada(driver):
    do_login(driver, "standard_user", "senha_errada")
    err = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "Username and password do not match" in err.text

def test_usuario_bloqueado(driver):
    do_login(driver, "locked_out_user", "secret_sauce")
    err = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "Sorry, this user has been locked out." in err.text
