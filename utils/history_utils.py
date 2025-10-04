import csv
import os

def save_chat_history(question, answer, filename="chat_history.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Question", "Answer"])
        writer.writerow([question, answer])
    return filename
