from models import Metrics, Properties
import json

def generate_output(metrics,properties:Properties):
    for metric in metrics:
        print("Method: {0}\n\tMin: {1}\n\tX: {2}\n\tTime: {3}".format(metric.method, metric.error, metric.x, metric.time))
    
# Receive parameters from config.json and encapsulate them into properties object
def parse_properties():

    file = open('config.json')
    json_values = json.load(file)
    file.close()    
    
    initial_values = json_values.get("initial_values")
    
    if initial_values == None:
        print("Initial values required")
        exit(-1)

    for initial_value in initial_values:
        if len(initial_value) != 3:
            print("Initial value must be an array of 3 coordinates")
            exit(-1)

    initial_results = json_values.get("initial_results")
    if initial_results == None:
        print("Initial results required")
        exit(-1)
    for result in initial_results:
        if(result !=0 and result != 1):
            print("Invalid initial result. Only 1 or 0 is accepted")
            exit(-1)

    if len(initial_results) == 0 or len(initial_values) == 0 or len(initial_results) != len(initial_values):
        print("Invalid initial conditions. Either an initial value or an initial result is missing")
        exit(-1)

    return Properties(initial_values,initial_results)

