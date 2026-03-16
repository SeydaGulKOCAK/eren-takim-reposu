#!/usr/bin/env python3
"""
generate_qr_codes.py — QR Marker PNG Görüntüleri Oluştur

KULLANIM:
  cd ~/gz_ws/src/my_swarm_pkg
  pip3 install qrcode[pil] pillow
  python3 scripts/generate_qr_codes.py

ÇIKTI:
  models/qr_marker_N/materials/textures/qr_marker_N.png   (N=1..6)

Bu PNG'ler Gazebo'daki qr_marker modellerinin texture'ı olarak kullanılır.
qr_perception.py kamera görüntüsünde pyzbar ile bu QR'ları okur.
"""

import json
import os
import sys

try:
    import qrcode
    from PIL import Image as PILImage
except ImportError:
    print("Eksik kütüphane! Şunu çalıştırın: pip3 install qrcode[pil] pillow")
    sys.exit(1)

# ── QR İçerikleri (qr_map.yaml ile birebir) ──────────────────────────────────
QR_CONTENTS = {
    1: {
        "qr_id": 1,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "OKBASI"},
            "manevra_pitch_roll": {"aktif": False, "pitch_deg": "0", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": True, "deger": 15},
            "bekleme_suresi_s": 3
        },
        "suruden_ayrilma": {
            "aktif": False, "ayrilacak_drone_id": None,
            "hedef_renk": None, "bekleme_suresi_s": None
        },
        "sonraki_qr": {"team_1": 2, "team_2": 2, "team_3": 2}
    },
    2: {
        "qr_id": 2,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "V"},
            "manevra_pitch_roll": {"aktif": False, "pitch_deg": "0", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": True, "deger": 20},
            "bekleme_suresi_s": 3
        },
        "suruden_ayrilma": {
            "aktif": False, "ayrilacak_drone_id": None,
            "hedef_renk": None, "bekleme_suresi_s": None
        },
        "sonraki_qr": {"team_1": 3, "team_2": 3, "team_3": 3}
    },
    3: {
        "qr_id": 3,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "CIZGI"},
            "manevra_pitch_roll": {"aktif": False, "pitch_deg": "0", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": False, "deger": 20},
            "bekleme_suresi_s": 4
        },
        "suruden_ayrilma": {
            "aktif": True, "ayrilacak_drone_id": 2,
            "hedef_renk": "RED", "bekleme_suresi_s": 10
        },
        "sonraki_qr": {"team_1": 4, "team_2": 4, "team_3": 4}
    },
    4: {
        "qr_id": 4,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "OKBASI"},
            "manevra_pitch_roll": {"aktif": False, "pitch_deg": "0", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": True, "deger": 15},
            "bekleme_suresi_s": 3
        },
        "suruden_ayrilma": {
            "aktif": False, "ayrilacak_drone_id": None,
            "hedef_renk": None, "bekleme_suresi_s": None
        },
        "sonraki_qr": {"team_1": 5, "team_2": 5, "team_3": 5}
    },
    5: {
        "qr_id": 5,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "V"},
            "manevra_pitch_roll": {"aktif": True, "pitch_deg": "10", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": False, "deger": 15},
            "bekleme_suresi_s": 3
        },
        "suruden_ayrilma": {
            "aktif": False, "ayrilacak_drone_id": None,
            "hedef_renk": None, "bekleme_suresi_s": None
        },
        "sonraki_qr": {"team_1": 6, "team_2": 6, "team_3": 6}
    },
    6: {
        "qr_id": 6,
        "gorev": {
            "formasyon": {"aktif": True, "tip": "CIZGI"},
            "manevra_pitch_roll": {"aktif": False, "pitch_deg": "0", "roll_deg": "0"},
            "irtifa_degisim": {"aktif": True, "deger": 10},
            "bekleme_suresi_s": 3
        },
        "suruden_ayrilma": {
            "aktif": False, "ayrilacak_drone_id": None,
            "hedef_renk": None, "bekleme_suresi_s": None
        },
        "sonraki_qr": {"team_1": 0, "team_2": 0, "team_3": 0}
    },
}

def generate_qr_png(qr_id: int, content: dict, out_path: str):
    """QR kod PNG'si oluştur ve kaydet."""
    json_str = json.dumps(content, ensure_ascii=False, separators=(',', ':'))

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(json_str)
    qr.make(fit=True)

    # 480x480 piksel — kamera görüntüsünde net görünecek büyüklük
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((480, 480), PILImage.NEAREST)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print(f"  QR{qr_id} -> {out_path}  ({len(json_str)} karakter)")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, '..', 'models')

    print("QR Kod PNG Olusturucu — TEKNOFEST 2026")
    print("=" * 50)

    for qr_id, content in QR_CONTENTS.items():
        out_path = os.path.join(
            models_dir,
            f'qr_marker_{qr_id}',
            'materials', 'textures',
            f'qr_marker_{qr_id}.png'
        )
        generate_qr_png(qr_id, content, out_path)

    print("=" * 50)
    print("Tüm QR kodlar oluşturuldu!")
    print("\nGazebo'da görünmesi için:")
    print("  gz sim worlds/world_task1_qr_static.sdf")
    print("\nQR okuma testi:")
    print("  python3 -c \"import pyzbar.pyzbar as p; from PIL import Image; "
          "img=Image.open('models/qr_marker_1/materials/textures/qr_marker_1.png'); "
          "print(p.decode(img))\"")

if __name__ == '__main__':
    main()
