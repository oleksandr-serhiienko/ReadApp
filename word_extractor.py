import re
import PyPDF2
import spacy

class WordExtractor:
    def __init__(self, file_path, saved_file_path):
        self.file_path = file_path
        self.saved_file_path = saved_file_path
    
    def separate_sentence (self, text):
        #separates text into sentances. also separates \n
        nlp = spacy.load('de_core_news_sm')
        doc = nlp(text)
        result = []
        for sent in doc.sents:
            segments = re.split(r'(\n)', sent.text) 
            segments = [seg for seg in segments if seg]
            for segment in segments:
                result.append(segment)
        return result

    def convert_pdf_to_txt(self):
        with open(self.file_path, 'rb') as file:
        # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                # Extract text from the page
                text = page.extract_text()
                text = re.sub(r'^\d+', '', text, flags=re.MULTILINE)
    
                # Rule 2: Unite words split by a hyphen and newline
                text = re.sub(r'-\n', '', text)
    
                # Rule 3: Replace newlines with a space unless the line ends with certain punctuation
                text = re.sub(r'(?<=[^.!?:;\n])\n', ' ', text)

                if text.endswith("-"):
                    # Remove the last character and append a whitespace
                    formatted_text = text[:-1] 
                else:
                    # Use the original formatted_text
                    formatted_text = text + " "

                # Specify the filename where you want to save the formatted text
                filename = self.saved_file_path

                # Open the file in write mode ('w'). If the file does not exist, it will be created.
                # If it does exist, its contents will be overwritten.
                with open(filename, 'a', encoding='utf-8') as file:
                    file.write(formatted_text)
                print(text)


        # Regular expression pattern to capture sentences or newline sequences
        # This pattern is improved to handle dialogue and multiple punctuation
        pattern = r'((?<=\w[\.\?\!»])\s+)(?=[A-Z»])|((?<=[.!?»])\s+)(?=["A-Z])|([\n]+)'
    
        parts = re.split(pattern, text)
        filtered_parts = [part for part in parts if part and not part.isspace()]

        return filtered_parts
    
    def get_sentences(self):
        file_path = self.saved_file_path
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
            sentences = self.separate_sentence(content)
            
        return sentences
    
    def get_unique_words(self):
        file_path = self.saved_file_path
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
            content = content.lower()
            content = content.replace('.', '').replace(',', '').replace('!', '').replace('?', '')
            words = content.split()
            word_counts = {}
            # Remove leading and trailing non-alphanumeric characters from words
            pattern = re.compile(r'^\W+|\W+$')
            for word in words:
                if not word:
                    continue
                elif re.search(r'\d', word):
                    continue
                word = re.sub(pattern, '', word)
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

            sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1])

            for word, count in sorted_word_counts:
                print(f'{word}: {count}')
            unique_word_count = len(sorted_word_counts)
            print(f"Number of unique words: {unique_word_count}")
            return list(word_counts.keys())