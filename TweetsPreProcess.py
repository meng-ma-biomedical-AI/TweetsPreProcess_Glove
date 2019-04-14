#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
preprocess-twitter.py (https://gist.github.com/tokestermw/cb87a97113da12acb388)
python preprocess-twitter.py "Some random text with #hashtags, @mentions and http://t.co/kdjfkdjf (links). :)"
Script for preprocessing tweets by Romain Paulus
with small modifications by Jeffrey Pennington
with translation to Python by Motoki Wu
Translation of Ruby script to create features for GloVe vectors for Twitter data.
http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb
"""

import sys
import re
from ftfy import fix_text
import string

FLAGS = re.MULTILINE | re.DOTALL
nonvalid_characters_p = re.compile("[^a-zA-Z0-9#\*\-_\s]")

class TweetsPreProcess:

    def re_sub(self, pattern, repl, text):
        return re.sub(pattern, repl, text, flags=FLAGS)


    def hashtag(self, text):
        text = text.group()
        
        return text[1:] + " <hashtag> "


    def hashtag_converter(self, text):
        return self.re_sub(r"#\S+", self.hashtag, text)


    def abbr_restore(self, text):
        text = self.re_sub("i\'ve", "i have", text)
        text = self.re_sub("n\'t", " not", text)
        text = self.re_sub("i\'d like", "i would like", text)
        text = self.re_sub("i\'d (?!like)", "i had ", text)
        text = self.re_sub("that\'s", "that is", text)
        text = self.re_sub("it\'s", "it is", text)    
        return text


    def alpha_and_number_only(self, text):
        text = re.sub(nonvalid_characters_p, ' ', text)
        return text

    def pop_words_transformation(self, text):
        text = self.re_sub(r'ha[ha]+', '<symbollaugh>', text)
        text = self.re_sub(r'hua[hua]+', '<symbollaugh>', text)
        text = self.re_sub(r'ja[ja]+', '<symbollaugh>', text)
        text = self.re_sub(r'ja[ja]+j', '<symbollaugh>',text)
        text = self.re_sub(r'kno[o]+w', 'know', text)
        text = self.re_sub(r'goo[o]+d', 'good', text)
        text = self.re_sub(r'tir[r]+e[e]+d', 'tired', text)
        return text

    def remove_punctuation(self, text):
        text = self.re_sub(r'(\.|\?|;|!|,|~)(\s+|$)', ' ', text)

        return text 

    def url_converter(self, text):
        text = self.re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>", text)
        return text

    def user_converter(self, text):
        return self.re_sub(r"@\w+", " <user> ", text)

    def emoji_converter(self, text):
        eyes = r"[8:=;]"
        nose = r"['`\-]?"
        text = self.re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), " <smile> ", text)
        text = self.re_sub(r"{}{}p+".format(eyes, nose), " <lolface> ", text)
        text = self.re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), " <sadface> ", text)
        text = self.re_sub(r"{}{}[\/|l*]".format(eyes, nose), " <neutralface> ", text)
        text = self.re_sub(r"<3"," <heart> ", text)
        return text    

    def num_converter(self, text):
        return re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " <number> ", text)

    def allcaps(self, text):
        text = text.group()
        return text.lower() + " <allcaps>"

    def allcaps_converter(self, text):
        return self.re_sub(r"([A-Z]){2,}", self.allcaps, text)


    def special_repeat_converter(self, text):
        text = self.re_sub(r"([!?.]){2,}", r"\1 <repeat> ", text)
        text = self.re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong> ", text)
        return text


    def clean_text(self, text):
        non_ascii_p = re.compile(r'[^\x00-\x7F]+')
        text = fix_text(text.replace('\r\n',' ').replace('\n',' ').replace('\r',' '))

        text = re.sub(non_ascii_p, '', text)

        return text.strip()

    def sanitize(self, text_list):
        result = []
        for text in text_list:
            text = self.clean_text(text)
            text = self.url_converter(text)
            text = self.re_sub(r"/"," / ", text)    
            text = self.user_converter(text)
            text = self.hashtag_converter(text)
            text = self.allcaps_converter(text)
            text = self.remove_punctuation(text)
            result.append(text.strip())

        return result

    def sanitize_nofunccall(self, text_list):
        result = []
        for text in text_list:
            text = self.clean_text(text)
            text = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>", text, flags=FLAGS)
            text = re.sub(r"/"," / ", text, flags=FLAGS)
            text = re.sub(r"@\w+", " <user> ", text, flags=FLAGS)
            text = re.sub(r"#(\S+)", self.hashtag, text, flags=FLAGS)
            text = re.sub(r"([A-Z]){2,}", self.allcaps, text, flags=FLAGS)
            text = re.sub(r'(\.|\?|;|!|,|~)(\s+|$)', ' ', text, flags=FLAGS)
            result.append(text.strip())
        return result

if __name__ == '__main__':

    text_list = ["I TEST alllll kinds of #whatever and #HASHTAGS, @mentions 300,000 1.5 and 3000 (http://t.co/dkfjkdf). w/ <3 :) haha!!!!!"]
    test_tpp = TweetsPreProcess()
    print(test_tpp.sanitize(text_list))
    # logger.info(sanitize(text))
    # logger.info(sanitize_nofunccall(text))
