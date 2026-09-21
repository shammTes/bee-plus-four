#!/usr/bin/env python3
"""Bee Seller Windows helper — see repo BETA_FIXES.md"""
import hashlib, hmac, json, os, secrets, time, tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
STORE = Path.home() / '.bee_seller_desktop.json'
SECRET = os.environ.get('BEE_HMAC_SECRET', 'DEV_ONLY_CHANGE_ME').encode()
def load_store():
    return json.loads(STORE.read_text()) if STORE.exists() else {'quota': 0, 'history': [], 'used_nonces': []}
def save_store(d): STORE.write_text(json.dumps(d, indent=2))
def device_id():
    raw = f"{os.environ.get('COMPUTERNAME','PC')}-{os.environ.get('USERNAME','user')}"
    return hashlib.sha256(raw.encode()).hexdigest()[:24]
def sign_payload(body):
    return f"{body}|{hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()[:16]}"
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('Bee Seller — Windows'); self.geometry('520x640'); self.configure(bg='#0A2F2F'); self.store=load_store(); self._build()
    def _build(self):
        tk.Label(self, text='Bee Seller (Windows)', fg='white', bg='#0A2F2F', font=('Segoe UI',16,'bold')).pack(pady=(16,4))
        tk.Label(self, text=f'Device ID: {device_id()}', fg='#5EEAD4', bg='#0A2F2F').pack()
        tk.Label(self, text=f"Quota: {self.store.get('quota',0)}", fg='white', bg='#0A2F2F').pack(pady=8)
        f=tk.Frame(self, bg='#0A2F2F'); f.pack(fill='both', expand=True, padx=16)
        self.redeem_entry=tk.Text(f, height=3); self.redeem_entry.pack(fill='x')
        ttk.Button(f, text='Redeem (demo +10)', command=self.redeem).pack()
        self.student_id=ttk.Entry(f); self.student_id.pack(fill='x', pady=4)
        ttk.Button(f, text='Issue student code', command=self.issue_student).pack()
        self.sub_id=ttk.Entry(f); self.sub_id.pack(fill='x', pady=4)
        self.sub_quota=ttk.Entry(f); self.sub_quota.insert(0,'5'); self.sub_quota.pack(fill='x')
        ttk.Button(f, text='Issue seller grant', command=self.issue_seller).pack(pady=4)
        self.out=tk.Text(f, height=5); self.out.pack(fill='x', pady=6)
        ttk.Button(f, text='Copy', command=lambda:(self.clipboard_clear(), self.clipboard_append(self.out.get('1.0','end').strip()))).pack()
    def redeem(self):
        self.store['quota']=int(self.store.get('quota',0))+10; save_store(self.store); messagebox.showinfo('OK','+10 quota (demo)')
    def issue_student(self):
        sid=self.student_id.get().strip()
        if not sid or int(self.store.get('quota',0))<1: return messagebox.showerror('Err','ID/quota')
        body=f"HIGHSCHOOL|{sid}|{secrets.token_hex(6)}|{int(time.time())}"
        self.store['quota']-=1; save_store(self.store); self.out.delete('1.0','end'); self.out.insert('1.0', sign_payload(body))
    def issue_seller(self):
        sid=self.sub_id.get().strip(); q=int(self.sub_quota.get() or 0)
        if not sid or q<=0 or int(self.store.get('quota',0))<q: return messagebox.showerror('Err','quota')
        body=f"SELLER:{q}|{sid}|{secrets.token_hex(6)}|{int(time.time())}"
        self.store['quota']-=q; save_store(self.store); self.out.delete('1.0','end'); self.out.insert('1.0', sign_payload(body))
if __name__=='__main__': App().mainloop()
