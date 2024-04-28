from deepl_translator import DeeplTranslator  
from mongodb_handler import MongoDBHandler
from sentence_extractor import SentenceExtractor
from word_extractor import WordExtractor
from languages import Language
import re

class Main:
    def __init__(self):
        self.translator = DeeplTranslator(r'C:\Project\myenv\chromedriver.exe')
        self.word_extractor = WordExtractor(r'C:\Users\Serhi\Downloads\pdfcoffee.com_frank-herbert-dune-der-wuestenplanet-pdf-pdf-free.pdf', r'C:\Users\Serhi\Downloads\formatted_text.txt')
        self.mongodb = MongoDBHandler("wordsGeEn", "sentenceGeEn")


    
    def run(self):
        #self.word_extractor.convert_pdf_to_txt()
        self.translator.open_deepl()
        self.translator.select_original_translation_languages(Language.German, Language.English)
        self.processWords()
        self.processSentece()    
        self.translator.quit()

    def processSentece(self):
        senNum = 0
        sentences = self.word_extractor.get_sentences()      
        for sentence in sentences:
            senNum = senNum + 1
            try:
                if (not self.mongodb.check_sentence_in_db(senNum)):
                    if(not self.is_one_word(sentence)):
                        translated_text = self.translator.translate_text(sentence)
                        if (translated_text):
                            self.mongodb.save_sentence(sentence, translated_text, senNum)
                    else:
                        self.mongodb.save_sentence(sentence, sentence, senNum)
            except:
                self.translator.quit()
                main_app = Main()
                main_app.run()


    def processWords(self):
        words = self.word_extractor.get_unique_words()
        for word in words:
            try:
                # Translate the text
                if (not self.mongodb.check_word_in_db(word) and word):
                    translated_text = self.translator.translate_text(word)
                    if (translated_text):
                        self.mongodb.save_word(word, translated_text)
            except Exception as e:
                self.translator.quit()
                main_app = Main()
                main_app.run()

    def is_one_word(selfe, sentence):
        if sentence.strip() == '':
            return True
        words = sentence.split()
        return len(words) == 1
        
if __name__ == "__main__":
    main_app = Main()
    main_app.run()