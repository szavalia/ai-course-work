class HopfieldProperties:
    def __init__(self,letters,patterns,noise_prob, noise_patterns):
        self.method = "hopfield"
        self.letters = letters
        self.patterns = patterns
        self.noise_patterns = noise_patterns
        self.noise_prob = noise_prob

class HopfieldObservables:
    def __init__(self,pattern_states):
        self.pattern_states = pattern_states