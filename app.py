import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

url = 'https://www.alsoug.com/currency'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

app = FastAPI()

@app.get('/')
def health():
    return {'Server is Healthy 🌐': True}

@app.get('/rates')
def root():
    try:
        with requests.Session() as session:
            page = session.get(url, headers=headers, timeout=10)
            page.encoding = 'utf-8'
            page.raise_for_status()

            soup = BeautifulSoup(page.text, 'html.parser')

            sopo = soup.find_all('sapn') # Still check for 'sapn'

            rates = []
            for tag in sopo:
                text_value = tag.get_text(strip=True).replace(',', '')
                try:
                    num = float(text_value)
                    rates.append(num)
                except ValueError:
                    continue

            if len(rates) < 12:
                return {
                    "error": f"Expected at least 12 numeric rates, found {len(rates)}",
                    "collected_rates": rates
                }

            usd, busd = rates[0], rates[1]
            aed, baed = rates[2], rates[3]
            eur, beur = rates[4], rates[5]
            sar, bsar = rates[6], rates[7]
            egp, begp = rates[8], rates[9]
            qar, bqar = rates[10], rates[11]

    except Exception as e:
        return {"error": str(e)}

    return {
        'sdg_rates': {
            'USD': usd, 'Black_USD': busd,
            'AED': aed, 'Black_AED': baed,
            'EUR': eur, 'Black_EUR': beur,
            'SAR': sar, 'Black_SAR': bsar,
            'EGP': egp, 'Black_EGP': begp,
            'QAR': qar, 'Black_QAR': bqar,
        }
    }

