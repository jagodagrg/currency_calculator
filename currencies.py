from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)


@app.route("/calculator/", methods=['GET', 'POST'])
def calculate_exchange_rate():
    currency = None
    result = 0
    if request.method == 'POST':
        currency = request.form['currency']
        amount = request.form['amount']
        for code, rate in exchange_rates.items():
            if code == currency:
                result = round(float(amount) * float(rate), 2)
    return render_template('currency_calculator.html', currency=currency, codes=exchange_rates.keys(), result=result)


if __name__ == '__main__':
    response = requests.get(
        "http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates = (data[0])["rates"]
    exchange_rates = {}
    for rate in rates:
        exchange_rates[rate['code']] = rate['ask']
    with open('currencies.csv', 'w', newline='') as csvfile:
        currencywriter = csv.writer(csvfile, delimiter=';')
        currencywriter.writerow(['currency', 'code', 'bid', 'ask'])
        for rate in rates:
            currencywriter.writerow(
                [rate['currency'], rate['code'], str(rate['bid']), str(rate['ask'])])
    app.run(debug=True)
