from io_parser import generate_hopfield_output, parse_properties,generate_kohonen_output,generate_oja_output
from algorithms.hopfield import execute as hopfield_execute
from algorithms.kohonen import execute as kohonen_execute
from algorithms.oja import execute as oja_execute
from models import HopfieldObservables, KohonenObservables, OjaObservables
import numpy as np
from letters import alphabet

def __main__():
    properties = parse_properties()
    if(properties.method == "hopfield"):
        observables:HopfieldObservables = hopfield_execute(properties)
        generate_hopfield_output(properties,observables)
    elif(properties.method == "kohonen"):
        observables:KohonenObservables = kohonen_execute(properties)
        generate_kohonen_output(properties,observables)
    elif(properties.method == "oja"):
        observables:OjaObservables = oja_execute(properties)
        generate_oja_output(properties,observables)

if __name__ == "__main__":
    __main__()