#!/usr/bin/env python3
"""
Bee Seller — Windows desktop helper
===================================
Matches Flutter QrPayload (lib/core/licensing/qr_payload.dart):

  Format:  BEE1|<packageCode>|<deviceId>|<nonce>|<hmacSha256Hex>
  Package: HIGHSCHOOL | WHOLESALE:<n> | SELLER:<n>
  HMAC:    SHA-256 over UTF-8 of "BEE1|package|deviceId|nonce"
  Key:     env BEE_HMAC_KEY or default (same as Flutter defaultValue)

Install:
  pip install -r requirements.txt
Run:
  python bee_seller_desktop.py
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

try:
    import qrcode
    from PIL import ImageTk

    HAS_QR = True
except ImportError:
    HAS_QR = False

STORE = Path.home() / ".bee_seller_desktop.json"
VERSION = "BEE1"
DEFAULT_KEY = "BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE"
SIGNING_KEY = os.environ.get("BEE_HMAC_KEY") or os.environ.get(
    "BEE_HMAC_SECRET", DEFAULT_KEY
)


def load_store() -> dict[str, Any]:
    if STORE.exists():
        try:
            return json.loads(STORE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"quota": 0, "history": [], "used_nonces": []}


def save_store(data: dict[str, Any]) -> None:
    STORE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def hmac_hex(body: str) -> str:
    return hmac.new(
        SIGNING_KEY.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def build_payload(package_code: str, device_id: str, nonce: str | None = None) -> str:
    nonce = nonce or secrets.token_hex(8)
    device_id = device_id.strip()
    package_code = package_code.strip()
    body = f"{VERSION}|{package_code}|{device_id}|{nonce}"
    sig = hmac_hex(body)
    return f"{body}|{sig}"


def parse_payload(raw: str) -> dict[str, str] | None:
    parts = raw.strip().split("|")
    if len(parts) != 5 or parts[0] != VERSION:
        return None
    return {
        "version": parts[0],
        "package": parts[1],
        "device_id": parts[2],
        "nonce": parts[3],
        "signature": parts[4],
    }


def verify_payload(raw: str) -> dict[str, str] | None:
    p = parse_payload(raw)
    if not p:
        return None
    body = f"{p['version']}|{p['package']}|{p['device_id']}|{p['nonce']}"
    expected = hmac_hex(body)
    if not hmac.compare_digest(expected, p["signature"]):
        return None
    return p


class BeeSellerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bee Seller — Windows")
        self.geometry("560x780")
        self.minsize(480, 640)
        self.configure(bg="#0A2F2F")
        self.store = load_store()
        self._qr_photo: Any = None
        self._build_ui()
        self._refresh_quota()

    def _build_ui(self) -> None:
        tk.Label(
            self,
            text="Bee Seller (Windows)",
            fg="white",
            bg="#0A2F2F",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(16, 2))
        tk.Label(
            self,
            text="Same BEE1 HMAC format as Android Bee Seller",
            fg="#5EEAD4",
            bg="#0A2F2F",
            font=("Segoe UI", 10),
        ).pack()

        self.quota_label = tk.Label(
            self, text="Quota: 0", fg="white", bg="#0A2F2F", font=("Segoe UI", 12, "bold")
        )
        self.quota_label.pack(pady=8)

        card = tk.Frame(self, bg="#0F3D3D", padx=12, pady=12)
        card.pack(fill="both", expand=True, padx=16, pady=8)

        tk.Label(
            card,
            text="1) Redeem wholesale / master grant",
            fg="#FDE68A",
            bg="#0F3D3D",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            card,
            text="Paste WHOLESALE:N or SELLER:N code from Master / parent seller",
            fg="#94A3B8",
            bg="#0F3D3D",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x")
        self.redeem_entry = tk.Text(card, height=3, font=("Consolas", 10))
        self.redeem_entry.pack(fill="x", pady=4)
        ttk.Button(card, text="Redeem grant → add quota", command=self.redeem_grant).pack(
            anchor="w", pady=2
        )

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=10)

        tk.Label(
            card,
            text="2) Issue student unlock (HIGHSCHOOL)",
            fg="#FDE68A",
            bg="#0F3D3D",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            card,
            text="Paste student Device ID from the 4 app (Unlock screen)",
            fg="#94A3B8",
            bg="#0F3D3D",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x")
        self.student_id = ttk.Entry(card, font=("Consolas", 11))
        self.student_id.pack(fill="x", pady=4)
        ttk.Button(
            card, text="Issue student code + QR", command=self.issue_student
        ).pack(anchor="w", pady=2)

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=10)

        tk.Label(
            card,
            text="3) Issue seller grant (SELLER:N)",
            fg="#FDE68A",
            bg="#0F3D3D",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(card, text="Sub-seller device ID", fg="white", bg="#0F3D3D").pack(
            anchor="w"
        )
        self.sub_id = ttk.Entry(card, font=("Consolas", 11))
        self.sub_id.pack(fill="x", pady=2)
        qrow = tk.Frame(card, bg="#0F3D3D")
        qrow.pack(fill="x", pady=2)
        tk.Label(qrow, text="Quota to grant", fg="white", bg="#0F3D3D").pack(side="left")
        self.sub_quota = ttk.Entry(qrow, width=8, font=("Consolas", 11))
        self.sub_quota.insert(0, "5")
        self.sub_quota.pack(side="left", padx=8)
        ttk.Button(
            card, text="Issue seller grant + QR", command=self.issue_seller
        ).pack(anchor="w", pady=2)

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=10)

        tk.Label(
            card,
            text="Generated code (scan or copy into student / seller app)",
            fg="#FDE68A",
            bg="#0F3D3D",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x")
        self.out = tk.Text(card, height=4, font=("Consolas", 9), wrap="char")
        self.out.pack(fill="x", pady=4)
        btn_row = tk.Frame(card, bg="#0F3D3D")
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="Copy code", command=self.copy_code).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(btn_row, text="Clear", command=self.clear_out).pack(side="left")

        self.qr_label = tk.Label(card, bg="#0F3D3D")
        self.qr_label.pack(pady=8)
        if not HAS_QR:
            tk.Label(
                card,
                text="Install QR support:  pip install qrcode[pil]",
                fg="#FCA5A5",
                bg="#0F3D3D",
                font=("Segoe UI", 9),
            ).pack()

        key_src = (
            "BEE_HMAC_KEY env"
            if os.environ.get("BEE_HMAC_KEY") or os.environ.get("BEE_HMAC_SECRET")
            else "default (dev)"
        )
        tk.Label(
            self,
            text=f"Key source: {key_src}",
            fg="#64748B",
            bg="#0A2F2F",
            font=("Segoe UI", 8),
        ).pack(pady=(0, 8))

    def _refresh_quota(self) -> None:
        q = int(self.store.get("quota", 0))
        self.quota_label.config(text=f"Quota remaining: {q}")

    def _set_output(self, code: str) -> None:
        self.out.delete("1.0", "end")
        self.out.insert("1.0", code)
        self._show_qr(code)

    def _show_qr(self, data: str) -> None:
        if not HAS_QR:
            self.qr_label.config(image="", text="(QR library not installed)")
            return
        qr = qrcode.QRCode(version=None, box_size=5, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0F172A", back_color="white")
        img = img.resize((220, 220))
        self._qr_photo = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self._qr_photo, text="")

    def copy_code(self) -> None:
        text = self.out.get("1.0", "end").strip()
        if not text:
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Code copied to clipboard.")

    def clear_out(self) -> None:
        self.out.delete("1.0", "end")
        self.qr_label.config(image="", text="")
        self._qr_photo = None

    def redeem_grant(self) -> None:
        raw = self.redeem_entry.get("1.0", "end").strip()
        if not raw:
            messagebox.showerror("Error", "Paste a WHOLESALE:N or SELLER:N code.")
            return
        p = verify_payload(raw)
        if not p:
            messagebox.showerror(
                "Error",
                "Invalid or tampered code.\n"
                "Check format BEE1|... and that BEE_HMAC_KEY matches the app.",
            )
            return
        pkg = p["package"].upper()
        if pkg.startswith("WHOLESALE:"):
            quota = int(pkg.split(":", 1)[1] or 0)
        elif pkg.startswith("SELLER:"):
            quota = int(pkg.split(":", 1)[1] or 0)
        else:
            messagebox.showerror(
                "Error", "This code is not a wholesale/seller grant."
            )
            return
        if quota <= 0:
            messagebox.showerror("Error", "Quota must be positive.")
            return
        used = set(self.store.get("used_nonces") or [])
        if p["nonce"] in used:
            messagebox.showerror("Error", "This grant code was already redeemed.")
            return
        used.add(p["nonce"])
        self.store["used_nonces"] = list(used)
        self.store["quota"] = int(self.store.get("quota", 0)) + quota
        hist = list(self.store.get("history") or [])
        hist.insert(
            0,
            {
                "type": "redeem",
                "package": p["package"],
                "quota": quota,
                "ts": int(time.time()),
            },
        )
        self.store["history"] = hist[:100]
        save_store(self.store)
        self._refresh_quota()
        self.redeem_entry.delete("1.0", "end")
        messagebox.showinfo(
            "OK", f"Added +{quota} quota.\nNew total: {self.store['quota']}"
        )

    def issue_student(self) -> None:
        sid = self.student_id.get().strip()
        if not sid:
            messagebox.showerror("Error", "Enter the student Device ID.")
            return
        if int(self.store.get("quota", 0)) < 1:
            messagebox.showerror(
                "Error",
                "No quota left. Redeem a WHOLESALE/SELLER grant first, "
                "or set quota in %USERPROFILE%\\.bee_seller_desktop.json for testing.",
            )
            return
        code = build_payload("HIGHSCHOOL", sid)
        self.store["quota"] = int(self.store.get("quota", 0)) - 1
        hist = list(self.store.get("history") or [])
        hist.insert(
            0,
            {"type": "student", "device_id": sid, "ts": int(time.time())},
        )
        self.store["history"] = hist[:100]
        save_store(self.store)
        self._refresh_quota()
        self._set_output(code)

    def issue_seller(self) -> None:
        sid = self.sub_id.get().strip()
        try:
            q = int(self.sub_quota.get().strip() or "0")
        except ValueError:
            q = 0
        if not sid:
            messagebox.showerror("Error", "Enter sub-seller Device ID.")
            return
        if q <= 0:
            messagebox.showerror("Error", "Quota must be a positive number.")
            return
        if int(self.store.get("quota", 0)) < q:
            messagebox.showerror(
                "Error",
                f"Not enough quota (have {self.store.get('quota', 0)}, need {q}).",
            )
            return
        code = build_payload(f"SELLER:{q}", sid)
        self.store["quota"] = int(self.store.get("quota", 0)) - q
        hist = list(self.store.get("history") or [])
        hist.insert(
            0,
            {
                "type": "seller_grant",
                "device_id": sid,
                "quota": q,
                "ts": int(time.time()),
            },
        )
        self.store["history"] = hist[:100]
        save_store(self.store)
        self._refresh_quota()
        self._set_output(code)


def main() -> None:
    if sys.platform == "win32":
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    app = BeeSellerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
