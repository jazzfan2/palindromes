#!/usr/bin/env python3
# Name  : palindromes.py
# Author: Rob Toscani
# Date  : 29-03-2024
# Description: Single-word and multi-word Palindromes-generator
#
# Algorithm:
# 1. Limit the word database by omitting all words that are too short or
#    that contain excluded characters.
# 2. If any 'search-words' are given, these are placed in advance, the
#    first one as the 'mid-word', any others on the available positions
#    on the 'primary side';
# 3. If no 'search-words' are given, select an empty string or a word
#    from the dictionary list as the 'mid-word';
# 4. Place it in the middle of the palindrome around each of its
#    symmetrical substrings at beginning or end, as represented by
#    pre-determined 'skew' values;
# 5. Pick words from the dictionary list, in random or alphabetical
#    order; place as many that fit on the positions on the primary
#    side within total length and word quantity bounds, and if
#    not already occupied by search words;
# 6. Permute the primary word combination if it contains search-words;
# 7. Normalize each primary word combination (lower case, accent marks
#    and punctuation removed) and remove the spaces;
# 8. Mirror the part on the primary side plus the 'skew' part of the
#    middle word to the secondary side;
# 9. Recursively divide the resulting normalized secondary string
#    into all possible substring partitions;
# 10. While dividing, compare each partition with all existing unique
#     normalized words;
# 11. These are looked up as keys in a dictionary. If a match is found,
#     all associated real words (including punctuation, accent marks
#     and case) are a candidate for placement on that position;
# 12. If no match is found, abort the current recursion, backtrack to
#     the latest match, and create new partitions from there, etc.;
# 13. If each and every partition of a string matches an existing word,
#     the full string qualifies as a solution for the secondary side;
# 14. Deduce from the sign of the midword skew which of the primary and
#     secondary parts comes on the left and which on the right;
# 15. Position the primary and secondary parts around the middle word
#     accordingly to generate the palindrome result.
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
import math
import re
import random


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


def contains(string, characters):
    """Check if string contains any of characters:"""
    for char in characters:
        if char in string:
            return True          # one of more of characters is in string
    return False                 # none of characters is in string


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


def get_skews(string):
    """Get all 'skews' of a string, being the number of characters that must be removed
       at either end to result into the remaining (end)string being symmetric:"""
    skews = []
    for s in range(0, len(string)):
        l = len(string)
        if string[:l-s] == string[:l-s][::-1]:
            skews.append(-s)      # Skew = negative if chars are removed from the right
        if s > 0 and string[s:] == string[s:][::-1]:
            skews.append(s)       # Skew = positive if chars are removed from the left
    return skews                  # List of skews, sorted by increasing absolute value


def combine(wordslist, total_len, search_words):
    """Mid-word and search-words (pre-)combinator:"""
    midword_mode = 1        # If midword_mode = 1, palindrome includes a midword, else not
    restricted = 0          # If restricted (= 1), midword won't use a search word
    i = -1                  # Wordslist index initialization
    j = 0                   # Search-word list index initialization
    while True:
        search_remain = [ x for x in search_words ]   # Remaining search words
        if sorted_order:                              # Option -S (sorted order)
            i += 1                                    # Incremental wordslist index,
        else:
            i = int(random.random() * len(wordslist)) # Random wordslist index,
        if midword_mode:
            if len(search_words) == 0 or restricted:
                midword = wordslist[i]                # Pick from dictionary list
            else:
                midword = search_words[j]             # Pick from search words
                search_remain.remove(search_words[j])
            # Available word quantity for primary side, minus midword:
            max_qty = (max_word_qty - 1) // 2
        else:
            midword = ""
            # Available word quantity for primary side, if no midword:
            max_qty = max_word_qty // 2
        w = len(dictionary_reduced[midword])
        # Place the midword in the middle by all of its symmetry centers, by varying 'skew':
        for s in symmetry_skews[midword]:
            # Verify if the midword fits within the palindrome length:
            if (w % 2 == s % 2 and (w - abs(s))//2 + abs(s) > total_len//2) or \
                   (w % 2 != s % 2 and (w - abs(s))//2 + abs(s) > (total_len - 1)//2):
            # Skews are sorted by rising absolute value, so we can quit loop once 1x false:
                break
            # Calculate remaining length for the words on the primary side:
            length_remain = (total_len - w - abs(s)) // 2
            wordresult = []
            # Pre-fill the primary side with as many remaining and fitting search-words:
            for k in range(len(search_remain)):
                if len(wordresult) == max_qty:
                    break
                if length_remain >= len(dictionary_reduced[search_remain[k]]):
                    wordresult.append(search_remain[k])
                    length_remain = length_remain - len(dictionary_reduced[search_remain[k]])
                else:
                    continue
            # Stop if none of the search words fits the primary side nor matches the midword:
            if len(search_words) and midword not in search_words and not len(wordresult):
                break

            # Call the appropriate word combinator for the primary side:
            if sorted_order:
                yield from combine_sorted(wordslist, length_remain, wordresult,
                                          len(wordresult), midword, s, max_qty)
            else:
                yield from combine_random(wordslist, length_remain, wordresult,
                                          len(wordresult), midword, s, max_qty)

        # Throw switches to decide whether of not to place a midword in the next palindrome:
        midword_mode = (midword_mode + 1) % 5   # Choice: skip midword after each 5 midwords

        # ... and whether or not to place a search-word in the middle of the next palindrome:
        if len(search_words) and midword_mode:
            restricted = (restricted + 1) % length_ratio
            if not restricted:
                j = (j + 1) % len(search_words) # The search words are available for the midword


def combine_sorted(wordslist, string_length, wordresult, searchcount, midword, s, max_qty):
    """Generator of lexicographically sorted word-combinations for the primary side
       of the palindrome:"""
    for word in wordslist:
        if len(dictionary_reduced[word]) > string_length: # Length of normalized representation
            continue
        wordresult_new = wordresult + [word]
        if len(wordresult_new) > max_qty:
            return
        length_remain = string_length - len(dictionary_reduced[word])
        if length_remain < min_word_len:
            if searchcount:    # If primary side contained search words when function was called
                for permutation in permutelist(wordresult_new):
                    yield (permutation, midword, s)
            else:
                yield (wordresult_new, midword, s)
        else:
            yield from combine_sorted(wordslist, length_remain, wordresult_new, \
                                      searchcount, midword, s, max_qty)
    else:
        if len(wordresult) or len(midword):
            yield (wordresult, midword, s)


def combine_random(wordslist, length_remain, wordresult, searchcount, midword, s, max_qty):
    """Generator of random word-combinations for the primary side of the palindrome:"""
    while True:
        if length_remain < min_word_len:
            if len(wordresult) or len(midword):
                if searchcount:    # If primary side contains search words
                    for permutation in permutelist(wordresult):
                        yield (permutation, midword, s)
                else:
                    yield (wordresult, midword, s)
            break
        i = int(random.random() * len(wordslist))
        word = wordslist[i]
        if len(dictionary_reduced[word]) > length_remain:
            continue
        wordresult = wordresult + [word]
        if len(wordresult) > max_qty:
            break
        length_remain = length_remain - len(dictionary_reduced[word])


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


def partitions(string, Tuple = ()):
    """String partition generator for the secundary side of the palindrome,
       with condition-driven switches:"""
    if string == "":
        yield Tuple
        return
    # Quantity conditions:
    elif len(midword) == 0 and len(Tuple) >= max_word_qty // 2:
        return
    elif len(midword) > 0  and len(Tuple) >= (max_word_qty - 1) // 2:
        return                                    # Skip if too many words (= substrings)
    for i in range(len(string)):
        # Length and existence conditions:
        if len(string[:i+1]) < min_word_len:      # Skip at first word that's too short
            if string[:i+1] not in norm_args_set: # ... unless it's a search word!
                continue
        if string[:i+1] not in normdict:          # Skip at first word that's not in 'normdict'
            continue
        yield from partitions(string[i+1:], Tuple + (string[:i+1], ))


def make_palindromes(norm_partition_list, index, wordresult):
    """Generate palindromes from primary words, midword and normalized secundary partitions:"""
    for word in normdict[norm_partition_list[index]]:
        wordresult_new = wordresult + [word]      # Get secundary words from partitions
        if index < len(norm_partition_list) - 1:
            make_palindromes(norm_partition_list, index + 1, wordresult_new)
        else:
            secundary = ' '.join(wordresult_new)
            global count
            count += 1
            if count > maxcount:
                sys.exit()
            space1 = (len(primary) != 0) * " "
            space2 = (len(midword) != 0) * " "
            space3 = (len(secundary) != 0) * " "
            if skew >= 0:
                print_palindrome(primary + space1 + midword + space2 + secundary)
                if skew == 0:
                    print_palindrome(secundary + space3 + midword + space2 + primary)
            else:
                print_palindrome(secundary + space3 + midword + space2 + primary)


def print_palindrome(string):
    """Write results to standard output and optionally to logfile:"""
    print(string)
    if logmode:
        with open(logfile, "a") as myfile:
            myfile.write(string + "\n")


dictionary_nl = "/usr/share/dict/dutch"
dictionary_am = "/usr/share/dict/american-english"
dictionary_br = "/usr/share/dict/british-english"
dictionary_de = "/usr/share/hunspell/de_DE_frami.dic"
dictionary_fr = "/usr/share/dict/french"
dictionary_sp = "/usr/share/dict/spanish"
dictionary_it = "/usr/share/dict/italian"

dictionarylist  = to_list(dictionary_nl, "d")  # Dutch is default language
logfile         = "./logfile"
logmode         = 0
min_word_len    = 1
max_word_qty    = 1000
total_len       = 30           # Or allow *each* length if option -L is not given?
excl_chars      = "0123456789"
sorted_order    = 0
count           = 0
maxcount        = math.inf

# Regular expressions:
a_acc = re.compile('[áàäâåÁÀÄÂ]')
e_acc = re.compile('[éèëêÉÈËÊ]')
i_acc = re.compile('[ïíìÏÍÌ]')
o_acc = re.compile('[óòöôøÓÒÖÔ]')
u_acc = re.compile('[üûÜÛ]')
n_til = re.compile('[ñÑ]')
c_ced = re.compile('[çÇ]')
intpunct = re.compile('[\'\" :.&-]')
slashtag = re.compile('\/[^/]*')

# Text printed if -h option (help) or a non-existing option has been given:
usage = """
Usage:
palindromes.py [-abdfghiscFlLqxS] [WORD(1) [ ... WORD(n)]]
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
\t-F	Write output to logfile
\t-l MINWORDLEN
\t	Filter results to palindromes w/ words of at least MINWORDLEN
\t-L LENGTH
\t	Filter results to palindromes of approx. LENGTH (default 30)
\t-q MAXQTY
\t	Filter results to palindromes with <= approx. MAXQTY words
\t-x EXCLCHARS
\t	Exclude words with any of these EXCLCHARS
\t-S	Sorted palindrome generation
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
        total_len = int(arg)
    elif opt in ('-q'):
        max_word_qty = int(arg)
    elif opt in ('-x'):
        excl_chars = excl_chars + arg
    elif opt in ('-S'):
        sorted_order = 1


# Prevent negative min_word_len, total_len < min_word_len or max word quantity < 1:
if min_word_len <= 0 or total_len < min_word_len or max_word_qty < 1:
    sys.exit()

# Prevent min_word_len to be smaller than shortest word in list:
shortest = 10
for word in dictionarylist:
    if len(word) < shortest:
        shortest = len(word)
if min_word_len < shortest:
    min_word_len = shortest

# Convert the non-option word arguments to normalized words and join together to string:
norm_args = normalize(''.join(non_option_args))

# Length ratio between half palindrome and search string, to be used in combine() function:
if len(non_option_args):
    length_ratio = max(1, total_len//(2*len(norm_args)))

# Generate word dictionary with all words per unique normalized representation:
normdict           = {}    # Dictionary with key = normalized word, value = list of words
symmetry_skews     = {}    # Symmetry 'skews' dictionary
dictionary_reduced = {}    # Reduced dictionary with key = word, value = normalized word
dictlist_reduced   = []    # Reduced wordlist
norm_args_set      = set() # Set of normalized non_option_args

# The empty midword has one 'skew': 0
symmetry_skews[""] = [0]

# The empty (normalized) word:
dictionary_reduced[""] = ""

# Prepare all databases:
for word in dictionarylist + non_option_args:
    total_len_fault = 0
    if contains(word, excl_chars):
        if word in non_option_args:
            sys.exit()
        continue
    normalized = normalize(word)
    if len(normalized) > total_len or (max_word_qty == 1 and len(normalized) < total_len):
        total_len_fault = 1
    if word in non_option_args:
        if total_len_fault:
            sys.exit()
        norm_args_set.add(word)
    elif len(normalized) < min_word_len or total_len_fault:
        continue
    symmetry_skews[word] = get_skews(normalized)
    dictionary_reduced[word] = normalized
    dictlist_reduced.append(word)
    if normalized in normdict:
        normdict[normalized].append(word)
    else:
        normdict[normalized] = [word]

# If option -q = 1 or option -l > palindrome-length/2, print all single-word palindromes:
if max_word_qty == 1 or min_word_len * 2 > total_len:
    for word in symmetry_skews:
        if 0 in symmetry_skews[word] and \
                (len(non_option_args) == 0 or word in non_option_args):
            print_palindrome(word)
    sys.exit()

# Otherwise, combine the dictionary words to multi-word palindromes:
for (combination, midword, skew) in combine(dictlist_reduced, total_len, non_option_args):
    primary = ' '.join(combination)
    norm_primary = normalize(primary)
    norm_midword = dictionary_reduced[midword]

    s = skew
    w = len(norm_midword)
    p = len(norm_primary)

    if skew >= 0:
        norm_string = (norm_primary + norm_midword)[:p+abs(s)]
    elif skew < 0:
        norm_string = (norm_midword + norm_primary)[w-abs(s):]

    if len(norm_string) == 0:             # Iff primary is empty AND midword is palindrome!
        print_palindrome(midword)         # Hence result is the palindrome midword only
        count += 1
        if count > maxcount:
            sys.exit()
        continue

    # Generate results by mirroring the normalized string from primary to secundary side
    for p in partitions(norm_string[::-1]): # Reversed string partitioned
        make_palindromes(p, 0, [])          # Generate matching palindrome word-combination
