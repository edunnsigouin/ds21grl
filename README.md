Limited influence of localized tropical sea-surface temperatures on moisture transport into the Arctic
============

Authors
--------
[Etienne Dunn-Sigouin](https://sites.google.com/view/etiennedunnsigouin/home)<sup>1</sup>, [Camille Li](https://folk.uib.no/cli061/)<sup>1</sup>
,and [Paul J. Kushner](http://www.pjk.atmosp.physics.utoronto.ca/)<sup>2</sup>.

1: [Geophysical Institute, University of Bergen](https://www.uib.no/en/gfi),
[Bjerknes Centre for Climate Research](https://bjerknes.uib.no/en/frontpage), Bergen, Norway.

2: [Department of Physics, University of Toronto](https://www.physics.utoronto.ca/), Toronto, ON, Canada.

Key Points
----------

  - Arctic moisture transport is dominated by transient planetary waves in aquaplanet model driven by zonally uniform boundary conditions
  - Tropical sea-surface temperature anomalies affect Arctic moisture transport mostly via changes in water vapor
  - Localized tropical perturbations alter Arctic moisture transport more than uniform perturbations for cooling but not warming

Abstract
--------
Arctic moisture transport is dominated by planetary-scale waves in reanalysis. Planetary waves are influenced by localized Sea-Surface Temperature (SST) features such as the tropical warm pool. Here, an aquaplanet model is used to clarify the link between tropical SST anomalies and Arctic moisture transport. In a zonally uniform setup with no climatological east-west gradients, Arctic moisture transport is dominated by transient planetary waves, as in reanalysis. Warming tropical SSTs by heating the ocean strengthens Arctic moisture transport, mediated mostly by changes in water vapor rather than eddies. This strengthening occurs whether the tropical warming is zonally uniform or localized. Cooling tropical SSTs weakens Arctic moisture transport; however, unlike warming, the pattern matters, with localized cooling producing stronger transport changes owing to non-linear feedbacks in the surface energy budget. Thus, the simulations show that localized tropical SST anomalies influence Arctic moisture transport differently than uniform anomalies, but only in cooling scenarios.

Status
----------
The paper was published in [Geophysical Research Letters](https://agupubs.onlinelibrary.wiley.com/journal/19448007), [doi: 10.1029/2020GL091540](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020GL091540). Comments, questions, and suggestions are appreciated. Feedback can be submitted through github [issues](https://github.com/edunnsigouin/ds21grl/issues) or via e-mail to Etienne Dunn-Sigouin (Etienne.Dunn-Sigouin@uib.no).

Data 
----
The model simulations and analysis for this paper were performed using the Norwegian academic high-performance computing and storage facilities maintained by [Sigma2](https://www.sigma2.no/metacenter). The simulations were performed on the [FRAM](https://documentation.sigma2.no/hpc_machines/fram.html) machine and stored and processed on [NIRD](https://documentation.sigma2.no/files_storage/nird.html).

The simulations are run with the [NCAR CESM2.1.0 CAM5 model](https://www.cesm.ucar.edu/models/) in a slab ocean aquaplanet configuration following the [TRACMIP protocol](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016MS000748). ERA-Interim reanalysis data are available for download from [ECMWF](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim). 

Due to the large volume of raw simulation data (15T), only 'interim' data used to reproduce the figures are included here. Raw and processed data can be made available upon request. 


Code
-------------
The scripts to setup and run the model simulations, process the data and plot the results from the paper are provided. The organization of this project follows loosely from the [cookiecutter-science-project](https://github.com/jbusecke/cookiecutter-science-project) template written by [Julius Busecke](http://jbusecke.github.io/). The project is organized as an installable conda package.

To get setup, first pull the directory from github to your local machine:

``` bash
$ git clone https://github.com/edunnsigouin/ds21grl
```

Then install the conda environment:

``` bash
$ conda env create -f environment.yml
```

Then install the project package:

``` bash
$ python setup.py develop
```

Finally change the project directory in ds21grl/config.py to your local project directory

Support
-------
This research was funded by Research Council of Norway grants Dynamite 255027, Nansen Legacy 276730, and visiting fellowship 287930. [Sigma2](https://www.sigma2.no/metacenter) and the [Bjerknes Prediction Unit (BPU)](https://bcpu.w.uib.no/#:~:text=The%20Bjerknes%20Climate%20Prediction%20Unit,to%20develop%20skilful%20climate%20predictions.) are acknowledged for providing computing and storage facilities under projects NS9625K and NS9039K.

Acknowledgments
----------------
[NCAR](https://ncar.ucar.edu/) and [ECMWF](https://www.ecmwf.int/) are acknowledged for providing free access to the CAM5 model and ERA-interim data. [Tim Woollings](https://www2.physics.ox.ac.uk/contacts/people/woollings) provided helpful discussions and [Ingo Bethke](https://www.bjerknes.uib.no/en/people/ingo-bethke) helped to setup the model. [Julius Busecke](http://jbusecke.github.io/) gave important advice on how to publish reproducible research and organize the github repository for this project.


