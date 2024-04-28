import re

class SentenceExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def other_custom_token(text):
        # Split the text at one or more newline characters first
        potential_sentences = re.split(r'\n+', text)
        
        # Tokenize further if the segments contain sentence-ending punctuations
        sentences = []
        pattern = r'[^.!?]+\.{1,3}|[^.!?]+[.!?]'
        for segment in potential_sentences:
            if re.search(pattern, segment):
                sentences.extend(re.findall(pattern, segment))
            else:
                sentences.append(segment)

        return [sentence.strip() for sentence in sentences if sentence.strip() != '']
    
    def get_sentences(self):
        file_path = 'C:/Dev/tst.txt'
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'utf-16']
        content = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            print("Unable to decode the file with the available encodings.")
            return []
        else:
            sentences = self.other_custom_token(content)
            
        return sentences
    
    def custom_sent_tokenize(text):
        # Split sentences using newline characters
        sentences = text.split('\n')
        
        # Merge sentences that end with punctuation and lowercase
        merged_sentences = []
        for sentence in sentences:
            if len(merged_sentences) > 0 and re.match(r'^\s*[-"\'“”‘’¿¡\(\)]*\s*\w', sentence):
                merged_sentences[-1] += " " + sentence.strip()
            else:
                merged_sentences.append(sentence.strip())
        
        return merged_sentences
    