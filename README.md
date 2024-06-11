# Sampling script for ASTEC

## Description

A code for sampling operator actions for the ASTEC code. The operator actions are sampled using the Latin hypercube sampling method with uniform distributions.

This code generates a series of input decks stored inside a series of directories "Sample_i/". The only code to be run is "assas_sampling.py".

Two main paths must be specified in config_data inside "assas_sampling.py":
- "path to scenario", which specifies the path to the .mdat file which will be copied in all the directories which will contain the generated input decks.
- "path to ASTEC input", which specifies where the generated input decks will be saved.

Under "uncertain input parameters" the parameters to be sampled should be specified.
Under "certain input parameters" the parameters to be kept fixed should be specified. (If one wants to sample all the parameters then the list which corresponds to "certain input parameters" should be kept empty).

IMPORTANT:
Inside the .mdat file that corresponds to the "path to scenario" there is a line where "path1300" is specified: this path should be modified manually inside the desired .mdat file before running the script assas_sampling.py. The "path1300" should be such that the generated .mdat files (so not the one modified manually) can reach the file "trans.dat" using the path "path1300/STUDY/TRANS/trans.dat". If this does not happen, the ASTEC code will not work.

The file .test is created in the directory specified by confing_data["path to ASTEC input"]. This file allows for the serial computation of ASTEC.
