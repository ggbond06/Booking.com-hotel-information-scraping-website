from flask import Flask, request, render_template, send_file
import os
from bs4 import BeautifulSoup
import requests
import csv

#website = http://127.0.0.1:5000/!!!!!!!!!

app = Flask(__name__)

def web_scrapper2(url, file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')

        hotel_divs = soup.find_all('div', role="listitem")

        with open(file_name, 'w', newline='', encoding='utf-8-sig') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['hotel_name', 'hotel_location', 'hotel_prices', 'hotel_rating_number', 'hotel_review_number', 'link'])

            for hotel in hotel_divs:
                try:
                    hotel_name = hotel.find('div', class_="f6431b446c a15b38c233").text.strip()
                except:
                    hotel_name = 'N/A'

                try:
                    hotel_location = hotel.find('span', class_="aee5343fdb def9bc142a").text.strip()
                except:
                    hotel_location = 'N/A'

                try:
                    hotel_prices = hotel.find('span', class_="f6431b446c fbfd7c1165 e84eb96b1f").text.strip()
                except:
                    hotel_prices = 'N/A'

                rating_div = hotel.find('div', class_="a3b8729ab1 d86cee9b25")
                hotel_rating_number = rating_div.text.strip().replace('评分', '')[:3] if rating_div else 'N/A'

                review_div = hotel.find('div', class_="abf093bdfe f45d8e4c32 d935416c47")
                if review_div:
                    review_text = review_div.text.strip()
                    hotel_review_number = ''.join(filter(str.isdigit, review_text))
                else:
                    hotel_review_number = 'N/A'

                link_tag = hotel.find('a', href=True)
                link = link_tag.get('href') if link_tag else 'N/A'

                writer.writerow([hotel_name, hotel_location, hotel_prices, hotel_rating_number, hotel_review_number, link])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        filename = request.form.get('filename')

        csv_filename = filename + '.csv'
        web_scrapper2(url, csv_filename)

        return send_file(csv_filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
