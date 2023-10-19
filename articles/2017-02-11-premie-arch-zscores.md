title: 'Discussion of Premie Arch Z-Score Data and Interpretation'
author: Dan
date: 11 Feb 2017
description: a few caveats and notes on my interpretation of the premie arch data from the recent JASE article
category: opinion
---

I could not make the calculations work the way the authors of a recent manuscript intended,
so I improvised. 

!!!

The recent/in-press manuscript [Normative Values of Aortic Arch Structures in Premature Infants](https://www.ncbi.nlm.nih.gov/pubmed/28139441) provides us with new data for z-score calculations 
of arch measurements. I used their data and equations to generate a z-score calculator as the authors describe in the manuscript 
and I had trouble reconciling the results of those calculations with the manuscript tables and charts.

For example, let's use only the data for the ascending aorta, and we'll assume the patient weighs 1100 grams.

The authors describe a third-order polynomial equation based on body weight for predicting the mean values and the data for these are given in their "Table 2":

* intercept: 2.332
* b1: 0.004
* b2: -1.258e-6
* b3: 2.111e-10
* se: 0.041

Per their equation, the mean is predicted as:

>intercept + (b1 * wt) + (b2 * wt^2) + (b3 * wt^3)

Substituting our hypothetical 1100 gram patient, we get:

>2.332 + (0.004 * 1100) + (-1.258e-6 * 1100^2) + (2.111e-10 * 1100^3)
>= **5.49**

That is close to their Table 2 value of 5.2 &plusmn; 0.8, and I should be fine with that. 

I am fine with that.

Probably fine with it.

Where things really fall apart for me on these equations is the z-score calculation. The authors instruct us to use the published standard error (SE). That is:

> z = (score - mean) / SE

The published SE for the ascending aorta is 0.041, yet the published SD from table 2 is 0.8 (for an 1100 gram patient). That means, for a measured ascending aorta of 4.4mm ( one SD below the mean, using Table 2):

> z = (4.4 - 5.49) / 0.041
> = **-26.6**

Yeeowch.

Clearly, the standard error cannot be substituted for standard deviation in this case, or the published se (or sd's) are in error.

I tried reaching out to the authors via email but alas&mdash; no answer.

So, I had to abandon the prediction equations. 
Thus, the z-score calculations that I generate [here](/refs/dijkema-jase-2017) 
use only the Table 2 data. The resulting predictions are therefore not continuously variable based on weight, 
but are categorized into discrete weight groups as they do in the manuscript.

Also note: I omitted these calculations from the arch calculator [here](/sites/aortic-arch) since the data are unique to premature babies and cannot be extrapolated above 2 kg.

