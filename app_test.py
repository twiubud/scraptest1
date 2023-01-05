from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
@cross_origin
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            uclient = uReq(flipkart_url)
            flipkart_page = uclient.read()
            uclient.close()
            flipkart_html = bs(flipkart_page, 'html.parser')
            bigboxes = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
            product_result = requests.get(product_link)
            product_result.encoding = 'utf-8'
            product_html = bs(product_result, 'html_parser')
            print(product_html)
            commentboxes = product_html.find_all('div', {"class": "_16PBlm"})
            


