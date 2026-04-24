from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_data():

    session = requests.Session()

    login_url = "http://ecensus.nsonepal.gov.np:81/necReporting/public/index.php"
    data_url = "http://ecensus.nsonepal.gov.np:81/necReporting/public/view_reports.php"

    payload = {
        "username": "ec_off312",
        "password": "6004"
    }

    # 🔐 LOGIN REQUEST
    session.post(login_url, data=payload)

    # 📄 FETCH DATA PAGE
    res = session.get(data_url)

    # 🔍 DEBUG OUTPUT (IMPORTANT)
    print("STATUS:", res.status_code)
    print("FINAL URL:", res.url)
    print("HTML START:")
    print(res.text[:1500])

    # 🧠 PARSE HTML
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table")

    result = []

    # 🛑 SAFETY CHECK (prevents crash)
    if not table:
        return [["ERROR: Table no- login failed or page changed"]]

    for row in table.find_all("tr"):
        cols = [col.text.strip() for col in row.find_all(["td", "th"])]
        if cols:
            result.append(cols)

    return result


@app.route("/data")
def data():
    return jsonify(scrape_data())
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
