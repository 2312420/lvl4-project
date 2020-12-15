from flask import Flask, request
import flask
import json

# Python libs
import prediction
import sentence_to_points

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

if __name__ == '__main__':
    app.run(port=5004)


# Updates verdict of company in database
#def update_verdict(stock_code, verdict, preds):
#    url = baseurl + '/company/predictions'
#    payload = {'stock_code': stock_code, 'verdict': verdict, 'predictions': json.dumps(preds)}
#    r = requests.post(url, json=payload)
#    if r.status_code == 200:
#        return "verdict updated"
#    else:
#        return "something went wrong"