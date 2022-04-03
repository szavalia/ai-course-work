from crossbreeding import crossbreeding_chooser
from main import __main__ as genetic_algorithm
import sys
import json

mutation = [[0.05,0.1], [0.1,1], [0.2,2]]
simple_algorithms = ["simple","uniform"]
complex_algorithms = ["multiple"]
complex_algorithm_param_names = ["multiple_point_n"]
complex_algorithm_param_values = [[2,4,6]]
selection_method = "tournament_wr"
selection_param_names = ["tournament_threshold"]
selection_param_values = [0.8]
variability = ["Low", "Medium", "High"]

def simple_algs(total_runs,output_path,avg_output_path):
    simple_header="Crossbreeding,Variability,Step,Min,Max\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"selection" : {"method": selection_method, selection_param_names[0]:selection_param_values[0]}})
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
                json_values.update({"output_path":(output_path + str(i))})
                json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                json_values.get("crossbreeding").update({"method" : algorithm})
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
    complex_header="Crossbreeding,Param_Name,Param_Value,Variability,Step,Min,Max\n"
    lines = []

    with open("config.json", "r") as file:
        json_values = json.load(file)
        json_values.update({"selection" : {"method": selection_method, selection_param_names[0]:selection_param_values[0]}})
        json_values.pop("error_threshold",-1)
        json_values["generations"] = 1000
        json_values["limit_first_generation"] = 10
        json_values["population_size"] = 50
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)

    for (index_alg,algorithm) in enumerate(complex_algorithms):
        lines.append([])
        for (index_param,algorithm_param) in enumerate(complex_algorithm_param_values[index_alg]):
            lines[index_alg].append([])
            for (index_var,args) in enumerate(mutation):
                lines[index_alg][index_param].append([])
                for i in range(1, total_runs+1):
                    with open("config.json", "r") as file:
                        json_values = json.load(file)
                    json_values.update({"output_path":(output_path + str(i))})
                    json_values.update({"mutation": {"method": "uniform","probability": args[0],"a": args[1]}})
                    json_values.get("crossbreeding").update({"method" : algorithm, complex_algorithm_param_names[index_alg] : algorithm_param})
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
                        f.write("{0},{1},{2},{3},{4},{5},{6}\n".format(complex_algorithms[index_alg], complex_algorithm_param_names[index_alg], complex_algorithm_param_values[index_alg][index_param],variability[index_var],i+1,current_min_sum / total_runs, current_max_sum / total_runs))

def __main__(total_runs,type,output_path,avg_output_path):
    if(type == "simple"):
        simple_algs(int(total_runs),output_path,avg_output_path)
    elif(type=="complex"):
        complex_algs(int(total_runs),output_path,avg_output_path)
    else:
        print("Wrong type")
        exit(-1)

if __name__ == "__main__":
    __main__(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])