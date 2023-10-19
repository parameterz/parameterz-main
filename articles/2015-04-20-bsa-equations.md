title: 'BSA Equations'
author: Dan
date: 20 Apr 2015
description: a JavaScript helper utility for calculating BSA from various equations
category: code
---

A Parameterz.googlecode code relic I am going to hold on to: BSA equations

!!!

This is a JavaScript function I often refer to for calculating BSA via various equations (rescued from the soon-to-be-shut-down parameterz googlecode repo).

<pre><code>
function calcBSA(wt, ht, BSAMethod) {
    /// &lt;summary&gt;returns the body surface area in meters^2; calling with a single arg is assumed to be 'wt'&lt;/summary&gt;    
    /// &lt;param name=&quot;ht&quot;&gt;height, units = cm&lt;/param&gt;<br/>    /// &lt;param name=&quot;wt&quot;&gt;weight, units = kg&lt;/param&gt;   
    /// &lt;param name=&quot;BSAMethod&quot;&gt;optional; type = string (any of the following:&quot;DuBois&quot;, &quot;Haycock&quot;(default), &quot;Gehan&quot;, &quot;Mosteller&quot;, &quot;Boyd&quot;, or &quot;Dreyer&quot;)&lt;/param&gt; 
    /// &lt;returns&gt;Number&lt;/returns&gt;   
    // allow for ht and method to be optional:
    if (!ht && !BSAMethod) {
        // only one arg was passed, 'wt'
        var BSAMethod = "Dreyer";
    }
    else if (!BSAMethod) {
        var BSAMethod = "Haycock";
    }
    switch (BSAMethod) {
        case "DuBois":
            return 0.007184 * Math.pow(ht, 0.725) * Math.pow(wt, 0.425);
        case "Haycock":
            return 0.024265 * Math.pow(ht, 0.3964) * Math.pow(wt, 0.5378);
        case "Gehan":
            return 0.0235 * Math.pow(ht, 0.42246) * Math.pow(wt, 0.51456);
        case "Mosteller":
            return Math.sqrt((ht * wt) / 3600);
        case "Boyd":
            wt = wt * 1000;
            var exponent = 0.7285 - 0.0188 * (Math.LOG10E * Math.log(wt)); //necessary to get the Log base 10 of (wt)
            return 0.0003207 * Math.pow(ht, 0.3) * Math.pow(wt, exponent);
        case "Dreyer":
            return 0.1 * Math.pow(wt, (2 / 3));
        default:
            return 0.024265 * Math.pow(ht, 0.3964) * Math.pow(wt, 0.5378);// returns Haycock in the event an unfamiliar method is passed in
    } //end switch
}
</code></pre>

