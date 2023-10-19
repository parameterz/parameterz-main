title: 'Thoughts About Pulmonary Artery Acceleration Time Z-Scores'
author: Dan
date: 19 Jan 2017
description: a few thoughts about the age-adjusted PAAT z-scores 
category: opinion
---

A few thoughts for your consideration concerning age-adjusted z-scores of pulmonary artery acceleration time.

!!!

I recently added a [z-score calculator for age-adjusted pulmonary artery acceleration time](/refs/koestenberger-circimaging-2017) (PAAT), based on the manuscript "[Normal Reference Values and z Scores of the Pulmonary Artery Acceleration Time in Children and Its Importance for the Assessment of Pulmonary Hypertension](https://www.ncbi.nlm.nih.gov/pubmed/28003222)" (Circ Cardiovasc Imaging., 2017;10).

The manuscript provides PAAT z-scores for various children using age and body size as the predictors.
As long as the patient has an age-appropriate HR, age is probably a reasonably fair predictor. But I wonder if the primary factor that influences PAAT isn't just *heart rate*.

Using data from the manuscript "Table 3. Age-Specific PAAT Values", I plotted the average heart rate for the age groups vs the PAAT:

<img src="https://docs.google.com/spreadsheets/d/1P9P14D0FloHd-CjfUnPjmjRVpfxmbWp6lFuo5QEERAQ/pubchart?oid=2093392434&amp;format=image" alt="PAAT vs HR" >

The second order polynomial equation suggested by Google Sheets fit the data quite nicely.

While I think it may seem obvious that the primary influence is HR&mdash; beyond that the actual relationship might be even more usefully described when HR is expressed as the *heart period*. Firstly, the pulmonary artery ejection time is measured in milliseconds, so it should be intuitively helpful to have our predictor use *the same units*. Secondly, The ejection time is, functionally, a portion of systole; systole comprises a fairly predictable portion of the entire heart cycle/period. Predicting the PAAT from the heart period seems mechanistically sound.

<img src="https://docs.google.com/spreadsheets/d/1P9P14D0FloHd-CjfUnPjmjRVpfxmbWp6lFuo5QEERAQ/pubchart?oid=355047830&amp;format=image" alt="PAAT vs RR">

The fit through this data is also well described with a second-order polynomial equation.

Apart from the maturational decrease in heart rate with age, until the PAAT is *adjusted* for heart rate, I am not sure what conclusions can be drawn about the effect of age on pulmonary artery acceleration time.

