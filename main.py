import csv
import os
from evaluation import evaluate_by_metrics

def collect_user_estimation(song_name):
    ratings = {}
    estimation_notes = {}
    for source in ["Drums", "Bass", "Vocals", "Other"]:
        while True:
            try:
                rating = float(input(f"For the {source} separation file, please give me a score from 1 to 10:\n").strip())
                if 1 <= rating <= 10:
                    ratings[source.lower()] = rating
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        estimation_notes[source.lower()] = input(f"For the {source} separation file, you may provide free text about your hearing estimation:\n").strip()
    print("\nThank you!")
    return {"song_name": song_name, "ratings": ratings, "notes": estimation_notes}


def save_to_csv(data, filename="evaluation.csv"):
    file_exists = os.path.exists(filename)

    headers = ["Song Name", "Drums User Rating", "Drums Notes", "Bass User Rating", "Bass Notes",
               "Vocals User Rating", "Vocals Notes", "Other User Rating", "Other Notes"]

    row = [
        data["song_name"],
        data["ratings"]["drums"], data["notes"]["drums"],
        data["ratings"]["bass"], data["notes"]["bass"],
        data["ratings"]["vocals"], data["notes"]["vocals"],
        data["ratings"]["other"], data["notes"]["other"]
    ]

    if not file_exists:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)
    print(f"\nData successfully saved to {filename}!")


if __name__ == "__main__":
    try:
        song_name = input("Type song name: ").strip()
        user_feedback = collect_user_estimation(song_name)
        evaluation_scores = evaluate_by_metrics(song_name)
        save_to_csv(user_feedback | evaluation_scores)
    except Exception as e:
        print(e)
