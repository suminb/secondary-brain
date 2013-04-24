
import requests

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.99 Safari/537.22'

class HTTPException(RuntimeError):
    """HTTPError does not take keyword arguments, so we are defining a custom exception class.

    Copied from https://github.com/suminb/translator/blob/master/app/core.py
    """
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super(HTTPException, self).__init__()


def fetch_url(url):
    headers = {
        'User-Agent': USER_AGENT
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise HTTPException(('Google Translate returned HTTP %d' % r.status_code), r.status_code)

    else:
        return r

def make_url(ticker_symbol):
    return 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=1d/csv' % ticker_symbol.lower()

def read_symbols(file_name):
    with open(file_name, 'r') as f:
        return f.read().split()

if __name__ == '__main__':

    import time
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d')

    for symbol in read_symbols('bin/ticker_symbols.txt'):
        print 'Fetching data for %s' % symbol
        r = fetch_url(make_url(symbol))

        file_name = 'tmp/%s-%s-%s.txt' % (symbol.lower(), date, '1d')
        with open(file_name, 'w') as f:
            f.write(r.text)

        time.sleep(1800/500.0)