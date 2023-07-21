import requests


req = requests.get("http://quotes.toscrape.com/js-delayed/")

print(req.text)