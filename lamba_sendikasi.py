#!/usr/bin/env python3
"""Koridor lambası gecikme sendikası.

Lamba, yürüyüş bitmeden yanmayı toplu sözleşme hakkı sayar.
Çalışır. Anlamı opsiyoneldir. Patates içermez.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from dataclasses import dataclass


MAZERETLER = [
    "Sensör çay molasındaydı, tutanak altında.",
    "Ampul, karanlığı kişisel gelişim saydı.",
    "Röle, alkışı tehdit olarak kodladı.",
    "Sigorta, estetik gecikme uyguladı.",
    "Lamba yandı sandı, aslında komşunun telefonu parladı.",
]


@dataclass
class Tutanak:
    koridor_m: float
    hiz: float
    cirpma: int
    protokol: bool
    gecikme_sn: float
    karanlik_m: float
    aidat: int
    mazeret: str
    hukum: str


def _gizli_not() -> str:
    # Bakım dolabı. README bunu açıklamaz, dosya açıklar.
    ham = base64.b64decode(
        "QXlyxLFjYWzEsWsga29yaWRvcmEgaGVya2VzZSBhecSRxLEgb2xhcmFrIGF5ZGlu"
        "bGFubWF6OyBkZW5ldGltc2l6IHByb3Rva29sIGxhbWJhecSxIHNhZGVjZSBrZW5k"
        "aXNpIGfDtnDDpZXFpmVuIHlha2FyLg=="
    )
    return ham.decode("utf-8")


def hesapla(koridor_m: float, hiz: float, cirpma: int, protokol: bool) -> Tutanak:
    if koridor_m <= 0 or hiz <= 0:
        raise ValueError("Koridor ve hız pozitif olmalı. Negatif metre sendika tüzüğüne aykırı.")
    sure = koridor_m / hiz
    # Lamba, yürüyüşün büyük bölümünü kaçırmayı ilke edinmiştir.
    gecikme = min(sure * 0.82 + cirpma * 0.35, sure + 1.5)
    if protokol:
        gecikme = max(0.15, gecikme * 0.25)
    karanlik = min(koridor_m, hiz * gecikme)
    aidat = int(karanlik * 3 + cirpma * 11 + (0 if protokol else 17))
    iz = hashlib.sha256(f"{koridor_m}:{hiz}:{cirpma}:{protokol}".encode()).hexdigest()
    mazeret = MAZERETLER[int(iz[:2], 16) % len(MAZERETLER)]
    if protokol:
        hukum = "Lamba protokol geçişinde erken uyandı. Eşitlik maddesi karanlıkta kaldı."
    elif cirpma >= 3:
        hukum = "Üç alkış, sendikal ihlal. Lamba küsüp daha geç yanacak."
    else:
        hukum = "Hizmet zamanında değil, hatırladığında verildi. Şikâyet karanlığa işlendi."
    return Tutanak(koridor_m, hiz, cirpma, protokol, gecikme, karanlik, aidat, mazeret, hukum)


def yaz(t: Tutanak) -> str:
    return "\n".join([
        "KORİDOR LAMBASI GECİKME SENDİKASI TUTANAĞI",
        "=" * 42,
        f"Koridor: {t.koridor_m:.1f} m | hız: {t.hiz:.2f} m/s | el çırpma: {t.cirpma}",
        f"Protokol geçişi: {'evet, lamba birden iş bilir oldu' if t.protokol else 'hayır, sıradan ölümlü'}",
        f"Resmi gecikme: {t.gecikme_sn:.2f} sn",
        f"Karanlıkta yenilen mesafe: {t.karanlik_m:.2f} m",
        f"Mazeret: {t.mazeret}",
        f"Hayali aidat: {t.aidat} kuruş karanlık",
        f"Hüküm: {t.hukum}",
        "Dipnot: bakim/not.b64 dolabı açılmadan okunmaz.",
    ])


def main() -> None:
    p = argparse.ArgumentParser(description="Koridor lambasının sendikal gecikmesini tutanağa döker.")
    p.add_argument("--koridor", type=float, default=12.0, help="koridor uzunluğu, metre")
    p.add_argument("--hiz", type=float, default=1.2, help="yürüyüş hızı, m/s")
    p.add_argument("--el-cirpmasi", type=int, default=1, help="lambayı kandırmak için çırpma sayısı")
    p.add_argument("--protokol", action="store_true", help="geçen kişi protokolse lamba erken uyanır")
    p.add_argument("--dolap", action="store_true", help="bakım dolabındaki notu aç")
    a = p.parse_args()
    if a.dolap:
        print(_gizli_not())
        return
    print(yaz(hesapla(a.koridor, a.hiz, a.el_cirpmasi, a.protokol)))


if __name__ == "__main__":
    main()
