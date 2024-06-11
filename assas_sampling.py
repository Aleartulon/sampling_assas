import os
import numpy as np
import shutil
from scipy.stats import uniform
from pyDOE import lhs 

#dictionary with necessary specifications is given
config_data = {
"path to scenario": "SBO_fb_1300_LIKE_SIMPLIFIED_ASSAS.mdat",
"name of scenario file": "SBO_fb_1300_LIKE_SIMPLIFIED_ASSAS.mdat",
"path to ASTEC input": "inputs_directory/",
"sampling algorithm": "LHS",
"number of samples": 20,
"uncertain input parameters": [
{"name": "tpesp", "distribution": "uniform", "min": 13000.0, "max": 20000.0}, #list of operator actions to be sampled
{"name": "t_fbseb", "distribution": "uniform", "min": 12040.0, "max": 20050.0}
],
"certain input parameters": [
    {"name": "tpessg", "value" : 20000.} #list of operator actions to be kept fixed. If no operator actions are to be fixed then
]                                        #the list should be kept empty.
}


def rescale_uniform(original_lhs, pdf_params):
    rescaled = uniform.ppf(q=original_lhs, loc=pdf_params['min'], scale=pdf_params['max'] - pdf_params['min'])
    return rescaled

def create_driving_ana_file(dictionary, uncertain_parameters_values, path_to_file):
   with open(path_to_file + "/driving.ana", "w") as file:
    for count, element in enumerate(uncertain_parameters_values):
        if count < uncertain_parameters_num:
            name = dictionary["uncertain input parameters"][count]["name"] + " ="
            file.write(f"{name} {element}\n")
        else:
            name = dictionary["certain input parameters"][count-uncertain_parameters_num]["name"] + " ="
            file.write(f"{name} {element}\n")

# sampling uncertain parameters
uncertain_parameters_num = len(config_data["uncertain input parameters"])
certain_parameters_num = len(config_data["certain input parameters"])
samples_num = config_data["number of samples"]

sampled_matrix = np.zeros((samples_num, uncertain_parameters_num), dtype=float, order='C')
original_sampling = lhs(uncertain_parameters_num, samples=samples_num, criterion='center')

for par_i in range(uncertain_parameters_num):
    current_par = config_data["uncertain input parameters"][par_i]
    pdf_params = current_par["distribution"]
    if pdf_params.lower() == 'uniform':
        sampled_matrix[:, par_i] = rescale_uniform(original_sampling[:, par_i], current_par)


# concatenate certain parameters
for param in config_data["certain input parameters"]:
    sampled_matrix = np.hstack((sampled_matrix, np.ones((samples_num,1))*param["value"]))


# preparing the ASTEC input decks
#BE CAREFUL TO NOT OVERWRITE EXISTING DIRECTORIES!!!

filename = os.path.basename(config_data["path to scenario"])
for sample_i in range(samples_num):
    if os.path.exists(config_data["path to ASTEC input"] + "/Sample_"+str(sample_i)):
        shutil.rmtree(config_data["path to ASTEC input"] + "/Sample_"+str(sample_i))
    os.makedirs(config_data["path to ASTEC input"] + "/Sample_"+str(sample_i).format(sample_i), exist_ok=True)
    
    shutil.copyfile(config_data["path to scenario"], os.path.join(config_data["path to ASTEC input"] + "/Sample_"+str(sample_i), filename))

    for param in range(uncertain_parameters_num + certain_parameters_num):
        create_driving_ana_file(config_data, sampled_matrix[sample_i], config_data["path to ASTEC input"] + "/Sample_"+str(sample_i))
    
#create the .test file which allows for serial computation of ASTEC

with open(config_data["path to ASTEC input"]+"/test.test", 'w') as file:
    
    name_file = config_data["name of scenario file"]
    for i in range(samples_num):
        file.write(f"Sample_{i}/{name_file};Sample_{i}\n")