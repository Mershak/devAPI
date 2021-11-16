from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
weather = "https://weather.com/weather/monthly/l/60eb7796d033a593c3294ffa7d76578ee16343ee1b14bbab570b30eee2a0fb0e"
yelpAPI = "ivTLzvNEFKorlR5CDuV6p9Qe_wIOrN0-vvnCedopKB-aXWGH1HVBtloCk1mFIVfSHNw65eG0BR_iQaOC2ydW-H2_IV_0GxpMTXVQOTH5Z_pfOfKnqMgNzsrHuXaTYXYx"
yelpBusinessURL = "https://api.yelp.com/v3/businesses/search"
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return "<h1>Hello there<h1/>"

@app.route("/scraper", methods = ["GET"])
def scraper():
    page = requests.get(weather)
    parsedPage = BeautifulSoup(page.content, "html.parser")

    grid = parsedPage.find("div", class_= "Calendar--gridWrapper--1oa1f")
    temps = grid.find_all("div", class_= "CalendarDateCell--tempHigh--2VBba")
    days = grid.find_all("span", class_= "CalendarDateCell--date--3Fw3h")
    tempDic = []
    for i in (range(len(days))):
        tempDic.append({
            "day" : days[i].text,
            "temp" : temps[i].text
        })
    return jsonify(tempDic)

@app.route("/api", methods = ["GET"])
def api():
    headers = {"Authorization": ("Bearer " + yelpAPI)}
    params = {"term": "restaurant", "location":"Eugene"}
    result = requests.get(yelpBusinessURL, headers=headers, params=params)
    response = result.json()
    businesses = response["businesses"]
    idList = []
    indexList = range(20)
    for businessIndex in range(len(businesses)):
        idList.append({businessIndex: businesses[businessIndex]["id"]})
    return jsonify(idList)


if __name__ == '__main__':
    app.run()