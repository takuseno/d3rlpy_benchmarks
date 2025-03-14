import csv
import glob
import os

import numpy as np

EXPERT_SCORE = 1.0
BASE_SCORE = 0.0

ALGOS = ["IQL", "AWAC"]
DATASETS = ["antmaze-umaze-v0", "antmaze-medium-play-v0", "antmaze-large-play-v0"]


def get_finetuning_score(algo, dataset):
    scores = []
    for path in glob.glob(f"finetuning/{algo}_finetuning_{dataset}_*/evaluation.csv"):
        with open(path, "r") as f:
            data = np.loadtxt(path, delimiter=",")
            scores.append(data[-1, -1])
    return scores


def get_pretraining_score(algo, dataset):
    scores = []
    for path in glob.glob(f"finetuning/{algo}_pretraining_{dataset}_*/environment.csv"):
        with open(path, "r") as f:
            data = np.loadtxt(path, delimiter=",")
            scores.append(data[-1, -1])
    return scores


def format_float(score):
    return "{:.1f}".format(score)


def main():
    table = {}
    for algo in ALGOS:
        table[algo] = {}
        for dataset in DATASETS:
            table[algo][dataset] = (get_pretraining_score(algo, dataset), get_finetuning_score(algo, dataset))

    with open("finetuning_table.csv", "w") as f:
        writer = csv.writer(f)

        header = [
            "algo",
            "dataset",
            "pretraining score",
            "pretraining std",
            "finetuning score",
            "finetuning std",
        ]
        writer.writerow(header)

        for algo in table.keys():
            for dataset in table[algo].keys():
                pretraining_scores, finetuning_scores = table[algo][dataset]
                pretraining_score = np.mean(pretraining_scores)
                pretraining_std = np.std(pretraining_scores)
                finetuning_score = np.mean(finetuning_scores)
                finetuning_std = np.std(finetuning_scores)
                row = [
                    algo,
                    dataset,
                    format_float(pretraining_score * 100.0),
                    format_float(pretraining_std * 100.0),
                    format_float(finetuning_score * 100.0),
                    format_float(finetuning_std * 100.0),
                ]
                print(row)
                writer.writerow(row)


if __name__ == "__main__":
    main()
