from enum import Enum

class LanguageInfo:
    def __init__(self, button_id, iso_code, spacy_rule):
        self.button_id = button_id
        self.iso_code = iso_code
        self.spacy_rule = spacy_rule

class Language(Enum):
    English = LanguageInfo('en-GB', 'en', 'en_core_web_sm')
    Spanish = LanguageInfo('es', 'es', '')
    French = LanguageInfo('fr', 'fr', '')
    German = LanguageInfo('de', 'de', 'de_core_news_sm')