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
    temp_time = 0
    recent_time = 0
    while True:
        for text in os.listdir(text_path):
            if os.path.getmtime(os.path.join(text_path,text)) > recent_time:
                recent_time = os.path.getmtime(os.path.join(text_path, text))
        if os.path.getmtime(keywords) > recent_time:
            recent_time = os.path.getmtime(keywords)
        if recent_time > temp_time:
            temp_time = recent_time
            voyant(keywords, text_path, corpora_path)
        print("SLEEPING FOR A BIT")
        time.sleep(10)

if __name__ == '__main__':
    main()
