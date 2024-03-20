# Name: palindromes.py
palindromes.py - Program that generates single-word and multi-word palindromes
in a given language.

# Description:
palindromes.py is a Python3 program that generates a random stream of single-word 
and multi-word palindromes in a given language,
including the optional words - whether or not existing - given as argument(s).

Various properties can be set to manipulate and filter the results, such as:
- the language in which the palindromes are to be generated (default is Dutch);
- approximate palindrome length;
- the minimum word length in the generated palindromes;
- the maximum number of words per palindrome;
- any characters to be excluded from the palindromes;
- the number of palindrome results.

Additionally, sorted (= reproducible) output can be chosen as replacement for the default random 
order output.

The results are sent to standard output and can be piped to e.g. 'less' or other utilities and applications.

Prerequisite is presence on the system of a word list in flat text format
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

	palindromes.py [-abdfghiscFlLqxS] [WORD(1) [ ... WORD(n)]]

## Options:
	-a            American-English
	-b            British-English
	-d            Dutch
	-f            French
	-g            German
	-h            Help (this output)
	-i            Italian
	-s            Spanish
	-c COUNT      Limit output to COUNT results
	-F            Write output to logfile
	-l MINWORDLEN Filter results to palindromes w/ words of at least MINWORDLEN
	-L LENGTH     Filter results to palindromes of approx. LENGTH (default 30)
	-q MAXQTY     Filter results to palindromes with <= MAXQTY words
	-x EXCLCHARS  Exclude words with any of these EXCLCHARS
	-S            Sorted instead of random generation of palindromes

Options can be combined but only one (1) language can be set at the time.
The WORD arguments are optional, and are used to filter the results.

As an example, the following command:

	./palindromes.py -a -c20 -l4 -L25

may render the following (random) output:

	deleverages Sega reveled
	derogating Nita gored
	remarking Agni Kramer
	débutantes Etna tubed
	débutante Etna tubed
	ululating Nita Lulu
	spoonerism siren oops
	allegro boga Iago Borg Ella
	allegro boga sago Borg Ella
	noontime's emit noon
	gardener's Rene drag
	gulp's orb's Bros plug
	redraw drab bard warder
	stalwarts straw lats
	procedure rude Corp
	procedure rude corp
	snits GNU's Sung's tin's
	snits GNU's Sung's tins
	spillways yawl lip's
	spillways yawl lips


# Author:
Written by Rob Toscani (rob_toscani@yahoo.com).
