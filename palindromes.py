#!/usr/bin/env python3
# Name  : palindromes.py
# Author: Rob Toscani
# Date  : 12-03-2024
# Description: Single-word and multi-word Palindromes-generator
#
# Algorithm:
# 0. Print eerst elk individueel woord dat aan de palindroomtest voldoet.
# 1. Laat een stroom random- (default) of alfabetisch (optioneel)
#    geordende combinaties van woorden genereren, al dan niet begrensd 
#    door maximum woord-aantal, minimum woord-lengte en totaal aantal
#    letters.
# 2. Geef optioneel als argument een reeks woorden die in de palindroom 
#    moeten zitten. Deze woorden filteren vooralsnog alleen het linkerdeel
#    van de palindromen.
# 3. De woordcombinaties aaneenschakelen tot één string en normaliseren
#    (accenten en interpunctie verwijderen, kleine letters).
# 4. Drie typen spiegelingen om het rechterdeel van het linkerdeel af
#    te leiden:
#    - type 1: rechter string is gelijk aan links omgedraaid.
#              Geen middenletter.
#    - type 2: idem als type 1, met extra letter uit de reeks a t/m z
#              (= middenletter) daarna vóór rechts geplaatst.
#    - type 3: laatste letter van links (= middenletter) afhalen vóór
#              omdraaien naar rechts.
# 5. De resulterende genormaliseerde rechter string recursief opdelen
#    in alle mogelijke partities. >> Dit is de kern van het programma <<
# 6. Tijdens het opdelen per partitie vergelijken met bestaande 
#    (genormaliseerde) woorden.
# 7. Hiervoor is een dictionary nodig met als keys unieke genormaliseerde
#    woorden en als value een lijst daaraan equivalente echte woorden,
#    incl. interpunctie, accenten en case.
# 8. Indien geen match, huidige recursie afbreken en met nieuwe partitie
#    beginnen etc.
# 9. Partitiereeksen met bij elke partitie een bestaand woord zijn
#    oplossingen voor het rechterdeel.
#
# Bug: 
# Nog zonder oplossing voor multi-word palindromen met "middenwoorden" 
# ofwel "overhangs". Deze hebben een zuivere of "scheve" symmetrie 
# (hierop is vooraf te filteren).
#
# Disclaimer: word combinations presented by this program as palindrome 
# solutions can't be expected to be grammatically correct nor to make
# sense in general.
#
# Use pypy3 for enhanced speed.
# Example with American-English words of minimally 4 characters, 
# palindrome length 18 characters, 30 results, appended to logfile:
# 	pypy3 ./palindromes.py -a -F -c30 -l4 -L18
#
# Random-methodes in Python:
# random.SystemRandom(), os.urandom() zijn zuiverder dan random.random()
# maar trager.
#
######################################################################################
#
# Copyright (C) 2024 Rob Toscani <rob_toscani@yahoo.com>
#
# palindromes.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# palindromes.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################################
#
import getopt
import sys
import re
import os
import random
import time
from string import ascii_lowercase


def to_list(file, language):
    """Convert language file to dictionarylist:"""
    if language == "g": # German language file
                        # Not UTF-8 encoded and contains superfluous text, so re-encode:
        with open(file,'r', encoding='ISO-8859-1') as language:
             dictionarylist = [word.replace("\n","") for word in language.readlines()]
        return [ slashtag.sub('', line) for line in dictionarylist if line[0] != "#" ]
    else:
        with open(file,'r') as language:
            dictionarylist = [word.replace("\n","") for word in language.readlines()]
        return dictionarylist


def normalize(string):
    """ By means of regular expressions, normalize all characters to lower case,
        remove accent marks and other non-alphanumeric characters:"""
    string = a_acc.sub('a', \
                e_acc.sub('e', \
                i_acc.sub('i', \
                o_acc.sub('o', \
                u_acc.sub('u', \
                n_til.sub('n', \
                c_ced.sub('c', \
                intpunct.sub('', string))))))))
    return string.lower()


def test_palindrome(normalized):
    """Test if word is a palindrome and meets all additional conditions:"""
    if normalized == normalized[::-1] and len(normalized) == palindrome_len and \
       max_word_qty > 0:
        if len(non_option_args) == 1:
            if normalized == norm_args:
                return True
            else:
                return False
        elif len(non_option_args) > 1:
            return False
        else:
            return True
    else:
        return False


def contains(string, characters):
    """Check if string contains any of characters:"""
    for char in characters:
        if char in string:
            return True                       # one of more of characters is in string
    return False                              # none of characters is in string


def combine(words, length_remain, non_option_args, sorted_order):
    """Combine meta-function:"""
    if min_word_len <= 0 or length_remain < min_word_len or \
       len(non_option_args) >= max_word_qty:
        if len(non_option_args):
            yield non_option_args
            return
    elif sorted_order:
        yield from combine_sorted(words, length_remain, non_option_args)
    else:
        yield from combine_random(words, length_remain, non_option_args)


def combine_sorted(wordslist, string_length, wordresult):
    """Generator of lexicographically sorted word-combinations for the left side 
       of the palindrome:"""
    for word in wordslist:
        if len(dictionary_reduced[word]) > string_length: # Length of normalized representation
            continue
        wordresult_new = wordresult + [word]
        length_remain = string_length - len(dictionary_reduced[word])
        if len(wordresult_new) == max_word_qty or length_remain < min_word_len:
            if len(non_option_args) > 0:            # If there are included words (global)
                for p in permutelist(wordresult_new):
                    yield p
            else:
                yield(wordresult_new)
        else:
            yield from combine_sorted(wordslist, length_remain, wordresult_new)
    else:
        if len(wordresult):
            yield wordresult


def combine_random(wordslist, string_length, included_words):
    """Generator of random word-combinations for the left side of the palindrome:"""
    factor = len(wordslist)
    while True:
        wordresult = [ x for x in included_words ]
        length_remain = string_length
        while True:
            index = int(random.random() * factor)
            word = wordslist[index]
            if len(dictionary_reduced[word]) > length_remain:
                continue
            wordresult = wordresult + [word]
            length_remain = length_remain - len(dictionary_reduced[word])
            if len(wordresult) == max_word_qty or length_remain < min_word_len:
                if len(included_words) > 0:   # If there are included words
                    for p in permutelist(wordresult):
                        yield p
                else:
                    yield(wordresult)
                break


def partitions(string, Tuple = ()):
    """String partition generator for the right side of the palindrome, 
       with condition-driven switches:"""
    if string == "":
        yield Tuple
        return
    # Condition:
    elif len(Tuple) >= max_word_qty:          # Skip if too many words (= substrings)
        return
    for i in range(len(string)):
        # Conditions:
        if len(string[:i+1]) < min_word_len:  # Skip at first word that's too short 
            continue
        if string[:i+1] not in normdict:      # Skip at first word that's not in 'normdict'
            continue
        yield from partitions(string[i+1:], Tuple + (string[:i+1], ))


def get_words(normlist, index, wordresult):
    """Print all word combinations for the given combinations of normalized words:"""
    for word in normdict[normlist[index]]:
        wordresult_new = wordresult + [word]
        if index < len(normlist) - 1:
            get_words(normlist, index + 1, wordresult_new)
        else:
            RightSide = ' '.join(wordresult_new)
            global count
            count += 1
            if count > maxcount:
                sys.exit()
            print(LeftSide, RightSide)
            if logmode:
                append2log(LeftSide + " " + RightSide)


def permutelist(list1, list2 = []):
    """Generate and yield all list permutations"""
    items = list1
    out = list2
    if items == []:
        yield out
        return
    previous = []
    for i in range(len(items)):
        if items[i] not in previous:
            previous.append(items[i])
            yield from permutelist(items[0:i] + items[i+1:], out + items[i:i+1])


def generate_results(norm_args):
    """Generate results by 3 types of mirroring of the normalized arguments on the left side"""
    for p in partitions(norm_args[::-1]): # Type 1: RightSide = LeftSide reversed
        get_words(p, 0, [])               # Matching palindrome word-combination

    for char in ascii_lowercase:          # Type 2: RightSide = char + (LeftSide reversed)
        norm_args_plus = norm_args + char
        for p in partitions(norm_args_plus[::-1]):    # All partitions of reversed string
            get_words(p, 0, [])

    if len(norm_args) > 1:
        norm_args_minus = norm_args[:-1]  # Type 3: RightSide = (LeftSide - char) reversed
        for p in partitions(norm_args_minus[::-1]):
            get_words(p, 0, []) 


def append2log(string):
    with open(logfile, "a") as myfile:
        myfile.write(string + "\n")


language = dictionary_nl = "/usr/share/dict/dutch"
dictionary_am = "/usr/share/dict/american-english"
dictionary_br = "/usr/share/dict/british-english"
dictionary_de = "/usr/share/hunspell/de_DE_frami.dic"
dictionary_fr = "/usr/share/dict/french"
dictionary_sp = "/usr/share/dict/spanish"
dictionary_it = "/usr/share/dict/italian"

dictionarylist  = to_list(dictionary_nl, "d")  # Dutch is default language
logfile         = "./logfile"
logmode         = 0
norm_args       = ""         # Initialization of norm_args
min_word_len    = 1
max_word_qty    = 1000 
palindrome_len  = 30         # Of *elke* lengte toestaan als optie -L niet wordt opgegeven?
excl_chars      = "0123456789"
sorted_order    = 0
count           = 0
maxcount        = 10000000

# Regular expressions:
a_acc = re.compile('[áàäâåÁÀÄÂ]')
e_acc = re.compile('[éèëêÉÈËÊ]')
i_acc = re.compile('[ïíìÏÍÌ]')
o_acc = re.compile('[óòöôøÓÒÖÔ]')
u_acc = re.compile('[úùüÚÙÜ]')
n_til = re.compile('[ñÑ]')
c_ced = re.compile('[çÇ]')
intpunct = re.compile('[\'\" :.&-]')
slashtag = re.compile('\/[^/]*')

# Text printed if -h option (help) or a non-existing option has been given:
usage = """
Usage:
palindromes.py [-abdfghiscFlLqxS] WORD(1) [ ... WORD(n)]
\t-a	American-English
\t-b	British-English
\t-d	Dutch
\t-f	French
\t-g	German
\t-h	Help (this output)
\t-i	Italian
\t-s	Spanish
\t-c COUNT
\t	Limit output to COUNT results
\t-F
\t	Write to logfile
\t-l MINWORDLEN
\t	Filter results to palindromes w/ words of at least MINWORDLEN
\t-L LENGTH
\t	Filter results to palindromes of approx. LENGTH (default 30)
\t-q MAXQTY
\t	Filter results to palindromes with <= MAXQTY words
\t-x EXCLCHARS
\t	Exclude words with any of these EXCLCHARS
\t-S	Sorted palindrome generation incl. optional WORD arg(s)
"""

# Select option(s):
try:
    options, non_option_args = getopt.getopt(sys.argv[1:], 'abdfghisc:Fl:L:q:x:S')
except:
    print(usage)
    sys.exit()

for opt, arg in options:
    if opt in ('-h'):
        print(usage)
        sys.exit()
    elif opt in ('-a'):
        dictionarylist = to_list(dictionary_am, "a")
    elif opt in ('-b'):
        dictionarylist = to_list(dictionary_br, "b")
    elif opt in ('-d'):
        dictionarylist = to_list(dictionary_nl, "d")
    elif opt in ('-f'):
        dictionarylist = to_list(dictionary_fr, "f")
    elif opt in ('-g'):
        dictionarylist = to_list(dictionary_de, "g")
    elif opt in ('-i'):
        dictionarylist = to_list(dictionary_it, "i")
    elif opt in ('-s'):
        dictionarylist = to_list(dictionary_sp, "s")
    elif opt in ('-c'):
        maxcount = int(arg)
    elif opt in ('-F'):
        logmode = 1
    elif opt in ('-l'):
        min_word_len = int(arg)
    elif opt in ('-L'):
        palindrome_len = int(arg)
    elif opt in ('-q'):
        max_word_qty = int(arg)
    elif opt in ('-x'):
        excl_chars = excl_chars + arg
    elif opt in ('-S'):
        sorted_order = 1


# Argument words must not contain characters to be excluded:
for word in non_option_args:
    if contains(word, excl_chars):
        sys.exit()

# Prevent min_word_len to be smaller than shortest word in list: 
shortest = 10
for word in dictionarylist:
    if len(word) < shortest:
        shortest = len(word)
if min_word_len < shortest:
    min_word_len = shortest

# Convert the non-option word arguments to normalized words and join together to string:
norm_args = normalize(''.join(non_option_args))    # (Filters left side of palindrome only)

# Generate word dictionary with all words per unique normalized representation:
normdict           = {} # Dictionary with key = normalized word, value = word
dictionary_reduced = {} # Reduced dictionary with key = word, value = normalized words
dictlist_reduced   = [] # Reduced wordlist

for word in dictionarylist:
    if contains(word, excl_chars):
        continue
    normalized = normalize(word)
    if len(normalized) < min_word_len:
        continue
    if test_palindrome(normalized):
        print(word)
        if logmode:
            append2log(word)
    dictionary_reduced[word] = normalized
    dictlist_reduced.append(word)
    if normalized in normdict:
        normdict[normalized].append(word)
    else:
        normdict[normalized] = [word]

# Length of remaining part of left side after subtracting normalized length of argument words: 
string_length = palindrome_len//2 - len(norm_args)  # (Relevant for automatic generation only)

# Word quantity for both palindrome halves separately:
max_word_qty = max_word_qty//2

for combination in combine(dictlist_reduced, string_length, non_option_args, sorted_order):
    LeftSide = ' '.join(combination)
    norm_args = normalize(LeftSide)
    generate_results(norm_args)
