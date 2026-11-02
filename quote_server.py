from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
import csv, io, json
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        urls = {'/quotes':'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL', '/funds':'https://www.sitca.org.tw/MemberK0000/F/03/nav.csv', '/companies':'https://openapi.twse.com.tw/v1/opendata/t187ap03_L'}
        if self.path not in urls:
            self.send_error(404); return
        try:
            req = Request(urls[self.path], headers={'User-Agent':'WealthJournal/1.0'})
            with urlopen(req, timeout=20) as response: data = response.read()
            if self.path == '/funds':
                rows = csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
                data = json.dumps([{'code':r['基金代號'].strip().upper(), 'name':r['基金名稱'], 'price':r['基金淨值'], 'date':r['日期'], 'currency':r['幣別'], 'securityCode':r['受益憑證代號'].strip().upper()} for r in rows], ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Private-Network', 'true')
            self.end_headers(); self.wfile.write(data)
        except Exception:
            self.send_error(502, 'Quote service unavailable')
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.end_headers()
HTTPServer(('127.0.0.1',18765), Handler).serve_forever()
