import csv
import os

download_folder = r"C:\Users\Hendi\Downloads"

leaderboard_file = os.path.join(download_folder, "OSKM ITB DATA FULL.csv")
finder_file = os.path.join(download_folder, "finder_mahasiswa.csv")
output_file = os.path.join(download_folder, "final_data.csv")

# baca leaderboard
leaderboard = {}
with open(leaderboard_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nim = row["nim"].strip()
        leaderboard[nim] = row

# gabungkan dengan finder
with open(finder_file, "r", encoding="utf-8") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:
    
    finder_reader = csv.DictReader(f_in)
    fieldnames = finder_reader.fieldnames + ["rank", "points"]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in finder_reader:
        nim = row["nim"].strip()
        if nim in leaderboard:
            row["rank"] = leaderboard[nim]["rank"]
            row["points"] = leaderboard[nim]["points"]
        else:
            row["rank"] = ""
            row["points"] = ""
        writer.writerow(row)

print(f"✅ Data berhasil digabung ke: {output_file}")
