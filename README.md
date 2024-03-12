# Name: palindromes.py
palindromes.py - Program that generates (a stream of) single-word and multi-word palindromes
in a given language.

# Description:
palindromes.py is a Python3 program that generates single-word and multi-word palindromes
in a given language,
including the optional words given - whether or not existing - given as argument(s).

Various properties can be set to manipulate and filter the results, such as:
- the language in which the palindromes are to be generated (default is Dutch);
- approximate palindrome length;
- the minimum word length in the generated palindromes;
- the maximum number of words per palindrome;
- any characters to be excluded from the palindromes;
- any existing or non-existing word(s) that must be part of the palindromes;

The results are sent to standard output and can be piped to e.g. 'less' or other utilities and applications.

Perequisite is presence on the system of a word list in flat text format
of at least one language.
In its present form, the program code references following language word lists: 

	/usr/share/dict/dutch
	/usr/share/dict/american-english
	/usr/share/dict/british-english
	/usr/share/hunspell/de_DE_frami.dic
	/usr/share/dict/french
	/usr/share/dict/spanish
	/usr/share/dict/italian

If no language option is given, Dutch is the default language.

If wished and as per system configuration,
above paths and language default may be changed or removed
and references to other word lists may be added,
by modifying the program code accordingly.

# How to use palindromes.py

## Usage:

	palindromes.py [-abdfghisSRlLqx] WORD(1) [ ... WORD(n)]

## Options:
	-a            American-English
	-b            British-English
	-d            Dutch
	-f            French
	-g            German
	-h            Help (this output)
	-i            Italian
	-s            Spanish
	-S            Sorted generation of palindromes incl. WORD args (overridden by -R)
	-R            Random generation of palindromes incl. WORD args (overrides -S)
	-l MINWORDLEN Filter results to palindromes w/ words of at least MINLENGTH
	-L LENGTH     Filter results to palindromes of approx. LENGTH (only with -S or -R)
	-q MAXQTY     Filter results to palindromes with <= MAXQTY words
	-x CHARS      Exclude words with any of these CHARS

Options can be combined but only one (1) language can be set at the time.

LENGTH is set to 30 characters by default.

If either the option -S (lexicographically sorted) or -R (random word order) is used,
the program generates a stream of palindromes,
limited only by any further option settings.
If in addition one or more [WORD] arguments is provided,
the output is limited to only the palindromes that contain the given words,
if any match exists.

If neither of the options -S nor -R is used,
minimally one [WORD] argument *must* be provided,
to which the results will be filtered.

The [WORD] arguments are allowed to be non-existent words,
and are not limited by option -l (word length).

# Author:
Written by Rob Toscani (rob_toscani@yahoo.com).
