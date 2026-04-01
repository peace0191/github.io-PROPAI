from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, webbrowser
os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
class H(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/': self.path='/index.html'
        return super().do_GET()
    def log_message(self,f,*a): pass
print("PROPAI 서버 시작!")
print("메인앱:     http://localhost:8080")
print("숏츠스튜디오: http://localhost:8080/propai_shorts_studio.html")
print("파트너:     http://localhost:8080/propai_partner.html")
webbrowser.open('http://localhost:8080')
HTTPServer(('',8080),H).serve_forever()
