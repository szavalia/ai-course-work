from crossbreeding import crossbreeding_chooser
from main import __main__ as genetic_algorithm
import sys
import json

errors = [1e-1,1e-10,1e-50]
algorithms = ["uniform","normal"]
algorithms_param_names = ["a","sigma"]
algorithms_param_values = [4,2]
selection_method = "tournament_wr"
selection_param_names = ["tournament_threshold"]
selection_param_values = [0.8]
crossbreeding_method = "uniform"
probabilities = [0.05,0.1,0.2,0.5]

header="Mutation,Param_Name,Param_Value,Probability,Error,Generations\n"

def run_experiment(total_runs,output_path,gen_output_path):
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"selection" : {"method": selection_method, selection_param_names[0]:selection_param_values[0]}})
        json_values.update({"crossbreeding" : {"method": crossbreeding_method}})
        json_values["error_threshold"]=1
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(algorithms):
        lines.append([])
        for (index_prob,prob) in enumerate(probabilities):
            lines[index_alg].append([])
            for(index_err, err_value) in enumerate(errors):
                lines[index_alg][index_prob].append([])
                for i in range(1, total_runs+1):
                    with open("config.json", "r") as file:
                        json_values = json.load(file)
                        json_values.update({"output_path":(output_path + str(i))})
                        json_values.update({"mutation": {"method":algorithm,"probability": prob,algorithms_param_names[index_alg]:algorithms_param_values[index_alg]}})
                        json_values.update({"error_threshold" : err_value})
                    with open("config.json", "w") as file:
                        json.dump(json_values,file,indent=4)
                    print('------------------------------------------------------')
                    print('RUN NUMBER '+ str(i))
                    genetic_algorithm()
                for i in range(1,total_runs+1):
                    file = open("{0}{1}.csv".format(output_path,i))
                    lines[index_alg][index_prob][index_err].append(len(file.readlines()))
                    file.close()

    with open(gen_output_path, 'w') as f:
        f.write(header)

        for (index_alg, line_alg) in enumerate(lines):
            for(index_prob,line_prob) in enumerate(line_alg):
                for(index_err,gen_values) in enumerate(line_prob):
                    current_gen_sum = 0
                    for gens in gen_values:
                        current_gen_sum+=gens
                    f.write("{0},{1},{2},{3},{4},{5}\n".format(algorithms[index_alg], algorithms_param_names[index_alg], algorithms_param_values[index_alg],probabilities[index_prob],errors[index_err], current_gen_sum // total_runs))

def __main__(total_runs,output_path,avg_output_path):
    run_experiment((int)(total_runs),output_path,avg_output_path)

if __name__ == "__main__":
    __main__(sys.argv[1],sys.argv[2],sys.argv[3])