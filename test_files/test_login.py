import os
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException



# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables with default values
base_url = os.getenv("BASE_URL", "https://beta.sproutsai.com/login")
email = os.getenv("EMAIL", "pankaj+natera@sproutsai.com")
password = os.getenv("PASSWORD", "Demo@123")
wrong_email = os.getenv("WRONG_EMAIL", "pankaj+natera@sproutsai.comm")
wrong_password = os.getenv("WRONG_PASSWORD", "Demo@1234")

class TestGoogle:
    @pytest.mark.usefixtures("browser")
    def test_login_case1(self, browser):
        browser.get(base_url)
        wait = WebDriverWait(browser, 10)

        email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        email_element.click()

        send_email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        send_email_element.send_keys(email)

        password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        password_element.click()

        send_password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        send_password_element.send_keys(password)

        show_password = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".absolute > svg")))
        show_password.click()

        login_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary")))
        login_button.click()

        try:
            # Wait for the "Post new job" element
            WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[text()='Post new job']")))
            print('Successfully logged in')

        except TimeoutException:
            assert False, "Test failed due to incorrect username or password"

        # Check if "Post new job" is present after login
        assert "Post new job" in browser.page_source, "Post new job not found after login"


    @pytest.mark.usefixtures("browser")
    def test_login_case2(self, browser):
        #correct username wrong password
        browser.get(base_url)
        wait = WebDriverWait(browser, 10)

        email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        email_element.click()

        send_email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        send_email_element.send_keys(email)

        password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        password_element.click()

        send_password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        send_password_element.send_keys(wrong_password)

        show_password = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".absolute > svg")))
        show_password.click()

        login_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary")))
        login_button.click()

        try:
            # Wait for the "Post new job" element
            WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[text()='Cannot find an account with those credentials']")))

        except TimeoutException:
            assert False, "Test failed due to incorrect username or password"

        # Check if "Post new job" is present after login
        assert "Cannot find an account with those credentials" in browser.page_source, "Post new job not found after login"


    @pytest.mark.usefixtures("browser")
    def test_login_case3(self, browser):
        #wrong username correct password 
        browser.get(base_url)
        wait = WebDriverWait(browser, 10)

        email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        email_element.click()

        send_email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        send_email_element.send_keys(wrong_email)

        password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        password_element.click()

        send_password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        send_password_element.send_keys(password)

        show_password = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".absolute > svg")))
        show_password.click()

        login_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary")))
        login_button.click()

        try:
            # Wait for the "Post new job" element
            WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[text()='Cannot find an account with those credentials']")))

        except TimeoutException:
            assert False, "Test failed due to incorrect username or password"

        # Check if "Post new job" is present after login
        assert "Cannot find an account with those credentials" in browser.page_source, "Post new job not found after login"


    @pytest.mark.usefixtures("browser")
    def test_login_case4(self, browser):
        #wrong username correct password 
        browser.get(base_url)
        wait = WebDriverWait(browser, 10)

        email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        email_element.click()

        send_email_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".w-full:nth-child(4)")))
        send_email_element.send_keys(wrong_email)

        password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        password_element.click()

        send_password_element = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".border:nth-child(1)")))
        send_password_element.send_keys(wrong_password)

        show_password = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".absolute > svg")))
        show_password.click()

        login_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary")))
        login_button.click()

        try:
            # Wait for the "Post new job" element
            WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[text()='Cannot find an account with those credentials']")))

        except TimeoutException:
            assert False, "Test failed due to incorrect username or password"

        # Check if "Post new job" is present after login
        assert "Cannot find an account with those credentials" in browser.page_source, "Post new job not found after login"


    


    