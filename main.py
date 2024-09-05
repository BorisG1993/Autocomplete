import os
from data import Data
import time

    
def main():
    start_time1 = time.time()
    sentenceData = Data('sample.zip', 'sentence_files','.txt')
    end_time1 = time.time()
    start_time2 = time.time()
    sentences = sentenceData.word_trie.search_sentences('i for in range')
    end_time2 = time.time()
    print(sentences)
    load_diff = end_time1-start_time1
    search_diff = end_time2-start_time2
    print(f"seconds to load: {load_diff}")
    print(f"seconds to search: {search_diff}")

if __name__ == "__main__":
    main()