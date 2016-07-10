__author__ = 'jamiebrew'

import operator

# keeps a dictionary of sources with associated weights
# TODO: a source can be a corpus or a voice (which itself points to several sources)
class voice(object):

    def __init__(self, weighted_corpora):
        self.name = 'no_name'
        self.weighted_corpora = weighted_corpora

    # aggregates the suggestion lists of all constituent corpora in this voice, prints the top num_words from this list
    def suggest(self, sentence, cursor_position, num_words):
        suggestions = {}
        for key in self.weighted_corpora:
            corp, weight = self.weighted_corpora[key]
            if not weight == 0:
                contributed_suggestions = corp.suggest(sentence, cursor_position, num_words)
                for word, score in contributed_suggestions:
                    if word not in suggestions:
                        suggestions[word] = [0, {}]
                        suggestions[word][1][corp.name] = score * weight
                    else:
                        suggestions[word][0] += score * weight
                        suggestions[word][1][corp.name] = score * weight
        suggestions = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))[0:num_words]
        return suggestions[0:num_words]

    # adds a corpus to this voice
    def add_corpus(self, corp, weight):
        self.weighted_corpora[corp.name] = [corp, weight]

    # proportionally adjusts the weights to different corpora such that they sum to 1
    def normalize_weights(self):
        total_weight = 0
        for key in self.weighted_corpora:
            total_weight += self.weighted_corpora[key][1]
        for key in self.weighted_corpora:
            self.weighted_corpora[key][1] = self.weighted_corpora[key][1] / total_weight