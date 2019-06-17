import os
import shutil
import csv
import sys


# Makes python list from inputted txt list
def make_list(keyword_path):
    with open(keyword_path, 'r') as f:
        return [line.strip() for line in f]


def voyant(keywords, key_path, text_path, corpora_path, csv_path):
    if (not key_path.endswith('/') or not text_path.endswith('/') or not corpora_path.endswith('/')):
        raise Exception("File path must end with a /")

    keywords = make_list(keywords)

    # Making a directory for all the keywords
    for word in keywords:
        if ' ' in word:
            os.mkdir(key_path + word.replace(' ', '_'))
        else:
            os.mkdir(key_path + word)

    # Matching keywords to texts and filling the directories
    filenames = os.listdir(text_path)
    for text_file in filenames:
        with open(text_path + text_file, 'r', encoding='utf-8') as text:
            text = text.read()
            for word in keywords:
                if is_in(text, word):
                    if (' ' in word):
                        shutil.copy(text_path + text_file, key_path + word.replace(' ', '_'))
                    else:
                        shutil.copy(text_path + text_file, key_path + word)

    # Zipping files and moving them to corpora
    for word in keywords:
        if (' ' in word):
            shutil.make_archive(corpora_path + word.replace(' ', '_'), 'zip', key_path, word.replace(' ', '_'))
        else:
            shutil.make_archive(corpora_path + word, 'zip', key_path, word)

    # Making csv of all the voyant urls
    fields = ('keyword', 'url')
    with open(csv_path + 'voyant.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for word in keywords:
            url_template = 'https://jl.pennds.org/?input=https://jl.pennds.org/corpora/{}'
            url = url_template.format(word.replace(' ', '_') + '.zip')
            writer.writerow({'keyword': word, 'url': url})


# Function to check if a word is in a text
def is_in(text, word):
    return word in text


def main():
    keyword = str(sys.argv[1]).strip()
    key_path = str(sys.argv[2]).strip()
    text_path = str(sys.argv[3]).strip()
    corpora_path = str(sys.argv[4]).strip()
    csv_path = str(sys.argv[5]).strip()
    voyant(keyword, key_path, text_path, corpora_path, csv_path)
    print("Wow, it actually worked!")


if __name__ == '__main__':
    main()
