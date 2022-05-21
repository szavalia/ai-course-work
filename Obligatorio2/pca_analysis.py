from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def execute(dataset):
    # Standarizing the features
    x = dataset.loc[:, dataset.columns != "Country"].values # Strips country column
    x = StandardScaler().fit_transform(x) # Standarizes

    # Executing pca
    pca_config = PCA()
    principalComponents = pca_config.fit_transform(x)
    return (principalComponents, pca_config.components_[:2])

def generate_output(dataset,principal_components, loadings):
    loading_csv = "loadings.csv"
    components_csv = "components.csv"
    
    with open(loading_csv, "w") as f:
        f.write("column,loading1,loading2\n")
        for (index,column_name) in enumerate(dataset.columns[1:]):
            f.write("{0},{1},{2}\n".format(column_name,loadings[0][index], loadings[1][index]))

    with open(components_csv, "w") as f:
        f.write("country,first_comp,second_comp\n")
        for (index,country) in enumerate(dataset.Country):
            f.write("{0},{1},{2}\n".format(country,principal_components[index][0], principal_components[index][1]))

