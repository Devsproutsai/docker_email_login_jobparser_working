import os
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables with default values
base_url = os.getenv("BASE_URL", "https://beta.sproutsai.com/login")
email = os.getenv("EMAIL", "pankaj+natera@sproutsai.com")
password = os.getenv("PASSWORD", "Demo@123")
home_page = os.getenv("HOME_PAGE", "https://beta.sproutsai.com/")


normal_jd_docx_file_path = os.getenv("docx_tc009", "/app/job_descriptions/must_parse_jds/Must_parse_test_cases_docx/TC009 PDF with Unexpected Page Breaks.docx")
resume_file = os.getenv("resume_file", "/app/resumes/single_resume/mrudula_kulkarni.pdf")
multiples_files = os.getenv("multiples_files", "/app/resumes/multiple_resumes")

company_name = os.getenv("company_name", "truman")
job_title = os.getenv("job_title", "Senior Data Scientist and software engineer")

dynamic_text = os.getenv("job_tilte", "Senior Data Scientist and software engineer")



class TestGoogle:
    @pytest.mark.usefixtures("browser")
    def test_login(self, browser):
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
    def test_jobparser_with_resume_parser_single_file(self, browser,file_path_exist=True):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(normal_jd_docx_file_path)

            wait = WebDriverWait(browser, 80)
            autofill_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='button']/span[text()='Click to autofill']"))
            )

            document_name_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "uper-text")))
            document_name = document_name_element.text

            click_to_fill = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button']/span[text()='Click to autofill']")))
            click_to_fill.click()

            autofill_button = WebDriverWait(browser, 310).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@type='button']/span[text()='Parsed']")))

            if "Parsed" in browser.page_source:
            
                save_and_exit = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Review post"]')))
                save_and_exit.click()

                Publish = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Publish this job"]')))
                
                assert "Publish this job" in browser.page_source, "error in the job description part"

                Publish.click()

                view = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="View"]')))
                view.click()

                add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

                # Click the button
                add_candidate.click()

                time.sleep(3)
                select_file = browser.find_element(By.ID, 'resume')

                select_file.send_keys(resume_file)

                confirm_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
                confirm_button.click()

                # Wait until the text "Uploaded successfully" appears
                wait = WebDriverWait(browser, 60)
                success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

                assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"


    @pytest.mark.usefixtures("browser")
    def test_jobparser_with_resume_parser_multiple_files(self, browser,file_path_exist=True):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(normal_jd_docx_file_path)

            wait = WebDriverWait(browser, 80)
            autofill_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='button']/span[text()='Click to autofill']"))
            )

            document_name_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "uper-text")))
            document_name = document_name_element.text

            click_to_fill = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button']/span[text()='Click to autofill']")))
            click_to_fill.click()

            autofill_button = WebDriverWait(browser, 310).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@type='button']/span[text()='Parsed']")))

            if "Parsed" in browser.page_source:
            
                save_and_exit = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Review post"]')))
                save_and_exit.click()

                Publish = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Publish this job"]')))
                
                assert "Publish this job" in browser.page_source, "error in the job description part"

                Publish.click()

                view = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="View"]')))
                view.click()

                add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

                # Click the button
                add_candidate.click()
                time.sleep(3)

                select_file = browser.find_element(By.ID, 'folder')

                select_file.send_keys(multiples_files)

                confirm_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
                confirm_button.click()

                # Wait until the text "Uploaded successfully" appears
                wait = WebDriverWait(browser, 60)
                success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

                
                assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"

                


    @pytest.mark.usefixtures("browser")
    def test_resume_parser_single_file(self, browser):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cursor-pointer:nth-child(2) svg'))
        )
        element.click()

        # Select the element by its text content
        element_jobs = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@id='menu-list']/div/li/div/span"))
        )
        element_jobs.click()

        add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

        # Click the button
        add_candidate.click()

        time.sleep(3)
        select_file = browser.find_element(By.ID, 'resume')

        select_file.send_keys(resume_file)

        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
        confirm_button.click()

        # Wait until the text "Uploaded successfully" appears
        wait = WebDriverWait(browser, 60)
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

        assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"

    
    @pytest.mark.usefixtures("browser")
    def test_resume_parser_multiples_files(self, browser):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cursor-pointer:nth-child(2) svg'))
        )
        element.click()

        # Select the element by its text content
        element_jobs = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@id='menu-list']/div/li/div/span"))
        )
        element_jobs.click()

        add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

        # Click the button
        add_candidate.click()
        time.sleep(3)

        select_file = browser.find_element(By.ID, 'folder')

        select_file.send_keys(multiples_files)

        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
        confirm_button.click()

        # Wait until the text "Uploaded successfully" appears
        wait = WebDriverWait(browser, 60)
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

        
        assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"

    


    @pytest.mark.usefixtures("browser")
    def test_resume_parser_single_file_custom_job_selection(self, browser):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cursor-pointer:nth-child(2) svg'))
        )
        element.click()

        # Construct the XPath expression without the specific text
        xpath_template = "//span[text()='{}']".format(dynamic_text)

        # Select the element by its text content
        element_jobs = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_template))
        )
        element_jobs.click()

        time.sleep(3)

        add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

        # Click the button
        add_candidate.click()

        time.sleep(3)
        select_file = browser.find_element(By.ID, 'resume')

        select_file.send_keys(resume_file)

        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
        confirm_button.click()

        # Wait until the text "Uploaded successfully" appears
        wait = WebDriverWait(browser, 60)
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

        assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"


    @pytest.mark.usefixtures("browser")
    def test_resume_parser_multiple_file_custom_job_selection(self, browser):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cursor-pointer:nth-child(2) svg'))
        )
        element.click()

        # Construct the XPath expression without the specific text
        xpath_template = xpath_template = "//span[text()='{}']".format(dynamic_text)
        
        # Select the element by its text content
        element_jobs = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath_template))
        )
        element_jobs.click()

        add_candidate = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Add candidate']")))

        # Click the button
        add_candidate.click()
        time.sleep(3)

        select_file = browser.find_element(By.ID, 'folder')

        select_file.send_keys(multiples_files)

        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Upload']")))
        confirm_button.click()

        # Wait until the text "Uploaded successfully" appears
        wait = WebDriverWait(browser, 60)
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()=' Uploaded successfully']")))

        
        assert " Uploaded successfully" in browser.page_source, "Resume not uploaded successfully"
