'''Qr kod ti jaratiwsh ham mag'luwmatlardi saqlaw'''
import qrcode
import pandas as pd
import os
import random
import string

QR_DIR = "qr_codes"
TEACHERS_FILE = "teachers.xlsx"

def generate_unique_id(existing_ids):
    """Jana unikal ID jaratildi: TEAxxxx"""
    while True:
        new_id = "TEA" + ''.join(random.choices(string.digits, k=4))
        if new_id not in existing_ids:
            return new_id

def create_qr_code(teacher_id):
    """Berilgen ID tiykarinda QR code jaratiw"""
    qr = qrcode.make(teacher_id)
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)
    qr_path = os.path.join(QR_DIR, f"{teacher_id}.png")
    qr.save(qr_path)
    print(f"✅ QR kod saqlandi: {qr_path}")

def main():
    print("📌 QR kod jaratiwshi (tek at, familiya, pan kiritin)")
    at = input("At: ").strip()
    familiya = input("Familiya: ").strip()
    pan = input("Pan: ").strip()

    # Mag'lumatlar bazasi menen islew
    if os.path.exists(TEACHERS_FILE):
        df = pd.read_excel(TEACHERS_FILE)
        existing_ids = set(df["ID"].values)
    else:
        df = pd.DataFrame(columns=["ID", "At", "Familiya", "Pan"])
        existing_ids = set()

    teacher_id = generate_unique_id(existing_ids)

    user = {
        "ID": teacher_id,
        "At": at,
        "Familiya": familiya,
        "Pan": pan
    }

    df = pd.concat([df, pd.DataFrame([user])], ignore_index=True)
    df.to_excel(TEACHERS_FILE, index=False)
    print(f"✅ Mag'lumatlar saqlandi. ID: {teacher_id}")

    create_qr_code(teacher_id)

if __name__ == "__main__":
    main()
