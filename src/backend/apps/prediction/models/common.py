# Common functions used between both models

# Take time feature and expand it into multiple features
def expand_time(df):
    df["day_month"] = df["time"].dt.month
    df["day_week"] = df["time"].dt.isocalendar().week
    df["day"] = df["time"].dt.day
    df["day_hour"] = df["time"].dt.hour
    df["day_minute"] = df["time"].dt.minute
    df["day_dayofweek"] = df["time"].dt.dayofweek
    return df