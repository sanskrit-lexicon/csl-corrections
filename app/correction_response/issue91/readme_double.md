## Indentation in list display.
[corrections_scott_double.txt](https://github.com/sanskrit-lexicon/csl-corrections/blob/master/app/correction_response/issue91/corrections_scott_double.txt) collects 580 cases where Scott suggests using a Single indentation in the list display left pane instead of a double indentation.

These indentations in list display are supposed to represent what Monier-Williams describes as the '4 lines of words' in his dictionary:
[MW 4 lines](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/mwpref/mwpref11.html) .

In cdsl mw.xml and displays , these are represented as H1, H2, H3, H4;  
cdsl has also added some alphabetical suffixes (e.g. H1A, H1B, etc.)  In the discussion of this comment, let's ignore these suffixes.

In the left pane of the list display,  no indentation represents H1, Single indentation H2, Double Indentation H3, and triple indentation H4.

In mw.txt these lines are represented by <e>1, ..., <e>4  in the metaline of an entry.

---------------------------------------------------------------

Back to the suggested changes.  How to decide?  Take as example Cases 12-15 of words under anavadya.

<img width="599" alt="image" src="https://github.com/user-attachments/assets/dcee91a5-9a3c-41f2-86ee-9642a96f8eaf">

Here the relevant comment from MW preface is 
> The third or branch line in thick Indo-Romanic type is used for grouping together under a leading word all the words compounded with that leading word.

The 'leading word' in our example is अनवद्य which is an H1.
The 4 'thick Indo-Romanic type' words are '-tA, -tva, -rUpa, anavadyANga'.
And these 4 are marked by cdsl as 'H3'.

*This markup seems consistent with MW*.
I propose that none of the 580 correction suggestions should be made.
