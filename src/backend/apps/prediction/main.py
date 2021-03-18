from flask import Flask, request
import flask
import json

# Python libs
from modules import prediction, sentence_to_point
import custom_pred

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Prediction API"


@app.route('/predictions', methods=['GET'])
def prediction_for_company():
    company = request.get_json()
    stock_code, verdict, new_preds, new_change = prediction.new_predictions(company)
    return json.dumps({'stock_code': stock_code, 'verdict': verdict, 'predictions': new_preds, 'change': new_change})


@app.route('/points/sentences', methods=['POST'])
def sentence_points():
    sentence = request.get_json()
    sentence_to_point.sentence_to_point(sentence)
    return flask.Response(status=200)


@app.route('/predictions/custom', methods=['POST'])
def custom_predictions():
    try:
        content = request.get_json()
        start_date = content['start_date']
        end_date = content['end_date']
        company = content['stock_code']
        try:
            output = custom_pred.custom_predictions(start_date, end_date, company)
            return json.dumps(output)
        except Exception as i:
            return flask.Response(status=400)
    except:
        return flask.Response(status=405)


if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5004)