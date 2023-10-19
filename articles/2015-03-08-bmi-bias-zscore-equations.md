title: 'Dallaire Aortic Root Z-Score Equations'
author: Dan
date: 08 Mar 2015
description: New z-score equations for the aortic root adjusted for height and weight
category: release
---

New aortic valve, sinus of Valsalva, and ascending aorta z-score data

!!!

I added new equations for [z-scores of the aortic root](/refs/dallaire-pedcard-2015), based on the recent article,
[Bias related to body mass index in pediatric echocardiographic z scores](http://www.ncbi.nlm.nih.gov/pubmed/25388631).
In this article, the authors address the problem of using weight-containing variables (such as BSA) to adjust cardiac structures for body size, particularly in patients who are obese. 

Several different bivariate (one independent + one dependent variable) models using height, weight, BSA, and lean body mass (LBM) were tested for (residual) association with BMI. In their testing, all mathematical models, using all of the independent variables continued to have significant associations with BMI. It was only when a multivariable (using height and weight separately) polynomial model that they were able to achieve BMI independence.

>The association of higher BMI-for-age Z scores with lower proximal aorta Z scores when normalized for weight or BSA suggests one of two possibilities. Either the dimension of the proximal aorta is actually smaller in subjects with higher BMI-for-age, or the normalization for BSA or weight with bivariate models has introduced a bias.

So, I thought it might be interesting to make a few comparisons.

First, I made another [aortic valve z-score smackdown](/tools/aortic-valve-smackdown). For predicting the aortic valve "normal range" I used CDC and WHO growth chart data (50th %-ile) to generate a ht/wt/BSA range of "normal" (female) patients:

[![aortic valve vs. BSA](/static/img/aov-vs-bsa-demo.png "click to visit the smackdown")](/tools/aortic-valve-smackdown)


Secondly, although the range of normal is interesting, the specific problem the current model is designed to address concerns patients with "high BMI-for-age". So I generated a few hypothetical (female) patients and predicted the normal aortic valve for each of them:

<table>
<thead>
<tr>
<th>Age (yrs)</th>
<th>Height (cm)</th>
<th>Weight (kg)</th>
<th>BSA (H)</th>
<th>BMI</th>
<th>BMI Z</th>
</tr>
</thead>
<tbody>
<tr>
<td>8</td>
<td>120</td>
<td>39</td>
<td>1.16</td>
<td>27.08</td>
<td>2.46</td>
</tr>
<tr>
<td>10</td>
<td>130</td>
<td>51</td>
<td>1.38</td>
<td>30.2</td>
<td>2.4</td>
</tr>
<tr>
<td>12</td>
<td>141</td>
<td>66</td>
<td>1.64</td>
<td>33.2</td>
<td>2.38</td>
</tr>
<tr>
<td>14</td>
<td>152</td>
<td>78</td>
<td>1.85</td>
<td>33.8</td>
<td>2.2</td>
</tr>
<tr>
<td>18</td>
<td>163</td>
<td>120.5</td>
<td>2.41</td>
<td>45.2</td>
<td>2.43</td>
</tr>
</tbody>
</table>

[![AOV for Heavyweights](https://docs.google.com/spreadsheets/d/1_-Xa33ZTHg4JpEF6yKk7h6KR0YNsDtZRHSRtSP7iGog/pubchart?oid=1289956682&format=image)](https://docs.google.com/spreadsheets/d/1_-Xa33ZTHg4JpEF6yKk7h6KR0YNsDtZRHSRtSP7iGog/pubchart?oid=1289956682&format=interactive)

Finally, I created a single *extreme* hypothetical case (also female):

<div class="clear"></div>
<table>
<tbody>

<tr>
<td>Age (yrs):</td>
<td>12</td>
</tr>
<tr>
<td>Height (cm):</td>
<td>144</td>
</tr>
<tr>
<td>Weight (kg):</td>
<td>100</td>
</tr>
<tr>
<td>BMI:</td>
<td>48.2</td>
</tr>
<tr>
<td>BMI Z-Score:</td>
<td>2.92</td>
</tr>
<tr>
<td>Lean Body Mass (kg):</td>
<td>45.7</td>
</tr>
<tr>
<td>BSA (Boyd):</td>
<td>2.12</td>
</tr>
<tr>
<td>BSA (DuBois):</td>
<td>1.87</td>
</tr>
<tr>
<td>BSA (Haycock):</td>
<td>2.07</td>
</tr>
</tbody>
</table>
<div class="clear"></div>

and plotted a range of aortic dimensions and the generated z-scores for each dimension and reference:

[![Z-Score vs AOV](https://docs.google.com/spreadsheets/d/1_-Xa33ZTHg4JpEF6yKk7h6KR0YNsDtZRHSRtSP7iGog/pubchart?oid=773887378&format=image)](https://docs.google.com/spreadsheets/d/1_-Xa33ZTHg4JpEF6yKk7h6KR0YNsDtZRHSRtSP7iGog/pubchart?oid=773887378&format=interactive)

So, what can we learn from these plots and scenarios?
Well, one thing that is apparent to me is the data from Daubeney et al. are grossly removed from what all the others are predicting. The Pettersen et al. data becomes wildly unrealistic for larger patients. People should really think pretty hard before adopting these data.
Ignoring the above mentioned references, all the rest seem to predict things _pretty closely_. It is the plot of dimension versus z-score above that I think shows the most interesting data.

For the given "high BMI-for-age" patient, the Dallaire multivariable equation predicts the _smallest mean aortic valve diameter_. For that particular "extreme" patient, the predicted mean values are (excluding Daubeney and Pettersen):

<div class="clear"></div>
<table>
<thead>
<tr>
<th>Reference</th>
<th>Predicted Mean</th>
</tr>
</thead>
<tbody>
<tr>
<td>Dallaire:</td>
<td>20.25</td>
</tr>
<tr>
<td>Gautier:</td>
<td>20.59</td>
</tr>
<tr>
<td>Colan:</td>
<td>22.31</td>
</tr>
<tr>
<td>Warren:</td>
<td>21.16</td>
</tr>
<tr>
<td>Zilberman:</td>
<td>20.64</td>
</tr>
</tbody>
</table>
<div class="clear"></div>

By itself, a lower predicted mean will definitely address the issue of lower calculated z-scores for the higher BMI-for-age patients.

To wit, if we use the Dallaire predicted mean value of 20.25mm, each of the BSA-based references (again, excluding Daubeney and Pettersen) predict the following z-scores:

<div class="clear"></div>
<table>
<thead>
<tr>
<th>Reference</th>
<th>Z-score</th>
</tr>
</thead>
<tbody>
<tr>
<td>Dallaire:</td>
<td>(0.00)</td>
</tr>
<tr>
<td>Gautier:</td>
<td>-0.17</td>
</tr>
<tr>
<td>Colan:</td>
<td>-0.89</td>
</tr>
<tr>
<td>Warren:</td>
<td>-0.42</td>
</tr>
<tr>
<td>Zilberman:</td>
<td>-0.15</td>
</tr>
</tbody>
</table>
<div class="clear"></div>

Granted, the authors admit that a bias still exists in patients with BMI z-scores &gt;2, but that this effect is at least attenuated as compared to the bivariate models.

* * * 

N.B.: I included the lean body mass z-score equations (three term polynomial) in the plots even though the manuscript reveals that they did not perform as well as the multivariable polynomial model. I was hoping that something dramatic and unexpected would reveal itself, but alas nothing terribly obvious comes to light. I don't think we should give up on using LBM as a scaling variable, but based on the Dallaire et al. data in this article, the theoretically superior LBM  model might be outperformed by a more practical and simpler(?) multivariable model.


###Resources

- [WHO and CDC growth charts](http://www.cdc.gov/growthcharts/)
- [online BMI and BMI Z-Score calculator](http://www.quesgen.com/BMIPedsCalc.php)
- [Alternative plotting perspective on z-scores](http://www.ncbi.nlm.nih.gov/pubmed/23973183)
- [Pediatric Lean Body Mass Calculator](http://dev.parameterz.com/lbm/)