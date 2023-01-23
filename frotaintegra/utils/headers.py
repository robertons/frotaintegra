# Default Headers
_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'Cache-Control': 'no-cache',
    'X-Requested-With':'XMLHttpRequest'
}

def SetHeaders(Browser):
    Browser.headers = _headers
