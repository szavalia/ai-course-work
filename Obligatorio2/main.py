import pandas as pd
from pca_analysis import execute,generate_output

def __main__():
    dataset = pd.read_csv("resources/europe.csv", delimiter=",")
    (principal_components, loadings) = execute(dataset)
    generate_output(dataset,principal_components,loadings)

if __name__ == "__main__":
    __main__()
