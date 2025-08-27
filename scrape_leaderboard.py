import requests
import csv
import os

# jumlah halaman leaderboard
TOTAL_PAGES = 253  

# folder Downloads kamu
download_folder = r"C:\Users\Hendi\Downloads"
OUTPUT_FILE = os.path.join(download_folder, "leaderboard_full.csv")

# header CSV
headers = [
    "user_id", "rank", "nama", "nim", "fakultas", "keluarga",
    "Q1_score", "Q1_total",
    "Q2_score", "Q2_total",
    "Q3_score", "Q3_total",
    "Q4_score", "Q4_total",
    "Q5_score", "Q5_total",
    "quiz_score_total",
    "itbguessr_score", "memorygame_score", "total_score", "lulus"
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()

    for page in range(1, TOTAL_PAGES + 1):
        url = f"https://api.oskm.katitb.com/api/leaderboard?page={page}&page_size=20"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = res.json().get("data", [])

        for entry in data:
            # siapkan dict kosong untuk profil scores
            profil = {f"Q{i}_score": 0 for i in range(1, 6)}
            profil.update({f"Q{i}_total": 0 for i in range(1, 6)})

            # isi dari API
            for p in entry.get("profil_score", []):
                num = p.get("profil_number")
                profil[f"Q{num}_score"] = p.get("quiz_score", 0)
                profil[f"Q{num}_total"] = p.get("profil_total_score", 0)

            # hitung jumlah quiz_score
            quiz_score_total = sum(profil[f"Q{i}_score"] for i in range(1, 6))

            writer.writerow({
                "user_id": entry.get("user_id"),
                "rank": entry.get("rank"),
                "nama": entry.get("nama"),
                "nim": entry.get("nim"),
                "fakultas": entry.get("fakultas"),
                "keluarga": entry.get("keluarga"),
                "Q1_score": profil["Q1_score"], "Q1_total": profil["Q1_total"],
                "Q2_score": profil["Q2_score"], "Q2_total": profil["Q2_total"],
                "Q3_score": profil["Q3_score"], "Q3_total": profil["Q3_total"],
                "Q4_score": profil["Q4_score"], "Q4_total": profil["Q4_total"],
                "Q5_score": profil["Q5_score"], "Q5_total": profil["Q5_total"],
                "quiz_score_total": quiz_score_total,
                "itbguessr_score": entry.get("itbguessr_score"),
                "memorygame_score": entry.get("memorygame_score"),
                "total_score": entry.get("total_score"),
                "lulus": entry.get("lulus"),
            })

        print(f"✅ Page {page}/{TOTAL_PAGES} selesai")

print(f"\n🎉 Selesai! Data lengkap sudah disimpan di:\n{OUTPUT_FILE}")
