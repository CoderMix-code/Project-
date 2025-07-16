'''Qr kodti oqiw, aniqlaw ham mag'lumatlardi jaziw'''
import cv2
import pandas as pd
from datetime import datetime
import os

TEACHERS_FILE = "teachers.xlsx"
ATTENDANCE_FILE = "attendance.xlsx"

def read_qr_opencv():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("📷 QR kodti korsetin...")
    while True:
        _, frame = cap.read()
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            print(f"✅ QR oqildi: {data}")
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("QR skaner (ESC = shig'iw)", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def write_attendance(teacher_id):
    if not os.path.exists(TEACHERS_FILE):
        print("❌ teachers.xlsx tabilmadi.")
        return

    df_teachers = pd.read_excel(TEACHERS_FILE)
    teacher = df_teachers[df_teachers["ID"] == teacher_id]

    if teacher.empty:
        print("❌ Bunday ID tabilmadi.")
        return

    first_name = teacher.iloc[0]["At"]
    last_name = teacher.iloc[0]["Familiya"]
    subject = teacher.iloc[0]["Pan"]

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(ATTENDANCE_FILE):
        df_att = pd.read_excel(ATTENDANCE_FILE)
        if "Ketgen waqit" in df_att.columns:
            df_att["Ketgen waqit"] = df_att["Ketgen waqit"].astype(str)
    else:
        df_att = pd.DataFrame(columns=["ID", "At", "Familiya", "Pan", "Kelgen waqit", "Ketgen waqit"])

    today_entry = df_att[
        (df_att["ID"] == teacher_id) &
        (df_att["Kelgen waqit"].str.startswith(today))
    ]

    if today_entry.empty:
        new_row = {
            "ID": teacher_id,
            "At": first_name,
            "Familiya": last_name,
            "Pan": subject,
            "Kelgen waqit": timestamp,
            "Ketgen waqit": ""
        }
        df_att = pd.concat([df_att, pd.DataFrame([new_row])], ignore_index=True)
        print(f"🟢 {first_name} {last_name} jumisqa KIRDI: {timestamp}")
    else:
        index = today_entry.index[0]
        df_att.at[index, "Ketgen waqit"] = timestamp
        print(f"🔴 {first_name} {last_name} jumisdan SHIQDI: {timestamp}")

    df_att.to_excel(ATTENDANCE_FILE, index=False)

def main():
    teacher_id = read_qr_opencv()
    if teacher_id and teacher_id.startswith("TEA"):
        write_attendance(teacher_id)
    else:
        print("⚠️ QR kod qate yamasa qateshilik juz berdi.")

if __name__ == "__main__":
    main()
