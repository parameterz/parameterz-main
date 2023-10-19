title: 'Z-Scores For Adult Echo Measurements'
author: Dan
date: 10 May 2019
description: Data from normal adult Chinese Gan patients using a novel multivariable allometric model
category: opinion
---

Wherein we are introduced to the OMAM (Optimized Multivariable 
Allometric Model). This one is for our long-suffering ACHD brethern.

!!!

It is somewhat rare that we encounter a manuscript that deals 
with adult echo reference values that can be adapted to, or understood in the 
terms of, z-scores. For whatever reason, z-scores do not cross pollinate 
to our adult echo brethren. 
But I think that is exactly what has happened with the recent manuscript
(still in-press at the moment), ["A Novel Mathematical Model for Correcting 
the Physiologic Variance of Two-Dimensional Echocardiographic Measurements 
in Healthy Chinese Adults"](/refs/yao-jase-2019). 
While I am not certain it was the authors'
intent that these be used *specifically* for z-scores, it looks like it 
is working out beautifully. 
Apart from this unique qualification, there are a few other elements of this manuscript
that I find noteworthy. Their consideration of the importance
of assessing residual associations of normalized values is essential. 
Armed with that understanding, 
they then litigate a fairly damning case against the continued use of 
ratiometric scaling. 

#### Residual Associations

If we consider the *actual* goal of scaling practice,

> The goal of scaling cardiovascular dimensions is to remove the
physiologic influence of age, gender, and body size in individuals... 

it is surprising how often the effect of scaling, the *removal* of the influence of body size, 
goes unexamined. Countless manuscripts describing 
"reference values" never bother to look for residual relationships of the scaled value 
with body size. Yet, this is probably the most important step in constructing such
reference values:  
 *does it do what it is supposed to do?*  

When, in the rare instance this bit of due diligence *has* been done, the results
are troubling. For instance, [Neilan et al.](https://www.ncbi.nlm.nih.gov/pubmed/18329846), 
looked at the LA diameter and various ways to index for body size. They note:

>Because the goal of normalization is to remove the effects of body size, 
following normalization there should ideally be little or no residual correlation of the
indexed variable with the indexing variable

![LA Residual Associations](/static/img/NeilanResidAssoc.jpg "overcorrection")

But, as they show, the desired effect is often not achieved. Before correction, there is a decent
correlation between left atrial size and BSA (0.44). However, the ***indexed*** left atrial size
has an even better correlation with BSA (-0.52)- only now the value is *negative*.

Plotting the indexed values against body size makes any residual relationship obvious visually, as the authors 
of the present study have done:

![LA Diam Index](/static/img/YaoLASize.jpg "more overcorrection") 

The plot on the left shows the expected relationship of cardiac structures with body size:
as body size increases, so too does the measurement of the structure, in this case,
the left atrial AP diameter. The plot on the right shows us the indexed value, 
LA diameter/BSA, plotted against BSA. The red line approximates the 
[ASE Guidelines](https://www.ncbi.nlm.nih.gov/pubmed/25559473) for the 
left atrial index upper limit of normal.

![ASE Guidelines for LA Size](/static/img/ASEGuidelines_LASize.jpg "LA size")

Note that the correlation of the indexed value with BSA is stronger than the original
association, and now the correlation is negative. The relationship has reversed. 
It is over-corrected. If
 the correction is to be believed, we should be starting to get concerned 
 about the trend for larger patients to have an almost pathologically small left atrium. 

 What we *want* to see from a properly scaled value is NO residual association with body size. 
 Something like:
 
 [![Rexthor, the Dog Bearer](/static/img/linear_regression.png)](https://xkcd.com/1725/)
 
 And that is, indeed, what results from using the multivariable model developed by the authors:
 
![OMAM LA Diam](/static/img/YaoLASize_OMAM.jpg "corrected LA Size") 
 
#### Litigating The Ratiometric Approach

 Knowing that a properly constructed scaled value should have no residual
 relationship with body size, the authors defined what that meant in an 
  objective, statistical sense: 
 
> absence of statistically and biologically significant correlation (r > 0.20, P < .05)
between the corrected values and age or any body size variables
 
 They then proceed to construct and test literally all possible "single variable
 isometric model" (SVIM) corrections. Each echocardiographic measurement 
 was indexed to each of height, weight,
 BMI, and BSA. There were 34 cardiac measurements made, resulting in 
 34 x 4 = 136 individual models. 
 Then, residual relationships were examined between each of *those* indexes
 and each of age, height, weight, BMI, and BSA. 136 models, 5 comparisons... 
 That is a systematic evaluation if ever there was one.
 
 Out of all of those models and comparisons they found that this type of simple index,
 commonplace among echo labs and throughout the literature, and *recommended in The Guidelines*, 
 is rarely effective as a correction. According to the authors, only 15 of 136 models 
 (11%) met their criteria for appropriate correction. Reviewing the data, it is not easy
 to discover which of the models actually meet criteria, but it looks like these might be the ones:
  
  * LA Area/BMI
  * LAV/BMI
  * LVOT/height 
  * LVEDD/height
  * LVESD/height
  * LVEDV/BSA
  * LVESV/weight
  * LVESV/BSA
  * RV-fwt/height
  * RVOT/height
  * RV-ap/height
  * RV-l/height
  * RV-m/height
  * RV-m/BSA
  * PV-a/height
 
  The two indexes that use BMI should just be ignored. Nobody in their right mind
  should be using BMI alone as a scaling parameter- it tells us nothing about the 
  actual size of a patient, only their proportions. Of the remaining indexes,
   most of them are linear measurements indexed to height- a dimensionally
   consistent adjustment and thus, not much of a surprise. Those *should* be rational adjustments.
 Only three of the appropriately scaled indexes use BSA&mdash; the recommended body-size adjusting variable.
 They also note that in the majority of cases (nearly 70%), the simple index
 over-corrects (as described above). They conclude this evaluation by stating:
   
 > the basic assumption of a
linear correlation between cardiovascular dimensions and body size
variables is incorrect, and thus the use of an SVIM for scaling cardiovascular
dimensions is problematic and should not be recommended
any longer in both scientific research and clinical practice for adult
populations.
  
  Combine that statement with the recommendations from [Dewey et al.,](https://www.ncbi.nlm.nih.gov/pubmed/18443249) in 2008:
  
  > theoretical arguments and empirical
evidence indicate that indiscriminate use of ratiometric
scaling approaches is at best problematic and at worst
dangerous.

and  

> Reliance on parameters ratiometrically scaled to
BSA for clinical decision making should be discouraged.
  
  
 I am appreciative of the thoughtful and thorough examination of the current scaling practice for adult
 echo measurements. I also believe their proposed model is a giant leap
 forward in our understanding of normal (and abnormal!) cardiac size. 
 
 I also appreciate that the 
 authors are looking forward to the data from the ongoing (recently concluded?) 
 [World Alliance of Societies of Echocardiography (WASE) Normal Values Study](https://www.asefoundation.org/wase/).  
 I am deeply troubled though, by the design of that study:
  
 > Indexing measurements by body surface area will be performed as recommended by the guidelines. 
 
  If the WASE study 
   is published *without* an examination of residual relationships, 
   it will simply prolong our collective international agony.  
   ... and then this study
    will stand for a long time as the definitive source for adult echo normative data.
    
   
 
  
 
 