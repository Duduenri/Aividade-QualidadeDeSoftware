
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"

def login_and_wait_inventory(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "inventory_container")))

def go_to_cart(driver):
    driver.find_element(By.ID, "shopping_cart_container").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cart_contents_container")))

def add_item(driver, item_id_suffix: str):
    driver.find_element(By.ID, f"add-to-cart-{item_id_suffix}").click()

def remove_item(driver, item_id_suffix: str):
    driver.find_element(By.ID, f"remove-{item_id_suffix}").click()

def get_cart_badge_text(driver):
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    return badges[0].text if badges else None

def test_add_single_item_to_cart(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-backpack")
    assert get_cart_badge_text(driver) == "1"
    go_to_cart(driver)
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Backpack" in names

def test_add_two_and_remove_one(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-backpack")
    add_item(driver, "sauce-labs-bike-light")
    assert get_cart_badge_text(driver) == "2"
    go_to_cart(driver)
    remove_item(driver, "sauce-labs-backpack")
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Backpack" not in names
    assert "Sauce Labs Bike Light" in names
    assert get_cart_badge_text(driver) == "1"

def test_cart_persists_and_continue_shopping(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-bolt-t-shirt")
    assert get_cart_badge_text(driver) == "1"
    go_to_cart(driver)
    driver.find_element(By.ID, "continue-shopping").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "inventory_container")))
    assert get_cart_badge_text(driver) == "1"
    go_to_cart(driver)
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Bolt T-Shirt" in names
