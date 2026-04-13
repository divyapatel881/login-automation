from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
URL = "https://the-internet.herokuapp.com/login"

def get_driver():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.implicitly_wait(5)
    return driver

def test_smoke_page_loads():
    driver = get_driver()
    driver.get(URL)
    print("Page title is:", driver.title)  # <- add this line
    assert driver.find_element(By.ID, "username").is_displayed()
    assert driver.find_element(By.ID, "password").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()
    print("PASS: Smoke test — login page loads")
    driver.quit()
# def test_smoke_page_loads():
#     driver = get_driver()
#     driver.get(URL)
#     assert "Login" in driver.title
#     assert driver.find_element(By.ID, "username").is_displayed()
#     assert driver.find_element(By.ID, "password").is_displayed()
#     assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()
#     print("PASS: Smoke test — login page loads")
#     driver.quit()

def test_valid_login():
    driver = get_driver()
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    msg = driver.find_element(By.CSS_SELECTOR, ".flash.success")
    assert "You logged into a secure area!" in msg.text
    print("PASS: Valid login works")
    driver.quit()

def test_invalid_username():
    driver = get_driver()
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    msg = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert "Your username is invalid!" in msg.text
    print("PASS: Invalid username shows error")
    driver.quit()

def test_invalid_password():
    driver = get_driver()
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    msg = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert "Your password is invalid!" in msg.text
    print("PASS: Invalid password shows error")
    driver.quit()

def test_empty_fields():
    driver = get_driver()
    driver.get(URL)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    msg = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert msg.is_displayed()
    print("PASS: Empty form shows error")
    driver.quit()


if __name__ == "__main__":
    print("Starting Login Automation Suite...")
    print("=" * 40)
    test_smoke_page_loads()
    test_valid_login()
    test_invalid_username()
    test_invalid_password()
    test_empty_fields()
    print("=" * 40)
    print("All tests passed!")