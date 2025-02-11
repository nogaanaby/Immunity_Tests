import csv
import os
from evaluation import evaluate_by_metrics

def collect_user_estimation(song_name):
    ratings = {}
    estimation_notes = {}
    for source in ["drums", "bass", "vocals", "other"]:
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


def save_to_csv(user_feedback, evaluation_scores, filename="evaluation.csv"):
    file_exists = os.path.exists(filename)

    headers = ["Song Name", "Drums User Rating","Drums Notes", "Drums SDR", "Drums SIR",
               "Bass User Rating", "Bass Notes","Bass SDR", "Bass SIR",
               "Vocals User Rating", "Vocals Notes", "Vocals SDR", "Vocals SIR",
               "Other User Rating", "Other Notes", "Other SDR", "Other SIR",
               ]

    row = []
    row.append(user_feedback["song_name"])

    channels=["drums", "bass", "vocals", "other"]

    for channel in channels:
        row.append(user_feedback["ratings"][channel])
        row.append(user_feedback["notes"][channel])
        row.append(evaluation_scores[f"{channel}_SDR"])
        row.append(evaluation_scores[f"{channel}_SIR"])


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
        save_to_csv(user_feedback, evaluation_scores)

    except Exception as e:
        print(e)
