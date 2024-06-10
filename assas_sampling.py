import json
import os
import numpy as np
from scipy.stats import uniform
from pyDOE import lhs  # https://pythonhosted.org/pyDOE/randomized.html#latin-hypercube

#json input_file(config.dat)
config_data = {
"scenario": "SBO",
"path to ASTEC input": "trial/",
"sampling algorithm": "LHS",
"number of samples": 5,
"uncertain input parameters": [
{"name": "tpesp", "distribution": "uniform", "min": 2.0, "max": 3.0, "value": None},
{"name": "t_fbseb", "distribution": "uniform", "min": 10.0, "max": 11.0, "value": None},
{"name": "trial", "distribution": "uniform", "min": 10.0, "max": 11.0, "value": 5.}
]
}


def rescale_uniform(original_lhs, pdf_params):
    #uniform = scipy.stats.uniform()
    rescaled = uniform.ppf(q=original_lhs, loc=pdf_params['min'], scale=pdf_params['max'] - pdf_params['min'])
    return rescaled

def create_driving_ana_file(dictionary, uncertain_parameters_values, path_to_file):
   #open driving.ana next to .mdat - file.open(path_to_file, file_name)
   with open(path_to_file + "/driving.ana", "w") as file:
    for count, element in enumerate(uncertain_parameters_values):
        name = dictionary["uncertain input parameters"][count]["name"] + " ="
        file.write(f"{name} {element}\n")



#with open(input_file, 'r') as f:
#    try:
#        input_data = json.load(f)
#    except ValueError:
#        print("Reading JSON failed")
#        quit(-1)

# sampling
parameters_num = len(config_data["uncertain input parameters"])
samples_num = config_data["number of samples"]

sampled_matrix = np.zeros((samples_num, parameters_num), dtype=float, order='C')
original_sampling = lhs(parameters_num, samples=samples_num, criterion='center')

for par_i in range(parameters_num):
    current_par = config_data["uncertain input parameters"][par_i]
    pdf_params = current_par["distribution"]
    if pdf_params.lower() == 'uniform':
        sampled_matrix[:, par_i] = rescale_uniform(original_sampling[:, par_i], current_par)

print(sampled_matrix)

# preparing the ASTEC input decks
# create main output folder

for sample_i in range(samples_num):
#     # inside the main output folder create the folder for sample
    os.makedirs(config_data["path to ASTEC input"] + "/Sample_"+str(sample_i).format(sample_i), exist_ok=True)
#     # copy original input to sample folder
#     copytree function
#     create driving.ana file - call create_driving_ana_file function
    for param in range(parameters_num):
        create_driving_ana_file(config_data, sampled_matrix[sample_i], config_data["path to ASTEC input"] + "/Sample_"+str(sample_i))