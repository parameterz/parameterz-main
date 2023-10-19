title: 'Neonatal RV data'
author: Dan
date: 17 Jan 2015
description: New z-scores and reference values for echo measurements of the newborn RV
category: release
---

Newborn RV size and function data based on Jain et al., JASE 2014.

!!!

Today I added [z-score calculations for the neonatal RV](/refs/jain-jase-2014), based on data presented in the December 2014 JASE article,
[A comprehensive echocardiographic protocol for assessing neonatal right ventricular dimensions and function in the transitional period: normative data and z scores](http://www.ncbi.nlm.nih.gov/pubmed/25260435).

There are a few exceptions to the data available here as compared to that presented in the article.
Namely, I have omitted the z-score calculations of the following measurements:

- IVCV'
- IVRT'
- MPI
- S'/D' ratio


Things like the tissue Doppler-derived IVCV' (isovolumic contraction velocity) and IVRT (isovolumic relaxation time) are notoriously difficult to measure[^notorious] (particularly so in my hands).
The tissue Doppler-derived MPI and S'/D' ratio suffer from the same fate as the preceding, I am afraid. To wit: the wide range of normal values of the MPI (&plusmn; 2 SD = 0.1 - 0.7).

I struggled with the idea of including calculated Doppler ratios. The ratios of the inflow and tissue Doppler vary wildly: according to the data, it is normal for the ratio to exhibit a reversed E/A&mdash; like that of a "normal" newborn, or a  "big E, little A" like that of an adult (inflow Doppler E/A ratio &plusmn; 2 SD = 0.6 - 1.2). If the morphology of the E and A waves can normally vary that much, I am not sure if a ratio z-score has much benefit. I am deeply skeptical about diastolic function z-scores you see, but I included them anyhow for the less skeptical among us.

If you feel strongly that these omissions are glaring and must be remedied, you can petition for their inclusion by [adding a feature request](https://bitbucket.org/parameterz/main/issues).

[^notorious]: ["Citation needed"](http://xkcd.com/285/)