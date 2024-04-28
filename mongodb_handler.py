import pymongo

class MongoDBHandler:
    def __init__(self, database_name_word, database_name_sentence):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["DuneBook"]
        self.words_db = self.db[database_name_word]
        self.sentence_db = self.db[database_name_sentence]

    def save_word(self, word, translation):
        existing_word = self.words_db.find_one({"word": word})
        if not existing_word:
            word_doc = {
                "word": word,
                "translations": translation
            }          
            self.words_db.insert_one(word_doc)

    def save_sentence(self, sentence, translation, number):
        sent_doc = {
            "sentenceNumber": number,
            "original": sentence,
            "translations": translation
        }
        self.sentence_db.insert_one(sent_doc)
    
    def check_word_in_db(self, word):
        existing_word = self.words_db.find_one({"word": word})
        return existing_word
    
    def check_sentence_in_db(self, number):
        existingSent = self.sentence_db.find_one({"sentenceNumber": number})
        return existingSent