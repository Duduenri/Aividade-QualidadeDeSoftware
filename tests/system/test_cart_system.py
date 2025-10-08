
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"

def login_and_wait_inventory(driver):
    driver.delete_all_cookies()
    driver.get(BASE_URL)
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    driver.execute_script("arguments[0].click();", login_btn)
    WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "inventory_container"))
    )

def go_to_cart(driver):
    cart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".shopping_cart_link"))
    )
    driver.execute_script("arguments[0].click();", cart_link)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cart_contents_container"))
    )

def add_item(driver, item_id_suffix: str):
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, f"add-to-cart-{item_id_suffix}"))
    )
    driver.execute_script("arguments[0].click();", add_button)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f"remove-{item_id_suffix}"))
    )

def remove_item(driver, item_id_suffix: str):
    remove_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, f"remove-{item_id_suffix}"))
    )
    driver.execute_script("arguments[0].click();", remove_button)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, f"remove-{item_id_suffix}"))
    )

def get_cart_badge_text(driver):
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    return badges[0].text if badges else None

def wait_for_cart_badge(driver, expected_text):
    WebDriverWait(driver, 10).until(
        lambda drv: get_cart_badge_text(drv) == expected_text
    )

def test_add_single_item_to_cart(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-backpack")
    wait_for_cart_badge(driver, "1")
    assert get_cart_badge_text(driver) == "1"
    go_to_cart(driver)
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Backpack" in names

def test_add_two_and_remove_one(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-backpack")
    add_item(driver, "sauce-labs-bike-light")
    wait_for_cart_badge(driver, "2")
    go_to_cart(driver)
    remove_item(driver, "sauce-labs-backpack")
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Backpack" not in names
    assert "Sauce Labs Bike Light" in names
    wait_for_cart_badge(driver, "1")
    assert get_cart_badge_text(driver) == "1"

def test_cart_persists_and_continue_shopping(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-bolt-t-shirt")
    wait_for_cart_badge(driver, "1")
    go_to_cart(driver)
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "continue-shopping"))
    )
    driver.execute_script("arguments[0].click();", continue_button)
    WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "inventory_container"))
    )
    wait_for_cart_badge(driver, "1")
    go_to_cart(driver)
    names = [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    assert "Sauce Labs Bolt T-Shirt" in names

def test_checkout_without_customer_info_shows_error(driver):
    login_and_wait_inventory(driver)
    add_item(driver, "sauce-labs-backpack")
    wait_for_cart_badge(driver, "1")
    go_to_cart(driver)
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )
    driver.execute_script("arguments[0].click();", checkout_button)
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "continue"))
    )
    driver.execute_script("arguments[0].click();", continue_button)
    error_banner = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "First Name is required" in error_banner.text
