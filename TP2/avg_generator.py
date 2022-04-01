from main import __main__ as genetic_algorithm
import sys
import json

total_runs = int(sys.argv[1])
path = sys.argv[2]
output_path = sys.argv[3]

for i in range(1, total_runs+1):
    print(i)
    with open("config.json", "r") as file:
        json_values = json.load(file)
    json_values.update({"output_path":(path + str(i))})
    with open("config.json", "w") as file:
        json.dump(json_values,file,indent=4)
    print('------------------------------------------------------')
    print('RUN NUMBER '+ str(i))
    genetic_algorithm()

lines = []

for i in range(1,total_runs+1):
    file = open("{0}{1}.csv".format(path,i))
    lines.append(file.readlines())
    file.close()

with open(output_path, 'w') as f:

    line_len = len(lines[0])

    for i in range(0,line_len):
        current_max_sum = 0
        current_min_sum = 0
        for j in range(0,total_runs):
            line_values = lines[j][i].split(',')
            current_min_sum += float(line_values[0])
            current_max_sum += float(line_values[1])
        f.write("{0},{1}\n".format(current_min_sum / total_runs, current_max_sum / total_runs))