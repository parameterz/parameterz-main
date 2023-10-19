title: 'RV TDI Z-Scores'
author: Dan
date: 12 Mar 2014
description: RV tissue Doppler z-score calculator
category: release
---

Starting to go beyond just anatomy... 

!!!
A quick post announcing the [RV TDI S' z-score calculator](/refs/koestenberger-ajc-2012).  

Today I added a reference and calculation for RV tissue Doppler z-scores (for children). This calculator uses the
2012 data from Koestenberger et al., and is only for the s' wave&mdash; which they
adoringly termed _TAPSV_, or "tricuspid annular peak systolic velocity".

This is a very simple lookup, using the data table provided in the manuscript. I used their
&plusmn;2 SD data to calculate the appropriate SD and thus the z-score. Minor differences in the
results generated here versus the text can be attributed to the fact that I use &plusmn;1.96 for the ranges...

Later in 2013 the same group published data for pre-term infants, thus broadening the utility of this calculation.
Before I incorporate their new data I will have to think about how to deal with the "age" of the patient as my
current implementation starts at "zero"&mdash;as in "day of life 1"&mdash;without regard to the term.
