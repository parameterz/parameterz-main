title: 'BSA to ht and wt tool + TDI z-scores'
author: Dan
date: 20 Mar 2014
description: introducing a way to reverse engineer ht and wt from BSA; more TDI z-scores
category: release
---

Feature requests: "use BSA" and "more TDI data".

!!!
###BSA
Some time ago, a feature request was made that would allow a user to enter a
known BSA instead of the patient's *actual height and weight*. And, while I thought
that sounded a little far-fetched at first, I also thought there was some utility
in having a way to look up a reasonable length/height for patients in whom measuring this
feature is inconvenient or impossible.

So, I came up with this: [reverse engineering body surface area.](/tools/bsa-ht-wt)

The tool uses published age and gender-specific normative data for height and weight
and calculates a BSA. Then it seeks a match from that data or if a match is not found,
reverts to a prediction algorithm (based on splines).
A little wonky, I know... but it does what I set out to do.

###TDI
I also added the age-specific TDI data presented by
[Eidem et al., JASE 2004](/refs/eidem-jase-2004), now experiencing it's 10-year anniversary.
The RV systolic TDI values can be contrasted
against the recently added [Koestenberger data](/refs/koestenberger-ajc-2012).
Adding this data was also a feature request and it sort of went against my better judgement
to include it. For one thing, I have some reservations about z-scores for
measurements of diastolic physiology. Physiology is weird;
physiology *changes*.

For another thing, some of the relationships are tenuous. The "R-squared" value for some of the
diastolic parameters is so low that to suggest a relationship exists at all seems, ahhmm, *optimistic*.
Moreover, while the data is analyzed using linear regression, the scatterplots seem to suggest otherwise
(at least to me it looks like a non-linear relationship with age&mdash;particularly in the very young).

Lastly, I used their published mean and SD values to generate the z-scores. Some of the SD's are so large that
the lower limit of normal for some of the measurements is a **negative value**. Comparing
the reference values I generate using this technique and the various figures throughout the article, I can't
reconcile the ranges.

I am not the only one that has reservations about what to do with
reference values for pediatric diastolic function indices.
The recent critical review by [Cantinotti et al.](http://www.ncbi.nlm.nih.gov/pubmed/23261147), sums up the current state of the art:

>A valid meta-analysis cannot be performed from published studies,
>because of variability in the population being studied,
>in the methodology for performing and normalizing measurements,
>and in the ways to express normalized data.

Until something new and dramatically better comes along in this scope, this reference will likely be the
first and last of the parameterz.com diastolic function z-scores.



