from io_parser import parse_properties
from algorithms.hopfield import execute as hopfield_execute
from models import HopfieldObservables
import numpy as np
from letters import alphabet

def __main__():
    properties = parse_properties()
    if(properties.method == "hopfield"):
        observables:HopfieldObservables = hopfield_execute(properties)


if __name__ == "__main__":
    __main__()