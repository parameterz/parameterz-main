title: 'Aortic Valve Z-Score Smackdown'
author: Dan
date: 12 Feb 2018
description: pitting the most recent z-score models against each other
category: opinion
---

Presenting a Valentine's Edition 
re-make of the Aortic Valve Z-Score Smackdown.

!!!

The new [PHN data](/refs/lopez-circimaging-2017) and most recent data from [Cantinotti et al.](/refs/cantinotti-jcard-2017)
provide us with the industry's most recent and, arguably, definitive z-score reference. Both references were published in 2017.
The PHN data is developed using data on 3215 subjects from 19 North American centers. The Cantinotti data is based on 1151 subjects 
from a single center in Italy. Since the PHN data purport to show *no clinically significant difference* 
when considering race, a comparison of the two datasets *should* hold&mdash; despite their geographic differences.

Firstly, lets examine the predicted means.

###Means
![PHN Means](\static\img\PHN-AOV-Means.png)

The PHN data use their allometric scaling model, previously validated, and 
involves *"... nonlogarithmic BSA
transformations and no measurement transformations, unlike
other studies..."* Their aortic valve equation looks like this:

![PHN Eqn1](\static\img\PHNEqn1.png)

*Note: I multiplied the published value by ten to get the result in mm.*

They go out of their way to state that this form does not involve "BSA transformation", unlike the data from Cantinotti, whose equation 
looks like this:

![PHN Eqn2](\static\img\CantEqn2.png)

Yet, logarithms and exponents are **related**: a logarithm is nothing more than an exponent. 
So, we can also change the form of the Cantinotti expression by *exponentiating* it, and we get this:
 
![PHN Eqn3](\static\img\CantEqn3.png) 

Presented in this way, both equations are identical *in form*- differing by a trifle here and there between the allometric exponent and multiplier.
I happen to think the PHN model makes good sense: using the exponent "0.5"- i.e., raising it to the 1/2 power- 
is also to say taking the square root of BSA, which puts it in the same geometric units
as the linear measurement. That is not capricious or random- that's logical.

Inspecting the &beta; terms for the Cantinotti data reveals a remarkable consistency. Except for the IVC, they all hover around 
"0.5" and range from 
0.466 to 0.569, with a mean, mode, and median of 0.510, 0.515, and 0.514. 

So, with identical form, similar exponents and multipliers, are they importantly different? 
Looking at the plot of the means it is clear that for the smaller patients the means are not much different but as the 
BSA increases the difference becomes larger.

![PHN Eqn4](\static\img\PHNMeanDiff.png) 

At around 0.5 M^2 the difference between the two equations is a trivial 0.5mm; at around 1.25<sup>2</sup> the difference approaches 1mm and it goes up from there. 
At around 0.65m<sup>2</sup> that difference hits the 5% mark, i.e., becomes clinically significant, and by the time you reach 2.0m<sup>2</sup>, there is nearly a 7% difference between the 2 equations

###Ranges

![PHN Ranges](\static\img\PHNvCantinottiRanges.png)

I was going to go on a bit of a rant about the manner in which the ranges
are calculated, but looking at the charts for the normal range, it is hard to argue that there 
is much in the way of a difference. The Cantinotti ranges are uniformly higher than the PHN ranges and most- if not all- of that difference can be 
attributed to the higher predicted mean values for the Cantinotti data.

Where things get a bit hairy- and this goes for all equations like the 
Cantinotti data that assume a log-normal distribution-
 is on the edges. That is to say, the biggest differences are in the &plusmn; 5 sd's and beyond.
 At z= +5, you need a full 1 mm larger measurement using the Cantinotti equations; at z = +10, the aortic valve measurement
 has to be nearly 4mm larger than when using the PHN equations. The reverse situation applies on the negative Z-score side...   
 
![PHN ZScore diffs](\static\img\PHNZScoreDiffs.png)

Both manuscripts claim, with equal veracity, that their data produce normally distributed z-scores. Neither manuscript provide us with a normality plot
or histogram though. The PHN manuscript does not explixitly state in which way they tested for normality, while Cantinotti et al. make some effort,
using the "Shapiro-Wilk and Lilliefors (Kolmogorov-Smirnov)" tests. 

Both models can't be true though. Echo measurement data can't be both normally distributed on the natural scale AND normally distributed when log-transformed.
As far as I a concerned, the jury is still out.


See also: [AOV smackdown page](/tools/aortic-valve-smackdown), updated to reflect the additional references.



  


 