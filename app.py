from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


def get_conversion_factor(source_currency, target_currency):
    url = ("https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_s42hADrwNuU5uJXnfk8WiRTvTSDsYTxyfiNG0Ks8"
           "&currencies={}&base_currency={}").format(target_currency, source_currency, )
    data = requests.get(url)
    data = data.json()
    #print("conversion factor from ",source_currency, " to ", target_currency, " is ")
    #print(data)
    fac = data['data'][str(target_currency)]
    #print(fac)
    return fac


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(amount, source_currency)
    cf = get_conversion_factor(source_currency,target_currency)
    final_amount = cf * amount
    final_amount = round(final_amount,2)
    print("final amount is {}".format(final_amount))
    res = {'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)}
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
