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



# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables with default values
base_url = os.getenv("BASE_URL", "https://beta.sproutsai.com/login")
email = os.getenv("EMAIL", "pankaj+natera@sproutsai.com")
password = os.getenv("PASSWORD", "Demo@123")
home_page = os.getenv("HOME_PAGE", "https://beta.sproutsai.com/")

empty_jd_docx_file_path = os.getenv("docx_tc001", "/app/job_descriptions/empty_jds/Empty_fields_test_cases_docx/TC001 Empty PDF.docx")
empty_jd_pdf_file_path = os.getenv("pdf_tc001", "/app/job_descriptions/empty_jds/Empty_fields_test_cases_pdfs/TC001 Empty PDF.pdf")
empty_jd_txt_file_path = os.getenv("txt_tc001", "/app/job_descriptions/empty_jds/Empty_fields_test_cases_txt/TC001 Empty PDF.txt")

normal_jd_docx_file_path = os.getenv("docx_tc009", "/app/job_descriptions/must_parse_jds/Must_parse_test_cases_docx/TC009 PDF with Unexpected Page Breaks.docx")
normal_jd_pdf_file_path = os.getenv("pdf_tc009", "/app/job_descriptions/must_parse_jds/Must_parse_test_cases_pdfs/TC009 PDF with Unexpected Page Breaks.pdf")
normal_jd_txt_file_path = os.getenv("txt_tc009", "/app/job_descriptions/must_parse_jds/Must_parse_test_cases_txt/TC009 PDF with Unexpected Page Breaks.txt")






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
    def test_jobparser_empty_jd_docx(self, browser,file_path_exist=True, file_paths=empty_jd_docx_file_path):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        #upload = WebDriverWait(browser, 10).until(
            #EC.element_to_be_clickable((By.CLASS_NAME, "upload-document-first-state")))
        #upload.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(empty_jd_docx_file_path)

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

            if "Parsed" in autofill_button.text:
                company_name_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search here"][name="company"]')))

                job_title_input =  WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][name="position"]')))

                job_description_input_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="editor-class rdw-editor-main"])[2]')))

                time.sleep(2)
                job_description_input_element.click()

                # Your conditions
                condition2 = company_name_input.get_attribute('value') == ''
                condition3 = job_title_input.get_attribute('value') == ''
                condition1 = not job_description_input_element.text.strip()

                # Asserting that all conditions are true
                assert condition1 and condition2 and condition3, "Assertion failed: Conditions not met"


    @pytest.mark.usefixtures("browser")
    def test_jobparser_empty_jd_pdf(self, browser,file_path_exist=True, file_paths=empty_jd_pdf_file_path):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        #upload = WebDriverWait(browser, 10).until(
            #EC.element_to_be_clickable((By.CLASS_NAME, "upload-document-first-state")))
        #upload.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(empty_jd_pdf_file_path)

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

            if "Parsed" in autofill_button.text:
                company_name_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search here"][name="company"]')))

                job_title_input =  WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][name="position"]')))

                job_description_input_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="editor-class rdw-editor-main"])[2]')))

                time.sleep(2)
                job_description_input_element.click()

                # Your conditions
                condition2 = company_name_input.get_attribute('value') == ''
                condition3 = job_title_input.get_attribute('value') == ''
                condition1 = not job_description_input_element.text.strip()

                # Asserting that all conditions are true
                assert condition1 and condition2 and condition3, "Assertion failed: Conditions not met"


    @pytest.mark.usefixtures("browser")
    def test_jobparser_empty_jd_txt(self, browser,file_path_exist=True, file_paths=empty_jd_txt_file_path):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        #upload = WebDriverWait(browser, 10).until(
            #EC.element_to_be_clickable((By.CLASS_NAME, "upload-document-first-state")))
        #upload.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(empty_jd_txt_file_path)

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

            if "Parsed" in autofill_button.text:
                company_name_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search here"][name="company"]')))

                job_title_input =  WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][name="position"]')))

                job_description_input_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="editor-class rdw-editor-main"])[2]')))

                time.sleep(2)
                job_description_input_element.click()

                # Your conditions
                condition2 = company_name_input.get_attribute('value') == ''
                condition3 = job_title_input.get_attribute('value') == ''
                condition1 = not job_description_input_element.text.strip()

                # Asserting that all conditions are true
                assert condition1 and condition2 and condition3, "Assertion failed: Conditions not met"



    @pytest.mark.usefixtures("browser")
    def test_jobparser_docx_normal_jd(self, browser,file_path_exist=True, file_paths=normal_jd_docx_file_path):
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

                menu = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/div/div[1]/div/div/main/div[1]/div/div[1]/div[2]/button")))

                # Click the button
                menu.click()

                delete_job_element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li[text()='Delete job']")))

                time.sleep(2)

                # Click the "Edit job" element
                delete_job_element.click()

                confirm_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="custom-modal"]/div/div/div/button[1]')))

                time.sleep(2)
                # Click the "Confirm" button
                confirm_button.click()

    @pytest.mark.usefixtures("browser")
    def test_jobparser_pdf_normal_jd(self, browser,file_path_exist=True, file_paths=normal_jd_pdf_file_path):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(normal_jd_pdf_file_path)

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

                menu = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/div/div[1]/div/div/main/div[1]/div/div[1]/div[2]/button")))

                # Click the button
                menu.click()

                delete_job_element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li[text()='Delete job']")))

                time.sleep(2)

                # Click the "Edit job" element
                delete_job_element.click()

                confirm_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="custom-modal"]/div/div/div/button[1]')))

                time.sleep(2)
                # Click the "Confirm" button
                confirm_button.click()


    @pytest.mark.usefixtures("browser")
    def test_jobparser_txt_normal_jd(self, browser,file_path_exist=True, file_paths=normal_jd_txt_file_path):
        browser.get(home_page)
        # Select the element by its text content
        element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Post new job"]'))
        )
        element.click()

        if file_path_exist:
            time.sleep(2)
            file_input = browser.find_element(By.ID, 'upload')
            file_input.send_keys(normal_jd_txt_file_path)

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

                menu = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/div/div[1]/div/div/main/div[1]/div/div[1]/div[2]/button")))

                # Click the button
                menu.click()

                delete_job_element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li[text()='Delete job']")))

                time.sleep(2)

                # Click the "Edit job" element
                delete_job_element.click()

                confirm_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="custom-modal"]/div/div/div/button[1]')))

                time.sleep(2)
                # Click the "Confirm" button
                confirm_button.click()
    