# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta

from models import common, sentiment_model

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn import decomposition
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

import numpy

# Used to make actual predictions
def linear_regression(df, target_feature, future_days, end_date=-1):
    data = common.expand_time(df.copy())

    x_train = data[['sentiment', 'day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data[target_feature]


    x_future = sentiment_model.future_sentiment_regression(x_train, future_days, end_date)

    x_future = x_future[['sentiment', 'day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]

    x_future = pd.concat([x_train, x_future])

    # MODEL

    #model = LinearRegression().fit(x_train, y_train)

    #clf = make_pipeline(StandardScaler(), SVR(gamma='auto'))

    #clf = make_pipeline(StandardScaler(), DecisionTreeRegressor())
    #clf = DecisionTreeRegressor()

    #clf = make_pipeline(StandardScaler(), DecisionTreeRegressor())

    #std_slc = StandardScaler()
    #pca = decomposition.PCA()
    #dtreeReg = DecisionTreeRegressor()

    #pipe = Pipeline(steps=[("std_slc", std_slc), ("pca", pca), ("dtreeReg", dtreeReg)])

    #print(x_train)
    #print(y_train)

    #n_components = list(range(1, x_train.shape[1]+1,1))

    #criterion = ['gini', 'entropy']
    #max_depth = [2, 4, 6, 8, 10, 12]
    #max_depth = None
    #print(max_depth)

    #parameters = dict(pca__n_components=n_components,
      #                dec_tree__criterion=criterion,
     #                 dec_tree__max_depth=max_depth)

    #clf = GridSearchCV(pipe, parameters)



    #clf = make_pipeline(StandardScaler(),RandomForestRegressor())
    clf = make_pipeline(RandomForestRegressor())

    model = clf.fit(x_train, y_train)


    # Prediction
    preds = model.predict(x_future)
    x_future['predictions'] = preds

    # Plot graph (for testing)
    #plt.plot(data['close'])
    #plt.plot(x_future['predictions'], color='green', alpha=0.4)
    #plt.xticks(fontsize=5)
    #plt.show()

    return x_future