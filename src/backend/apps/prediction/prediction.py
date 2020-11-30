from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt


def get_data():
    return pd.read_csv('A.csv', infer_datetime_format=True)


def process_data(data, degree):
    poly = PolynomialFeatures(degree=degree)
    data_poly = poly.fit_transform(data)
    return data_poly


if __name__ == '__main__':
    degree = 3

    data = get_data()
    t = data['High']
    X = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    #Model data
    X_poly = process_data(X, degree)
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, t)

    #Plot data
    plt.xlabel('Date')
    plt.ylabel('Price-High')
    plt.title('Degree: ' + str(degree))
    plt.plot(X['Date'], t)
    plt.plot(X['Date'], lin_reg.predict(X_poly), color='red')
    plt.show()