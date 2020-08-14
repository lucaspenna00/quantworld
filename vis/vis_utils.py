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
   

def get_precision_recall_curves(Y_prob, Y_teste):
    
    def classifier(Y_prob, threshold):

    pred = []

    for prob in Y_prob:

        if prob >= threshold:

            pred.append(1)

        else:

            pred.append(0)

    return pred
    
    precisions = []
    recalls = []

    thresholds = np.linspace(0, 1, 100)

    for threshold in thresholds:

        Y_pred = classifier(Y_prob, threshold)

        precisions.append(precision_score(Y_pred, Y_teste))
        recalls.append(recall_score(Y_pred, Y_teste))

    plt.figure()
    plt.plot(precisions, color='orange', label='precision')
    plt.plot(recalls, color='blue', label='recall')
    plt.legend()
    plt.title("Precisions and Recall vs threholds")
    plt.show()
