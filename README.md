# Name: palindromes.py
palindromes.py - Program that generates multi-word palindromes.

# Description:
palindromes.py is a Python3 program that generates multi-word palindromes, including the optional words given - whether or not existing - given as argument(s).

palindromes.py can be used in two modes:
- Automatic generating mode (if option -S or -R is given) with optional word argument(s),
rendering solutions in either:
    - Sorted lexicographical word order, or
    - Random order
- Query mode (without any of the options mentioned above) with compulsary word argument(s)

palindromes.py offers the possibility to set various properties to manipulate and filter the results,
such as:
- the language in which the palindromes are to be generated (default is Dutch);
- the minimum length of words in the generated palindromes;
- the maximum number of words per palindrome(s);
- any characters to be excluded from the palindrome(s);
- any existing or non-existing word(s) that must be part of the palindrome(s);

The results are sent to standard output and can be piped to e.g. 'less' or other utilities and applications.

Perequisite is presence on the system of a word list in flat text format of at least one language.
In its present form, the program code references following language word lists: 

	/usr/share/dict/dutch
	/usr/share/dict/american-english
	/usr/share/dict/british-english
	/usr/share/hunspell/de_DE_frami.dic
	/usr/share/dict/french
	/usr/share/dict/spanish
	/usr/share/dict/italian

If no language option is given, Dutch is the default language.

If wished and as per system configuration, above paths and language default may be changed or removed and references to other word lists may be added, by modifying the program code accordingly.

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

If the option -S or -R is used with no [WORD] argument(s),
the program generates a stream of palindromes, given the option settings.
If one of more [WORD] arguments are given, the stream of palindromes will be limited to those
including these words if existent.

If neither option -S nor -R are used, one of more [WORD] arguments *must* be given, to which
the program will present palindromes if existent with these words at the left side *exclusively*.

# Author:
Written by Rob Toscani (rob_toscani@yahoo.com).