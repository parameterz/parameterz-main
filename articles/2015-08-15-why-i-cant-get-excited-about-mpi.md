title: 'Thoughts on Fetal Modified MPI Reference Values'
author: Dan
date: 15 Aug 2015
description: Why I cant get excited about MPI z-scores
category: opinion
---

I almost got excited about z-scores for fetal _modified MPI_

!!!

While I was perusing PUBMED for new manuscripts concerning fetal echo reference values, a few[^mmpi] recent[^optimal] articles[^automation]
caught my attention, and I almost started to get excited about MPI again.

Then I read a little further.

Firstly, it appears that after decades of investigation, not everybody has the same idea about what _really_ happens to MPI during fetal development:

<a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4491561/"><img src="/static/img/aggregate_fetal_mpi.gif" alt="fetal MPI, or whatever"/></a>

(image courtesy of Biomed Res Int. 2015)

Secondly, when somebody thinks they get a pretty good idea about the relationship of MPI with gestational age, they
get something like this[^uog2007]:

<blockquote>
<p>
r<sup>2</sup> = 0.017
</p>
</blockquote>

As I understand it, the r<sup>2</sup> value tells us:

1. the "goodness of fit" of the regression line to the data, which is really:
2. the amount of variance explained by the linear model

This is a _miserable_ r<sup>2</sup>. <br/>
The data do not fit the regression well at all; basically none of the variance is explained by the model.
In cases like this, you are almost as well off to simply draw a perfectly horizontal line through
the mean value of all the data, and forget about gestational age altogether.

Lastly, when you look at the standard deviation generated by most of these "regressions", you find SD's that are
so large that basically all the normal patients are somewhere in the range of 0.25 to 0.45.
Since clinicians are generally not overly concerned with _supra-normal_ function, the take-home
message seems to be: MPI should be less than 0.45 - 0.50.

I just can't get excited about a broad range of normal, particularly when all that it really boils down to is a cutoff value.
While I think the "modified MPI" technique is attractive and solves many of the problems that the measurement of MPI
presents, I am not yet convinced it is something important enough to bother with calculating a z-score.

In any event, if you do occasionally get asked to calculate the MPI, I have a tool that makes it easy enough&mdash;
and even adds a little sugar (but no reference values!):

###[MPI Thing](//dev.parameterz.com/mpi)


[^mmpi]:[Gestational age-adjusted trends and reference intervals of the Modified
Myocardial Performance Index (Mod-MPI) and its components, with its
interpretation in the context of established cardiac physiological
principles.](http://www.ncbi.nlm.nih.gov/pubmed/24844183)
[^optimal]:[Influence of equipment and settings on myocardial performance index
repeatability and definition of settings to achieve optimal
reproducibility.](http://www.ncbi.nlm.nih.gov/pubmed/24639072)
[^automation]:[The Fetal Modified Myocardial Performance Index: Is Automation the Future?](http://www.ncbi.nlm.nih.gov/pubmed/26185751)
[^uog2007]:[Gestational-age-adjusted reference values for the modified
myocardial performance index for evaluation of fetal left cardiac
function](http://www.ncbi.nlm.nih.gov/pubmed/17290412)
