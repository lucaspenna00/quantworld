import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, spearmanr

def scatter_heat_map(x, y, title):

    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    plt.figure()
    plt.scatter(x, y, marker='o', c=z, edgecolor='')
    plt.colorbar()
    plt.title(title)
    plt.show()
    print("Correlação de Pearson: ", np.corrcoef(x, y)[0][1])
    print("Correlação de Spearman: ", spearmanr(x, y)[0])
