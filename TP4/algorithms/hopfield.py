from models import HopfieldObservables, HopfieldProperties
import numpy as np

def execute(properties:HopfieldProperties):
    
    # Build starting W
    # patterns is K transposed
    patterns = np.array(properties.patterns)
    kt = patterns.transpose()
    k = patterns
    w = np.dot(kt, k)
    w = np.multiply(w, 1/len(patterns[0]))   # N is number of elements in patterns
    np.fill_diagonal(w, 0)                  # 0s in diagonal

    # Execute algorithm for each letter with noise
    pattern_states = []
    for pattern in properties.noise_patterns:
        states = execute_single(w, pattern)
        pattern_states.append(states)
    return HopfieldObservables(pattern_states)

def execute_single(w, pattern):
    pattern = np.array(pattern)
    state = pattern.copy()
    stop = False
    states = [state.copy()]
    while not stop:

        # Calculate h
        h = np.dot(w,state.transpose())
        
        # Update state
        for (index, hi) in enumerate(h):
            if hi == 0:
                continue
            state[index] = np.sign(hi)

        # Check end condition
        if ((state == states[-1]).all()):
            stop = True
            continue
        states.append(state.copy())
    return states