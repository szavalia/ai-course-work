import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def execute(dataset):
    # Standarizing the features
    # x = dataset.loc[:, dataset.columns != "Country"].values # Strips country column
    x = StandardScaler().fit_transform(dataset) # Standarizes

    # Executing pca
    pca_config = PCA()
    principalComponents = pca_config.fit_transform(x)
    return (principalComponents, pca_config.components_[:2])

