import csv
import os
from evaluations_for_plots import evaluate_by_metrics
import matplotlib.pyplot as plt
import numpy as np


song_name = input("Type song name: ").strip()
demucs_evaluation = evaluate_by_metrics(song_name,"originals","seperation_prior_attack")
attack_effect_evaluation = evaluate_by_metrics(song_name,"seperation_prior_attack","seperation_after_attack")
defence_effect_evaluation = evaluate_by_metrics(song_name,"originals","seperation_after_attack_and_defence")

def plot_per_song(evaluation_scores, evaluation_metric):
    """
    Plots a grouped bar chart for a single song, showing SDR or SIR per channel and comparison type,
    excluding the 'mixture' channel.

    :param evaluation_scores: dict with keys 'demucs_evaluation', 'attack_effect_evaluation', 'defence_effect_evaluation',
                              each mapping to a dict of {channel: {metric: value}}.
    :param evaluation_metric: str, either "SDR" or "SIR"
    """
    channels = ['bass', 'drums', 'vocals', 'other']  # excluding 'mixture'
    comparisons = ['demucs_evaluation', 'attack_effect_evaluation', 'defence_effect_evaluation']
    labels = ['Demucs', 'Attack Effect', 'Defence Effect']
    colors = ['skyblue', 'salmon', 'lightgreen']

    x = np.arange(len(channels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (key, label, color) in enumerate(zip(comparisons, labels, colors)):
        values = [
            next((d[ch] for d in evaluation_scores[key].get(evaluation_metric, []) if ch in d), 0)
            for ch in channels
        ]
        ax.bar(x + i * width - width, values, width, label=label, color=color)

    ax.set_ylabel(evaluation_metric)
    ax.set_title(f'{evaluation_metric} per Channel')
    ax.set_xticks(x)
    ax.set_xticklabels([ch.capitalize() for ch in channels])
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()



evaluation_scores = {
    "demucs_evaluation": demucs_evaluation,
    "attack_effect_evaluation":  attack_effect_evaluation,
    "defence_effect_evaluation": defence_effect_evaluation
}


plot_per_song(evaluation_scores, "SDR")