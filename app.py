from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI

url = 'https://www.alsoug.com/en/currency'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
}

app = FastAPI()

@app.get('/')
def health():
    return {'Server is Healthy 🌐': True}

@app.get('/rates')
def root():
    try:
        page = requests.get(url, headers=headers, timeout=10)
        page.encoding = 'utf-8'
        page.raise_for_status()

        soup = BeautifulSoup(page.text, 'html.parser')

        # Site actually uses <sapn>, not <span>
        sopo = soup.find_all('sapn')

        rates = []
        for tag in sopo:
            text_value = tag.get_text(strip=True).replace(',', '')
            try:
                num = float(text_value)
                rates.append(num)
            except ValueError:
                # ignore non-numeric entries
                continue

        # DEBUG: if you want to inspect
        # print("RATES:", rates)

        # Make sure we have at least 12 numeric values
        if len(rates) < 12:
            return {
                "error": f"Expected at least 12 numeric rates, found {len(rates)}",
                "collected_rates": rates
            }

        usd,  busd  = rates[0],  rates[1]
        aed,  baed  = rates[2],  rates[3]
        eur,  beur  = rates[4],  rates[5]
        sar,  bsar  = rates[6],  rates[7]
        egp,  begp  = rates[8],  rates[9]
        qar,  bqar  = rates[10], rates[11]

    except Exception as e:
        # Return error to client
        return {"error": str(e)}

    return {
        'sdg_rates': {
            'USD': usd,
            'Black_USD': busd,
            'AED': aed,
            'Black_AED': baed,
            'EUR': eur,
            'Black_EUR': beur,
            'SAR': sar,
            'Black_SAR': bsar,
            'EGP': egp,
            'Black_EGP': begp,
            'QAR': qar,
            'Black_QAR': bqar,
        }
    }
