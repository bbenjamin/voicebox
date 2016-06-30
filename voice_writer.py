__author__ = 'jamiebrew'

import os
import corpus
import operator
import textwrap
import random
import re
import voice
import string

"""
input loop for writing with a corpus or set of corpora
"""
class writer(object):

    def __init__(self, hindsight = 3, foresight = 3):
        self.cursor = "|"
        self.voices = {}
        self.corpora = {}
        self.pronouncing_dictionary = 0

    def header(self):
        headerString = "\nVOICES\n"
        vnum = 1
        for corpus in sorted(self.corpora):
            headerString += 'v%s. %s\n' % (str(vnum), self.corpora[corpus].name)
            vnum+=1
        headerString += "\n____________________"
        return headerString

    def biggest_characters(self, tname, number):
        size_by_name = {}
        tpath = 'texts/transcripts/%s' % tname
        for cname in os.listdir(tpath):
            cpath = '%s/%s' % (tpath, cname)
            size_by_name[cname] = len(file(cpath).read().split())
        sorted_chars = list(reversed(sorted(size_by_name.items(), key=operator.itemgetter(1))))
        return sorted_chars[0:number]

    def write(self):
        #self.load_corpora()
        self.load_voices()
        #self.load_corpora_from_transcript('got', 25)
        #active_corpus = self.choose_corpus()
        active_voice = self.choose_voice()
        sentence = ['START_SENTENCE']
        cursor_position = 1
        #corpus_NAME = active_corpus.name.upper() + ':'
        #log = [corpus_NAME]
        voice_name = active_voice.name.upper()
        log = [voice_name]

        while 1:
            words_before = sentence[0:cursor_position]
            words_after = sentence[cursor_position:]
            suggestions = active_voice.suggest(sentence, cursor_position, 20)
            #suggestions = active_corpus.suggest(sentence, cursor_position, 20)
            print suggestions[0][0] == ''
            print len(suggestions[0])
            print self.header()
            print textwrap.fill(" ".join(log + words_before[1:] + [self.cursor] + words_after),80)
            self.display_suggestions(suggestions)

            input = raw_input('What now?\n')
            
            try:
                input = int(input)
            except:
                pass
            
            if input in range(1, len(suggestions)+1):
                next_word = self.take_suggestion(suggestions, input)
                words_before.append(next_word)
                sentence = words_before + words_after
                cursor_position += 1
            elif input == 0:
                log = log + sentence
                log.remove('START_SENTENCE')
                print " ".join(log)
                return    
            elif input == 'z':
                cursor_position -= 1
            elif input == 'c':
                cursor_position +=1
            elif input == 'x':
                self.delete_word(words_before)
                cursor_position -= 1
                sentence = words_before+words_after
            elif input == 'r':
				next_word = self.weighted_random_choice(suggestions)
				words_before.append(next_word)
				sentence = words_before + words_after
				cursor_position += 1
            elif not re.compile('v[0-9]').search(input) == None: # switch to different corpus
                voice_num = input[1:]
                corpus_keys = sorted(self.corpora.keys())
                active_corpus = self.corpora[corpus_keys[int(voice_num) - 1]]
                print '%s chosen!' % active_corpus.name
                finished_sentence = self.finish_sentence(words_before, words_after, '.', '\n\n')
                log = log + [finished_sentence] + [active_corpus.name.upper() + ':']
                sentence = ['START_SENTENCE']
            elif input in ['.', '?','!']:
                finished_sentence = self.finish_sentence(words_before, words_after, input)
                log = log + [finished_sentence]
                sentence = ['START_SENTENCE']
            elif isinstance(input, str) and len(input.strip()) > 0:
                words_before.append(input)
                sentence = words_before + words_after
                cursor_position += 1
            else:
                print "Invalid input."

    # returns a word from the suggestion list; choice weighted according to scores
    def weighted_random_choice(self, suggestions):
        total = sum(weight for word, weight in suggestions)
        r = random.uniform(0,total)
        upto = 0
        for word, weight in suggestions:
            if upto + weight >= r:
                return word
            upto += weight
        assert False, "Shouldn't get here"
    
    # random choice without weight bias
    def flat_random_choice(self, suggestions):
        choice = random.randint(1, len(suggestions))
        return choice

    # deletes word before the cursor from sentence
    def delete_word(self, before):
        if len(before) == 1:
            print "Cannot delete the start of the sentence!"
        else:
            del before[-1] # remove last element of current line

    #
    def finish_sentence(self, before, after, delimiter, line_break = ''):
        sentence = before[1:] + after
        if len(sentence) > 0:
            sentence[-1] += delimiter
        sentence += line_break
        return " ".join(sentence)

    def load_corpora_from_transcript(self, tname, number):
        for pair in self.biggest_characters(tname, number):
            charname = pair[0]
            print charname
            path = 'texts/transcripts/%s/%s' % (tname, charname)
            self.corpora[charname] = corpus.corpus(path, charname)

    def load_corpora(self):
        texts = os.listdir('texts')
        add_another = ''
        while add_another != 'n':
            for i in range(len(texts)):
                print "%s %s" % (i + 1, texts[i])

            choice = raw_input('Enter the number of the corpus you want to load:\n')

            corpus_name = texts[int(choice) - 1]
            path = 'texts/%s' % corpus_name
            self.corpora[corpus_name] = corpus.corpus(path, corpus_name)
            # removes from list of possible corpora to add on next cycle
            texts.remove(corpus_name)
            print "added %s!" % corpus_name
            #add_another = raw_input('Load another voice? y/n\n')
            add_another = 'n'

    def load_voices(self):
        texts = os.listdir('texts')
        paths_names_weights = []
        add_another_voice = ''
        while add_another_voice != 'n':
            add_another_corpus = ''
            while add_another_corpus != 'n':
                for i in range(len(texts)):
                    print "%s %s" % (i + 1, texts[i])

                choice = raw_input('Enter the number of the corpus you want to load:\n')
                corpus_name = texts[int(choice) - 1]
                path = 'texts/%s' % corpus_name
                name = corpus_name
                weight = float(raw_input('Enter the weight for this corpus:\n'))
                paths_names_weights.append((path, name, weight))
                add_another_corpus = raw_input('Add another corpus to this voice? y/n\n')
            voicename = raw_input('Name this voice:\n')
            self.voices[voicename] = voice.voice(paths_names_weights, voicename)
            add_another_voice = raw_input('Add another voice? y/n\n')

    # offers several corpus choices. returns a corpus
    def choose_corpus(self):
        corpus_keys = sorted(self.corpora.keys())
        print "CORPUS KEYS",corpus_keys
        for i in range(len(corpus_keys)):
            print "%s: %s" % (i + 1, corpus_keys[i])
        choice = raw_input('Choose a corpus to write with...\n')
        active_corpus = self.corpora[corpus_keys[int(choice) - 1]]
        return active_corpus

    # offers several voice choices, returns a voice
    def choose_voice(self):
        voice_keys = sorted(self.voices.keys())
        print "VOICE KEYS:", voice_keys
        for i in range(len(voice_keys)):
            print "%s: %s" % (i + 1, voice_keys[i])
        choice = raw_input('Choose a voice to write with...\n')
        active_voice = self.voices[voice_keys[int(choice) - 1]]
        return active_voice

    def display_suggestions(self, suggestions):
        for i in range(len(suggestions)):
            print "%s: %s" % (i + 1, suggestions[i][0])

    def take_suggestion(self, suggestions, input):
        chosen_number = input
        selection = suggestions[int(chosen_number) - 1][0]
        return selection

w = writer()
w.write()