from flask import Flask, request
import flask
import json

# Python libs
from modules import prediction, sentence_to_points
import custom_pred

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Prediction API"


@app.route('/predictions', methods=['GET'])
def prediction_for_company():
    company = request.get_json()
    stock_code, verdict, new_preds = prediction.make_prediction(company)
    print(new_preds)
    return json.dumps({'stock_code': stock_code, 'verdict': verdict, 'new_preds': new_preds})


@app.route('/points/sentences', methods=['POST'])
def sentence_points():
    sentence = request.get_json()
    sentence_to_points.sentence_to_point(sentence)
    return flask.Response(status=200)


@app.route('/predictions/custom', methods=['POST'])
def custom_predictions():
    try:
        content = request.get_json()
        start_date = content['start_date']
        end_date = content['end_date']
        company = content['stock_code']
        output = custom_pred.custom_prediction(start_date, end_date, company)
    except
        return

if __name__ == '__main__':
    app.run(port=5004)

