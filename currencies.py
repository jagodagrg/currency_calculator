from flask import Flask, render_template, request
import requests
import csv


app = Flask(__name__)

response = requests.get(
    "http://api.nbp.pl/api/exchangerates/tables/C?format=json")ies
data = response.json()

rates = (data[0])["rates"]

with open('/home/jagoda/Desktop/Kodilla/Python/currency_calculator/currencies.csv', 'w', newline='') as csvfile:
    currencywriter = csv.writer(csvfile, delimiter=';')
    currencywriter.writerow(['currency'] + ['code'] + ['bid'] + ['ask'])
    codes = []
    for item in rates:
        currencywriter.writerow([
            item['currency']] + [item['code']] + [str(item['bid'])] + [str(item['ask'])])
        codes.append(item['code'])


@app.route("/calculator/", methods=['GET', 'POST'])
def calculate_exchange_rate():
    currency = None
    result = 0
    if request.method == 'POST':
        currency = request.form['currency']
        amount = request.form['amount']
        for rate in rates:
            if rate['code'] == currency:
                result = round(float(amount) * float(rate['ask']), 2)
    return render_template('currency_calculator.html', codes=codes, result=result, currency=currency)


if __name__ == '__main__':
    app.run(debug=True)
