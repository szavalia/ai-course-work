from io_parser import generate_hopfield_output, parse_properties
from algorithms.hopfield import execute as hopfield_execute
from models import HopfieldObservables
import numpy as np
from letters import alphabet

def __main__():
    properties = parse_properties()
    if(properties.method == "hopfield"):
        observables:HopfieldObservables = hopfield_execute(properties)
        generate_hopfield_output(properties,observables)


if __name__ == "__main__":
    __main__()