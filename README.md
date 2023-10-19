#Overview

The goals for this re-make are several:

* permanence (favors javascript and GitHub hosting)
* modular design that allows easy introduction of new references/calculations
* reponsive design
* allow per-reference and per-site calculations
* incorporate feature requests:
    * convey patient info from page to page (html5 web storage)
    * allow user to optionally enter ht & wt OR bsa
* allow english/metric demographics
* +/- database user data (python/GAE)

##Moving Ahead With App Engine

While the free hosting on GitHub and the js solution is slick, it doesn't help
achieve the final, large goal: crowd-sourced reference values. The most reasonable way forward on this
path is most likely with a self-managed datastore, like with App Engine.
The Python module pattern is actually quite convenient, too.