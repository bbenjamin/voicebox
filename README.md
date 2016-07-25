# voicebox - placeholder readme

This does the same thing as pt-voicebox, but the lookup structure should be clearer.

The classes are structured as follows:
- a corpus has a tree of the frequencies of all n-grams up to a certain size present in a source
- a voice is a weighted combination of corpora
- a voicebox contains a list of voices, and has a user writing loop that allows for switching between them on the fly

There are several commands in the voicebox class that do things like saving, switching between voices, and changing the number of available options. These are implemented to various extents.
