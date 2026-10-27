"""Run: python app.py; open http://localhost:8501. Local demo only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from secrets import token_urlsafe
from http.cookies import SimpleCookie
from threading import Lock
import json
from src.agent import Agent
sessions={}; lock=Lock()
HTML='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZentroCare | Support demo</title>
<style>body{font:16px system-ui;background:#eef3f8;color:#13283b;max-width:920px;margin:40px auto;padding:20px}h1{font-size:40px}small{color:#526879}#chat{background:white;border-radius:16px;padding:24px;min-height:280px}pre{white-space:pre-wrap;font:15px system-ui;border-bottom:1px solid #eee;padding:12px}input{width:70%;padding:15px;border:1px solid #bbb;border-radius:8px}button{padding:15px;background:#086c70;color:white;border:0;border-radius:8px;cursor:pointer}.tag{color:#08787c}</style>
<h1>ZentroCare <span class="tag">/ Support AI</span></h1><p>Offline, evidence-first customer support prototype</p><p><small>Synthetic data only · Dataset reference: 20 October 2026 · English-first · No real cancellations or refunds · No voice integration</small></p><div id="chat"><pre>AI assistant: Ask about returns, refunds or an order. I verify identity before sharing order details.</pre></div><form id="form"><input id="msg" maxlength="4000" placeholder="How fast are wallet refunds?" required autocomplete="off"><button>Send</button><button type="button" id="reset">Reset</button></form>
<script>const chat=document.querySelector('#chat'); function line(t){let p=document.createElement('pre');p.textContent=t;chat.appendChild(p)}document.querySelector('#form').onsubmit=async e=>{e.preventDefault();let m=document.querySelector('#msg');let t=m.value;m.value='';line('You: '+t);try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();line('AI: '+d.answer+'\\nEvidence: '+(d.sources||[]).join(', '))}catch(e){line('Connection failed. Please retry.')}};document.querySelector('#reset').onclick=async()=>{await fetch('/reset',{method:'POST'});location.reload()};</script>'''
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass # No raw conversation/verification values logged.
    def do_GET(self):
        if self.path!='/': self.send_error(404);return
        b=HTML.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(b)
    def do_POST(self):
        if self.path not in ['/chat','/reset']: self.send_error(404);return
        if int(self.headers.get('Content-Length','0'))>16000:self.send_error(413);return
        cookie=SimpleCookie();cookie.load(self.headers.get('Cookie',''));sid=cookie['sid'].value if 'sid' in cookie else ''
        try:
            with lock:
                if sid not in sessions:
                    if len(sessions)>=100: sessions.clear()
                    sid=token_urlsafe(24);sessions[sid]=Agent()
                if self.path=='/reset':sessions[sid]=Agent();result={'answer':'Reset'}
                else:result=sessions[sid].reply(json.loads(self.rfile.read(int(self.headers.get('Content-Length',0)))).get('message',''))
            b=json.dumps(result,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Set-Cookie',f'sid={sid}; HttpOnly; SameSite=Strict; Path=/');self.end_headers();self.wfile.write(b)
        except Exception:
            self.send_error(500,'Local demo error; check setup.')
if __name__=='__main__':
    print('Local demo: http://localhost:8501 — synthetic data only')
    ThreadingHTTPServer(('127.0.0.1',8501),Handler).serve_forever()
