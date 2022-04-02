from main import __main__ as genetic_algorithm
import sys
import json

mutation = [[0.05,0.1], [0.1,1], [0.2,2]]
simple_algorithms = ["elite", "roulette", "rank"]
complex_algorithm_names=["tournament_wr", "tournament_nr","truncation"]
complex_algorithm_param_names=["tournament_threshold","tournament_threshold","truncation_k"]
complex_algorithm_params_values = [[0.5,0.65,0.80],[0.5,0.65,0.80],[10,25,50]]
boltzmann_param_names=["boltzmann_tc","boltzmann_t0","boltzmann_k"]
boltzmann_param_values = [[20,10,0.1],[30,10,0.1]]
variability = ["Low", "Medium", "High"]

def simple_algs(total_runs,output_path,avg_output_path):
    simple_header="Selection,Variability,Step,Min,Max\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values.pop("error_threshold",-1)
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(simple_algorithms):
        lines.append([])
        for (index_var,args) in enumerate(mutation):
            lines[index_alg].append([])
            for i in range(1, total_runs+1):
                with open("config.json", "r") as file:
                    json_values = json.load(file)
                json_values.get("selection").update({"method": algorithm})
                json_values.update({"output_path":(output_path + str(i))})
                json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                with open("config.json", "w") as file:
                    json.dump(json_values,file,indent=4)
                print('------------------------------------------------------')
                print('RUN NUMBER '+ str(i))
                genetic_algorithm()
            for i in range(1,total_runs+1):
                file = open("{0}{1}.csv".format(output_path,i))
                lines[index_alg][index_var].append(file.readlines())
                file.close()

    with open(avg_output_path, 'w') as f:
        f.write(simple_header)

        line_len = len(lines[0][0][0])

        for (index_alg, line_alg) in enumerate(lines):
            for (index_var,line_var) in enumerate(line_alg):
                for i in range(0,line_len):
                    current_max_sum = 0
                    current_min_sum = 0
                    for j in range(0,total_runs):
                        line_values = line_var[j][i].split(',')
                        current_min_sum += float(line_values[0])
                        current_max_sum += float(line_values[1])
                    f.write("{0},{1},{2},{3},{4}\n".format(simple_algorithms[index_alg],variability[index_var],i+1,current_min_sum / total_runs, current_max_sum / total_runs))

def complex_algs(total_runs,output_path,avg_output_path):
    complex_header="Selection,Param_Name,Param_Value,Variability,Step,Min,Max\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values.pop("error_threshold",-1)
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(complex_algorithm_names):
        lines.append([])
        for (index_param,algorithm_param) in enumerate(complex_algorithm_params_values[index_alg]):
            lines[index_alg].append([])
            for (index_var,args) in enumerate(mutation):
                lines[index_alg][index_param].append([])
                for i in range(1, total_runs+1):
                    with open("config.json", "r") as file:
                        json_values = json.load(file)
                    json_values.get("selection").update({"method": algorithm, complex_algorithm_param_names[index_alg] : algorithm_param})
                    json_values.update({"output_path":(output_path + str(i))})
                    json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                    with open("config.json", "w") as file:
                        json.dump(json_values,file,indent=4)
                    print('------------------------------------------------------')
                    print('RUN NUMBER '+ str(i))
                    genetic_algorithm()
                for i in range(1,total_runs+1):
                    file = open("{0}{1}.csv".format(output_path,i))
                    lines[index_alg][index_param][index_var].append(file.readlines())
                    file.close()

    with open(avg_output_path, 'w') as f:
        f.write(complex_header)

        line_len = len(lines[0][0][0][0])

        for (index_alg, line_alg) in enumerate(lines):
            for(index_param,line_param) in enumerate(line_alg):
                for (index_var,line_var) in enumerate(line_param):
                    for i in range(0,line_len):
                        current_max_sum = 0
                        current_min_sum = 0
                        for j in range(0,total_runs):
                            line_values = line_var[j][i].split(',')
                            current_min_sum += float(line_values[0])
                            current_max_sum += float(line_values[1])
                        f.write("{0},{1},{2},{3},{4},{5},{6}\n".format(complex_algorithm_names[index_alg], complex_algorithm_param_names[index_alg], complex_algorithm_params_values[index_alg][index_param],variability[index_var],i+1,current_min_sum / total_runs, current_max_sum / total_runs))

def boltzmann_alg(total_runs,output_path,avg_output_path):
    boltzmann_header="Selection,Tc,T0,k,Variability,Step,Min,Max\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"crossbreeding" : {"method": "simple"}})
        json_values.pop("error_threshold",-1)
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_param_comb, params) in enumerate(boltzmann_param_values):
        lines.append([])
        for (index_var,args) in enumerate(mutation):
            lines[index_param_comb].append([])
            for i in range(1, total_runs+1):
                with open("config.json", "r") as file:
                    json_values = json.load(file)
                json_values.get("selection").update({"method": "boltzmann",boltzmann_param_names[0]:params[0],boltzmann_param_names[1]:params[1],boltzmann_param_names[2]:params[2]})
                json_values.update({"output_path":(output_path + str(i))})
                json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                with open("config.json", "w") as file:
                    json.dump(json_values,file,indent=4)
                print('------------------------------------------------------')
                print('RUN NUMBER '+ str(i))
                genetic_algorithm()
            for i in range(1,total_runs+1):
                file = open("{0}{1}.csv".format(output_path,i))
                lines[index_param_comb][index_var].append(file.readlines())
                file.close()

    with open(avg_output_path, 'w') as f:
        f.write(boltzmann_header)

        line_len = len(lines[0][0][0])

        for (index_param_comb, line_param_comb) in enumerate(lines):
                for (index_var,line_var) in enumerate(line_param_comb):
                    for i in range(0,line_len):
                        current_max_sum = 0
                        current_min_sum = 0
                        for j in range(0,total_runs):
                            line_values = line_var[j][i].split(',')
                            current_min_sum += float(line_values[0])
                            current_max_sum += float(line_values[1])
                        f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format("boltzmann",boltzmann_param_values[index_param_comb][0],boltzmann_param_values[index_param_comb][1],boltzmann_param_values[index_param_comb][2],variability[index_var],i+1,current_min_sum / total_runs, current_max_sum / total_runs))


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