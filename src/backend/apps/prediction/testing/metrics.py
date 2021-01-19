import yfinance as yf

def squared_loss(df, stock_code):
    stock_data = yf.Ticker(stock_code)

    times = []
    prices = []
    for point in df:
        times.append()



    def squared_loss(company):
        predictions = json.loads(company['predictions'])
        if predictions != "[]":
            stock_data = yf.Ticker(company['stock_code'])
            start_point = datetime.strptime(predictions[0][0], "%Y-%m-%d %H:%M:%S")
            end_point = datetime.strptime(predictions[-1][0], "%Y-%m-%d %H:%M:%S")
            stock_df = stock_data.history(start=start_point, end=end_point)
            predictions_df = pd.DataFrame(predictions)

            # Get mean squared error for full all predictions
            times = []
            prices = []
            for point in predictions:
                times.append(point[0])
                prices.append(point[1])

            true = []
            pred = []
            for index, point in stock_df.iterrows():
                if index.__str__() in times:
                    pos = times.index(index.__str__())
                    true.append(point['Close'])
                    pred.append(prices[pos])

            total_mean_squared_loss = mean_squared_error(true, pred)

            # Get mean squared error for past thirty days
            past_30_days = end_point - timedelta(days=30)
            true = []
            pred = []
            for index, point in stock_df[past_30_days:].iterrows():
                if index.__str__() in times:
                    pos = times.index(index.__str__())
                    true.append(point['Close'])
                    pred.append(prices[pos])

            past_30_days_loss = mean_squared_error(true, pred)

            return total_mean_squared_loss, past_30_days_loss
        else:
            return None, None