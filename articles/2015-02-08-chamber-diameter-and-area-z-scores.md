title: 'Chamber Diameter and Area Z-Scores'
author: Dan
date: 08 Feb 2015
description: New z-scores of the chamber diameters and areas (but not volumes!) of the RA, RV, LA, and LV 
category: release
---

Chamber diameter and area z-scores based on Cantinotti et al., JASE Dec. 2014

!!!

Today I added [z-scores of the chamber diameters and areas](/refs/cantinotti-jase-2014-december) for the right atrium, right ventricle, left atrium, and left ventricle according to the data from Cantinotti et al., as
published in the December 2014 JASE article, [Echocardiographic nomograms for chamber diameters and areas in Caucasian children.](http://www.ncbi.nlm.nih.gov/pubmed/25240494)
I think it is a bit peculiar that they publish reference values for the _elements_ that we commonly measure to calculate volumes (areas and lengths), but not z-scores for the *actual volumes*. 
Reliable and valid z-scores of LV volumes are still hard to find, and their absence is curiously unexplained in the manuscript.
Nevertheless, there is still a lot of useful data here. Particularly, the RV diameters are immediately useful and have been sorely needed since... forever.

Another element of the manuscript I find fascinating is the remarkable similarity of exponents between this manuscript and other published models (this aspect is, again, not elaborated upon). I think there is good evidence that:

* cardiac areas scale linearly with BSA (cm<sup>2</sup> : m<sup>2</sup>)
* cardiac diameters scale to the square root of BSA (cm : sqrt(m<sup>2</sup>), or cm : BSA<sup>0.5</sup>)

This pattern of relationships was eloquently described by Gutgesell and Rembold in their brilliant 1990 article, [Growth of the human heart relative to body surface area.](http://www.ncbi.nlm.nih.gov/pubmed/2309636)
Fifteen years later, Sluysmans and Colan reiterated the point in their similarly brilliant and thorough manuscript, [Theoretical and empirical derivation of cardiovascular allometric relationships in children.](http://www.ncbi.nlm.nih.gov/pubmed/15557009)

It is at this point that I need to give myself little refresher about logarithms. 

>Logarithms are the inverse of exponents. 

There.

A common strategy in cardiovascular normative data research is to log-transform both sides, i.e., the independent and dependent variables, and fit a line (y = mx + b) through the plot of transformed variables:

    ln(y) = m*ln(x) + b
  
Knowing about logs and exponents, we can also write that same relationship in the "exponential" form as:

    y = x^m * exp(b) also written as y = exp(b) * x^m

The point being that Cantinotti's log transformed _slopes_ are others' _exponents_. 

Both Gutgesell and Sluysmans have demonstrated that, for linear dimensions of cardiac structures, the expected "allometric" exponent that BSA should be raised to is *0.5*, i.e., the square root of bsa, written as: 

    BSA^0.5
    
For each of the linear measurements in the Cantinotti article, the "slope" (or allometric exponent) ranges from 0.453 to 0.506, with a mean of 0.475&mdash; all very close to the expected 0.5.
In fact, in the Sluysmans manuscript they found their valve and vascular diameter exponents to range from 0.42 to 0.58.

>Comparison of the exponents in the regressions across variables
... indicated that vascular and valvar dimensions
correlated on average with BSA<sub>H</sub> raised to the 0.50 power
(range 0.42 to 0.58).

They go on to explain several important points about this relationship:

>1) all
valve and vascular dimensions related more closely to BSA<sub>H</sub>
than to height, weight, or BSA calculated by other methods, 

>2) on average valve and vascular diameters relate most closely to
BSA<sub>H</sub>^0.5 

>3) each of the valvar and vascular diameters carry
either the total or a constant proportion of CO and should
therefore demonstrate a similar exponential dependence on
BSA<sub>H</sub>

Further, to test if the differences between actual and expected exponent (0.5 vs. 0.42 -0.58) were significant, they compared two more models:

    Y = a * (BSA)^0.5
  
and

    Y = a *(BSA)^0.5 + c
  
The second equation including an error term. They found

>no significant change in residual mean square compared
with the more general Y = a*X^b model, indicating that
the simpler linear model using (BSA)^0.5 as the independent
variable was equally successful in describing the relationship
between BSA and the size of vessels and valves.
  
If you look carefully at all of the Cantinotti data (both manuscripts!) and all of the equations of the form they call "exponential", for valve, vascular, and chamber _diameters_ you will find a slope/exponent that is _not significantly different from 0.5_. Similarly, the slopes/exponents for their _area data_ are all close to (read "not significantly different from") 1.0 (anything raised to the power 1 remains unchanged)

I find those facts somewhat profound, and quite comforting.
