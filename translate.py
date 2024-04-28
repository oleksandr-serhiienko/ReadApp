from selenium import webdriver
import re
import pymongo
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import nltk
from nltk.tokenize import sent_tokenize


    

    

def has_no_letters(s):
    return not any(c.isalpha() for c in s)



chrome_driver_path = r'C:\Dev\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver_path)
browser.get("https://www.deepl.com/translator")
language_select_elements = browser.find_elements(By.CLASS_NAME, "lmt__language_select__active")
wait = WebDriverWait(browser, 10)
# Wait for the "Accept all cookies" button to become clickable
accept_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="cookie-banner-strict-accept-all"]')))

# Click the button
accept_button.click()

client = pymongo.MongoClient("mongodb://localhost:27017")
# Create a database
db = client["Application"]
words_collection = db["wordLittlePrinceEspEn"]
sentence_collection = db["sentenceLittlePrinceEspEn"]
words = GetUniqueWords()
sentences = GetSentences()
if len(language_select_elements) > 1:
    language_select_elements[0].click()
        # Find the button element with the specified data-testid attribute and text
    #button_element = browser.find_element(By.XPATH, '//button[@data-testid="translator-lang-option-de"]/span[text()="German"]')
button_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="translator-lang-option-es"]/span[text()="Spanish"]')))
button_element.click()

language_select_elementsNew = browser.find_elements(By.CLASS_NAME, "lmt__language_select__active")
    # Access the element at index 1 and click on it
if len(language_select_elementsNew) > 1:
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "lmt__language_select__active")))
        # element.click()
element = elements[1]
actions = ActionChains(browser)
actions.move_to_element(element).click().perform()
        
    # Find the button element with the specified data-testid attribute and text
    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="translator-lang-option-en-GB"]/span[text()="English (British)"]'))).click()
    # button_elementNew = browser.find_element(By.XPATH, '//button[@data-testid="translator-lang-option-en-GB"]/span[text()="English (British)"]')
elementNew = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="translator-lang-option-en-GB"]/span[text()="English (British)"]')))
    # Click the button element
actions = ActionChains(browser)
actions.move_to_element(elementNew).click().perform()
# Access the element at index 1 and click on it
# for word in words:
#     existing_word = words_collection.find_one({"word": word})
#     if existing_word:
#         continue
#     if not word.strip():
#         continue
#     try:
#         div_element = browser.find_element(By.XPATH, "//div[@contenteditable='true']")
#         div_element.clear()  # Clear any existing text in the div element
#         div_element.send_keys(word) 

#         time.sleep(5)


#         div_elements = browser.find_elements(By.CLASS_NAME, "lmt__inner_textarea_container")
#         target_div_element = div_elements[1]  # Select the first element

#         # Find the nested div element with contenteditable="true"
#         nested_div_element = target_div_element.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")

#         # Get the text from the nested div element
#         text = nested_div_element.text

#         word_doc = {
#             "word": word,
#             "translations": text
#         }
#         words_collection.insert_one(word_doc)
#     except Exception as e:
#         continue
i = 0
for sentence in sentences:
    i += 1
    existing_sentence = sentence_collection.find_one({"sentenceNumber": i})
    empty = not sentence 
    hasNoLetter = has_no_letters(sentence)
    if existing_sentence or empty or hasNoLetter:
        continue
    try:
        div_element = browser.find_element(By.XPATH, "//div[@contenteditable='true']")
        div_element.clear()  # Clear any existing text in the div element
        div_element.send_keys(sentence) 

        time.sleep(5)


        div_elements = browser.find_elements(By.CLASS_NAME, "lmt__inner_textarea_container")
        target_div_element = div_elements[1]  # Select the first element

        # Find the nested div element with contenteditable="true"
        nested_div_element = target_div_element.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")

        try:
        # Wait for up to 60 seconds for the text to be not empty
            WebDriverWait(browser, 60).until(
            lambda driver: nested_div_element.text.strip() != ''
            )
        # If this line is reached within 60 seconds, then the text is not empty
            print("Text is not empty!")

        except TimeoutException:
            # If the text is still empty after 60 seconds, this will be executed
            print("Waited for 1 minute, but the text is still empty.")
            GetSentences()

        # Get the text from the nested div element
        text = nested_div_element.text
        
        sent_doc = {
            "sentenceNumber": i,
            "original": sentence,
            "translations": text
        }
        sentence_collection.insert_one(sent_doc)
    except Exception as e:
        continue
browser.quit() 
