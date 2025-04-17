from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
data = pd.read_csv("Assignment5/insurance.csv")

# Select only numeric columns
data = data.select_dtypes(include=['number'])

# Split the dataset into train and test sets
for split in [0.2, 0.4, 0.5, 0.6, 0.8]:
    train, test = train_test_split(data, test_size=split, random_state=42)

    regress = LinearRegression()
    regress.fit(train.drop(columns=['charges']), train['charges'])
    predictions = regress.predict(test.drop(columns=['charges']))
    test_mse = mean_squared_error(test['charges'], predictions)
    train_mse = mean_squared_error(train['charges'], regress.predict(train.drop(columns=['charges'])))

    print(f"Test Size: {split}")
    print(f"\tTrain Mean Squared Error: {train_mse}")
    print(f"\tTest Mean Squared Error: {test_mse}")


train, test = train_test_split(data, test_size=0.5, random_state=42)
regress = LinearRegression()
regress.fit(train.drop(columns=['charges']), train['charges'])
predictions = regress.predict(test.drop(columns=['charges']))

# Plotting the results
plt.figure(figsize=(10, 5))
for feature in ['bmi', 'children', 'age']:
    plt.plot(train[feature], train['charges'], 'o', label=feature, alpha=0.5)


xseq = np.linspace(0, max(test['age']), num=test.shape[0])
plt.plot(xseq, predictions, "-")
plt.xlabel('Feature Value')
plt.ylabel('Predicted Charges')
plt.title('Predicted Charges vs Feature Value')
plt.legend()
plt.show()