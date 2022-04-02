from main import __main__ as genetic_algorithm
import sys
import json

errors = [1e-1,1e-10,1e-50]
mutation = [[0.05,0.1], [0.1,1], [0.2,2]]
simple_algorithms = ["elite", "roulette", "rank"]
complex_algorithm_names=["tournament_wr", "tournament_nr","truncation"]
complex_algorithm_param_names=["tournament_threshold","tournament_threshold","truncation_k"]
complex_algorithm_params_values = [[0.5,0.65,0.80],[0.5,0.65,0.80],[10,25,50]]
boltzmann_param_names=["boltzmann_tc","boltzmann_t0","boltzmann_k"]
boltzmann_param_values = [[10,70,0.1],[10,140,0.1],[10,70,0.5],[10,140,0.5]]
variability = ["Low", "Medium", "High"]

def simple_algs(total_runs,output_path,gen_output_path):
    simple_header="Selection,Variability,Error,Generations\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values["error_threshold"] = 1
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(simple_algorithms):
        lines.append([])
        for(index_err,err_value) in enumerate(errors):
            lines[index_alg].append([])
            for (index_var,args) in enumerate(mutation):
                lines[index_alg][index_err].append([])
                for i in range(1, total_runs+1):
                    with open("config.json", "r") as file:
                        json_values = json.load(file)
                    json_values.get("selection").update({"method": algorithm})
                    json_values.update({"output_path":(output_path + str(i))})
                    json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                    json_values.update({"error_threshold" : err_value})
                    with open("config.json", "w") as file:
                        json.dump(json_values,file,indent=4)
                    print('------------------------------------------------------')
                    print('RUN NUMBER '+ str(i))
                    genetic_algorithm()
                for i in range(1,total_runs+1):
                    file = open("{0}{1}.csv".format(output_path,i))
                    lines[index_alg][index_err][index_var].append(len(file.readlines()))
                    file.close()

    with open(gen_output_path, 'w') as f:
        f.write(simple_header)

        for (index_alg, line_alg) in enumerate(lines):
            for (index_err,line_err) in enumerate(line_alg):
                for(index_var,gen_values) in enumerate(line_err):
                    current_gen_sum = 0
                    for gens in gen_values:
                        current_gen_sum+=gens
                    f.write("{0},{1},{2},{3}\n".format(simple_algorithms[index_alg],variability[index_var],errors[index_err],current_gen_sum // total_runs))

def complex_algs(total_runs,output_path,gen_output_path):
    complex_header="Selection,Param_Name,Param_Value,Variability,Error,Generations\n"
    lines = []
    
    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values["error_threshold"] = 1
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(complex_algorithm_names):
        lines.append([])
        for (index_param,algorithm_param) in enumerate(complex_algorithm_params_values[index_alg]):
            lines[index_alg].append([])
            for(index_err, err_value) in enumerate(errors):
                lines[index_alg][index_param].append([])
                for (index_var,args) in enumerate(mutation):
                    lines[index_alg][index_param][index_err].append([])
                    for i in range(1, total_runs+1):
                        with open("config.json", "r") as file:
                            json_values = json.load(file)
                        json_values.get("selection").update({"method": algorithm, complex_algorithm_param_names[index_alg] : algorithm_param})
                        json_values.update({"output_path":(output_path + str(i))})
                        json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                        json_values.update({"error_threshold" : err_value})
                        with open("config.json", "w") as file:
                            json.dump(json_values,file,indent=4)
                        print('------------------------------------------------------')
                        print('RUN NUMBER '+ str(i))
                        genetic_algorithm()
                    for i in range(1,total_runs+1):
                        file = open("{0}{1}.csv".format(output_path,i))
                        lines[index_alg][index_param][index_err][index_var].append(len(file.readlines()))
                        file.close()

    with open(gen_output_path, 'w') as f:
        f.write(complex_header)

        for (index_alg, line_alg) in enumerate(lines):
            for(index_param,line_param) in enumerate(line_alg):
                for(index_err,line_err) in enumerate(line_param):
                    for (index_var,gen_values) in enumerate(line_err):
                        current_gen_sum = 0
                        for gens in gen_values:
                            current_gen_sum+=gens
                        f.write("{0},{1},{2},{3},{4},{5}\n".format(complex_algorithm_names[index_alg], complex_algorithm_param_names[index_alg], complex_algorithm_params_values[index_alg][index_param],variability[index_var],errors[index_err], current_gen_sum // total_runs))

def boltzmann_alg(total_runs,output_path,gen_output_path):
    boltzmann_header="Selection,Tc,T0,k,Variability,Error,Generations\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values["error_threshold"] = 1
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_param_comb, params) in enumerate(boltzmann_param_values):
        lines.append([])
        for(index_error, err_value) in enumerate(errors):
            lines[index_param_comb].append([])
            for (index_var,args) in enumerate(mutation):
                lines[index_param_comb][index_error].append([])
                for i in range(1, total_runs+1):
                    with open("config.json", "r") as file:
                        json_values = json.load(file)
                    json_values.get("selection").update({"method": "boltzmann",boltzmann_param_names[0]:params[0],boltzmann_param_names[1]:params[1],boltzmann_param_names[2]:params[2]})
                    json_values.update({"output_path":(output_path + str(i))})
                    json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                    json_values.update({"error_threshold" : err_value})
                    with open("config.json", "w") as file:
                        json.dump(json_values,file,indent=4)
                    print('------------------------------------------------------')
                    print('RUN NUMBER '+ str(i))
                    genetic_algorithm()
                for i in range(1,total_runs+1):
                    file = open("{0}{1}.csv".format(output_path,i))
                    lines[index_param_comb][index_error][index_var].append(len(file.readlines()))
                    file.close()

    with open(gen_output_path, 'w') as f:
        f.write(boltzmann_header)

        for (index_param_comb, line_param_comb) in enumerate(lines):
            for(index_err, line_err) in enumerate(line_param_comb):
                for (index_var,gen_values) in enumerate(line_err):
                    current_gen_sum = 0
                    for gens in gen_values:
                        current_gen_sum+=gens
                    f.write("{0},{1},{2},{3},{4},{5},{6}\n".format("boltzmann",boltzmann_param_values[index_param_comb][0],boltzmann_param_values[index_param_comb][1],boltzmann_param_values[index_param_comb][2],variability[index_var],errors[index_err],current_gen_sum//total_runs))


def __main__(total_runs,type,output_path,avg_output_path):
    if(type == "simple"):
        simple_algs(int(total_runs),output_path,avg_output_path)
    elif(type=="complex"):
        complex_algs(int(total_runs),output_path,avg_output_path)
    elif(type=="boltzmann"):
        boltzmann_alg(int(total_runs),output_path,avg_output_path)
    else:
        print("Wrong type")
        exit(-1)

if __name__ == "__main__":
    __main__(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])