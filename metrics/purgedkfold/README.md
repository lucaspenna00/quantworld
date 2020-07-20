# Purged K-Fold

An implementation of Purged K-Fold based on Advances in Financial Machine Learning.
As we know, financial time series cannot be considered as an IID process, because of the serial correlation X(t) ~ X(t+1).
In this way, Purged K-Fold is an alternative solution to traditional K-Fold Cross Validation. It splits the Time Series into K parts like K-Fold. However, besides this splits, this algorithm
add a "purge". It's a time interval that the algorithm doesn't consider to train or test the model, because of the "label overlapping" due to serial correlation.
