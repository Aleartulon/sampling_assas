# Sampling script for ASTEC

## Description

A code for sampling operator actions for the ASTEC code. The operator actions are sampled using the Latin hypercube sampling method with uniform distributions.

Two main paths must be specified in config_data:
- "path to scenario", which specifies the path to the .mdat file which will be copied in all the directories which will contain the generated input decks.
- "path to ASTEC input", which specifies where the generated input decks will be saved.

Under "uncertain input parameters" the parameters to be sampled should be specified.
Under "certain input parameters" the parameters to be kept fixed should be specified. (If one wants to sample all the parameters then the list which corresponds to "certain input parameters" should be kept empty).

Inside the .mdat file that corresponds to the "path to scenario" there is a line where "path1300" is specified: this path should be modified manually inside the desired .mdat file before running the script assas_sampling.py. The "path1300" should be such that the generated .mdat files can reach the file "trans.dat" using the path "path1300/STUDY/TRANS/trans.dat".

