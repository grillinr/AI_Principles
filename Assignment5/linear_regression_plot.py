import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import random
from datetime import datetime

# team: Derek Corniello, Ryan Sippy, Nathan Grilliot
# linear regression implementation for insurance.csv dataset

# load the dataset and keep only numerical columns
# as required by the assignment
data = pd.read_csv("insurance.csv")
data = data[['age', 'bmi', 'children', 'charges']]


def normal_eq(X, y):
    # implementation of normal equation for linear regression
    # this function calculates the weights w = (X^T X)^(-1) X^T y
    X_b = np.c_[np.ones((X.shape[0], 1)), X]  # add bias term
    return np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y


# this can be replaced to give true randomness
# our writeup rxplores one run of this!
seed = random.seed(datetime.now().timestamp())


# define a bunch of storage vars, used later, annotated with
# what it is used for

# experiment with different training set sizes as required:
# 20%, 40%, 50%, 60%, and 80% of the dataset
train_sizes = [0.2, 0.4, 0.5, 0.6, 0.8]
train_errors = []  # modeling power
test_errors = []   # generalization power
saved_split_50 = None  # store 50% split for part 2

for size in train_sizes:
    # split data into training and test sets with specified size
    # save the 50% split for part 2 of the assignment

    #
    train_set, test_set = train_test_split(
        data, train_size=size, random_state=seed)
    if size == 0.5:
        saved_split_50 = (train_set, test_set)

    # extract features and target variable
    X_train = train_set[['age', 'bmi', 'children']].values
    y_train = train_set['charges'].values
    X_test = test_set[['age', 'bmi', 'children']].values
    y_test = test_set['charges'].values

    # compute weights using normal equation,
    # add bias term to feature matrices for prediction,
    # and make predictions on training and test sets
    w = normal_eq(X_train, y_train)

    X_train_b = np.c_[np.ones((X_train.shape[0], 1)), X_train]
    X_test_b = np.c_[np.ones((X_test.shape[0], 1)), X_test]

    y_train_pred = X_train_b @ w
    y_test_pred = X_test_b @ w

    # calculate mean squared error for both sets
    # (i) modeling power - how well the model fits training data
    # (ii) generalization power - how well the model performs on unseen data
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)

    # save and output the values
    train_errors.append(train_mse)
    test_errors.append(test_mse)
    print(f"Training size: {int(size * 100)}%")
    print(f"\tTrain MSE: {train_mse:.2f}")
    print(f"\tTest MSE: {test_mse:.2f}")

# plot everything here...
plt.figure(figsize=(16, 12))

# plot 1: modeling and generalization errors (top-left)
plt.subplot(2, 2, 1)
plt.plot([int(s * 100) for s in train_sizes],
         train_errors, 'o-', label='Train Error')
plt.plot([int(s * 100) for s in train_sizes],
         test_errors, 's-', label='Test Error')
plt.xlabel("Training Set Size (%)")
plt.ylabel("Mean Squared Error")
plt.title("Modeling vs Generalization Error")
plt.legend()
plt.grid(True)

# part 2: analyze relationship between individual features and charges
# using the 50% train/test split
if saved_split_50:
    train_set, test_set = saved_split_50
else:
    train_set, test_set = train_test_split(
        data, train_size=0.5, random_state=42)

# calculate regression weights
X_train = train_set[['age', 'bmi', 'children']].values
y_train = train_set['charges'].values
w = normal_eq(X_train, y_train)

# plot regression line as function of each feature separately
# holding other features at their mean values
features = ['bmi', 'age', 'children']
fixed_vals = train_set[['age', 'bmi', 'children']].mean().to_dict()

# loop through features and plot in grid positions 2, 3, and 4
for i, feature in enumerate(features):
    # create feature range and prediction inputs
    x_vals = np.linspace(train_set[feature].min(),
                         train_set[feature].max(), 100)
    X_input = []

    # for each value in the range, create a data point with
    # other features held at their mean values
    for x in x_vals:
        row = [fixed_vals['age'], fixed_vals['bmi'], fixed_vals['children']]
        idx = features.index(feature)
        row[idx] = x
        X_input.append(row)

    # prepare inputs and calculate predictions
    X_input = np.array(X_input)
    X_input_b = np.c_[np.ones((X_input.shape[0], 1)), X_input]
    y_pred = X_input_b @ w

    # plot in the appropriate grid position
    plt.subplot(2, 2, i + 2)
    plt.scatter(train_set[feature], train_set['charges'],
                alpha=0.5, label='Training Data')
    plt.plot(x_vals, y_pred, color='red', label='Regression Line')
    plt.xlabel(feature)
    plt.ylabel('Charges')
    plt.title(f'Regression Line vs {feature}')
    plt.legend()
    plt.grid(True)

plt.suptitle("Linear Regression Analysis for Insurance Dataset", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
