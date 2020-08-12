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


def plot_scatter_test_true(Y_pred, Y_true, experimento=None):
    
    x = np.arange(0, len(Y_pred))
    
    fig = plt.figure(figsize=(15,8))
    
    ax1 = fig.add_subplot()
    
    ax1.scatter(x, Y_pred, c='orange', marker='x', label='predicted')
    ax1.scatter(x, Y_true, c='blue', marker='o', label='true')
    
    plt.title(str(experimento)+" | True and Predicted")
        
    plt.legend()
    
    plt.show()
    
