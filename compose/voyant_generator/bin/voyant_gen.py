import os
import shutil
import csv
import sys
import zipfile
from time import sleep
import signal
import time


# Makes python list from inputted txt list
def make_list(keyword_path):
    with open(keyword_path, 'r') as f:
        return [line.strip() for line in f]


def voyant(keywords, text_path, corpora_path):
    # if os.path.exists(corpora_path):
    #     shutil.rmtree(corpora_path)
    # os.mkdir(corpora_path)
    print(os.listdir(corpora_path))
    for f in os.listdir(corpora_path):
        os.remove(os.path.join(corpora_path, f))
    csv_path = corpora_path
    if (not text_path.endswith('/') or not corpora_path.endswith('/')):
        raise Exception("File path must end with a /")
    keywords = make_list(keywords)
    # Matching keywords to texts and filling the directories
    filenames = os.listdir(text_path)
    for text_file in filenames:
        with open(text_path + text_file, 'r', encoding='utf-8') as text:
            text = text.read()
            for word in keywords:
                if is_in(text, word):
                    with zipfile.ZipFile(corpora_path + word.replace(' ', '_') + '.zip', 'a') as myzip:
                        if word.replace(' ', '_') + '/' + text_file not in myzip.namelist():
                            myzip.write(text_path + text_file, word.replace(' ', '_') + '/' + text_file)

    # Making csv of all the voyant urls
    fields = ('keyword', 'url')
    with open(csv_path + 'voyant.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for word in keywords:
            url_template = 'https://jl.pennds.org/?input=https://jl.pennds.org/corpora/{}'
            url = url_template.format(word.replace(' ', '_') + '.zip')
            writer.writerow({'keyword': word, 'url': url})

    print("Corpus Generation Complete")

# Function to check if a word is in a text
def is_in(text, word):
    return word in text


def main():
    def handler(signum, frame):
        sys.exit()
    signal.signal(signal.SIGTERM, handler)
    keywords = str(sys.argv[1]).strip()
    text_path = str(sys.argv[2]).strip()
    corpora_path = str(sys.argv[3]).strip()
    timestamp_cache = {}
    keyword_cache = 0;
    while True:
        with os.scandir(text_path) as it:
            for entry in it:
                print(type(entry))
                if entry.name.endswith(".txt"):
                    entry_stats = entry.stat()
                    if entry.name in timestamp_cache:
                        entry_cache_timestamp = timestamp_cache[entry.name]
                        if (entry_cache_timestamp == entry_stats.st_mtime):
                            continue
                    timestamp_cache[entry.name] = entry_stats.st_mtime
                    voyant(keywords, text_path, corpora_path)
        keywords_stats = os.stat(keywords)
        if (keyword_cache != keywords_stats.st_mtime):
            keyword_cache = keywords_stats.st_mtime
            voyant(keywords, text_path, corpora_path)
        time.sleep(90)

if __name__ == '__main__':
    main()
