import os
import zipfile
from words_trie import Trie
import utils


class File:

    def __init__(self, filepath):
        self.filepath = filepath
        self.sentence_list = self._load_word_arrays_from_file_sentences(filepath)


    def _load_word_arrays_from_file_sentences(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                lines_list = []
                for line in lines:
                    line_list = utils.extract_words(line)
                    if len(line_list) >= 2: lines_list.append(line_list)
            return lines_list if lines_list != [] else None
        except FileNotFoundError:
            print(f"File {filepath} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
class Data:
    
    def __init__ (self, zipfile_path, sentence_files_dir, *filetypes):

        if not filetypes: filetypes = ['.txt']
        self.sentence_files_dir = sentence_files_dir if sentence_files_dir else 'sentences_data'

        self.sentences_data = []
        self.word_set = set()
        self.word_trie = Trie()

        self._unzip_sentences_data(zipfile_path)
        self._load_sentences_data(sentence_files_dir, filetypes)
        self._create_word_set()
        self._create_word_trie()
           

    def _unzip_sentences_data(self, zipfile_path):
        if not os.path.exists(self.sentence_files_dir):
            os.makedirs(self.sentence_files_dir)
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(self.sentence_files_dir)
            print("Files extracted")


    def _load_sentences_data(self, *filetypes):
        for root, dirs, files in os.walk(self.sentence_files_dir):
            for file in files:
                if any(file.endswith(ft) for ft in filetypes):
                    filepath = os.path.join(root, file)
                    file = File(filepath)
                    if file.sentence_list is not None: self.sentences_data.append(file)
                    print(os.path.basename(filepath) + ' loaded')


    def _create_word_set(self):
         self.word_set.update([word for file_decorator in self.sentences_data for word_list in file_decorator.sentence_list for word in word_list])

    
    def _create_word_trie(self):
        for word in self.word_set: 
            self.word_trie.insert(word)



        

