from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from languages import Language
import time

class DeeplTranslator:
    def __init__(self, driver_path):
        driver_path = r'C:\Dev\chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.wait = WebDriverWait(self.browser, 10)

    def open_deepl(self):
        
        self.browser.get("https://www.deepl.com/translator")
        language_select_elements = self.browser.find_elements(By.CLASS_NAME, "lmt__language_select__active")
        wait = WebDriverWait(self.browser, 10)

        # Wait for the "Accept all cookies" button to become clickable
        accept_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="cookie-banner-strict-accept-all"]')))
        # Click the button
        accept_button.click()
        time.sleep(20)

        try:
            # Find the button by its aria-label and click it
            button = self.browser.find_element(By.XPATH, '//button[@aria-label="Close"]')
            button.click()
            print("Button clicked successfully!")
        except Exception as e:
            print("Error clicking the button:", e)               

    def select_original_translation_languages(self, original_language: Language, translation_language: Language):
        
        button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="translator-source-lang-btn"]')))
        button_element.click()

        button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[@data-testid="translator-lang-option-{original_language.value.button_id}"]')))
        button_element.click()

        button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="translator-target-lang-btn"]')))
        button_element.click()

        button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[@data-testid="translator-lang-option-{translation_language.value.button_id}"]')))
        button_element.click()

    def translate_text(self, text):
        try:
            div_element = self.browser.find_element(By.XPATH, "//div[@contenteditable='true']")
            div_element.clear()  # Clear any existing text in the div element
            div_element.send_keys(text) 

            time.sleep(5)

            div_elements = self.browser.find_elements(By.CSS_SELECTOR, "d-textarea[name='target']")
            target_div_element = div_elements[0]  # Select the first element

            # Find the nested div element with contenteditable="true"
            nested_div_element = target_div_element.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")

            try:
                # Wait for up to 60 seconds for the text to be not empty
                WebDriverWait(self.browser, 60).until(lambda driver: nested_div_element.text.strip() != '')
                 # If this line is reached within 60 seconds, then the text is not empty
                print("Text is not empty!")

            except TimeoutException:
                # If the text is still empty after 60 seconds, this will be executed
                print("Waited for 1 minute, but the text is still empty.") 

            # Get the text from the nested div element
            # Find elements containing the words and their example sentences
            unique_words_list = []
            seen = set()
            try:
                elementAlterantive = self.browser.find_element(By.CLASS_NAME, "translation_lines")
                words = elementAlterantive.find_elements(By.CLASS_NAME, "dictLink")
                extracted_text_words = [element.text for element in words]
            except:
                extracted_text_words = []
            
            try:
                wordsAlt = self.browser.find_elements(By.XPATH, "//li/button/span[@lang='en-GB']")
                extracted_text_wordsAlt = [element.text for element in wordsAlt]
            except:
                extracted_text_wordsAlt = []
                      
            text = nested_div_element.text
            combined_list = [text] + extracted_text_wordsAlt + extracted_text_words 

            for item in combined_list:
                if item not in seen:
                    unique_words_list.append(item.strip(" ."))
                    seen.add(item)

            
            return unique_words_list
        except Exception as e:
            print(e)
            raise Exception(e)
            
            

    def quit(self):
        self.browser.quit()