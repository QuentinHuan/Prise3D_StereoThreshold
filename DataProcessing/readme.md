Python scripts for data processing:

# description:

* ```main.py```: interface to extract the data from .log Ue4 files and compute the perceptive thresholds
* ```process_log.py```: module that extracts data form .log Ue4 files
* ```process_data.py```: module that computes thresholds
* ```Output.py```: module for plots and visualisation of the results
* ```ExperimentAnalysis.py```: analyse .log files and save the results (used by UE4 project)
* ```ComputeNewStimulusSet.py```: use saved results to compute new stimulus values (used by UE4 project)
* ```MLE_stimulus.py```: module for MLE procedure (interface and performance tests)