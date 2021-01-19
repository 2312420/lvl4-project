from modules import company_points

stock_code = "FB"
data = company_points.get_data(stock_code, "2020-11-11", "2020-12-15",)
print(data)