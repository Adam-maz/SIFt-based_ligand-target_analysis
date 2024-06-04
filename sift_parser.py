import re
import os
import pandas as pd
import numpy as np


class SiftBasedVirtualScreeningTool:
    def __init__(self):
        self.list_for_fps = []
        self.df = pd.DataFrame()

    def file_reader(self):
        """Reads .dat files and extracts SIFt data into a DataFrame."""
        for path in os.listdir():
            if path.endswith("fp.dat"):
                with open(path, "r") as file:
                    content = file.read()
                    pattern = re.compile(r"(?:.*\d{,6}:.*:)((?:[0,1]*))")
                    output = re.findall(pattern, content)
                    for nr, entries in enumerate(output, start=1):
                        self.list_for_fps.append({"No": nr, "SIFt": entries})
        self.df = pd.DataFrame(self.list_for_fps)

    def calculate_tanimoto_coefficients(self, reference_sift):
        """Calculates Tanimoto coefficients for the given reference SIFt vector."""
        reference_length = len(reference_sift)
        tanimoto_coefficients = []
        for sift_vector in self.df["SIFt"]:
            sift_vector = sift_vector.ljust(reference_length, "0")
            intersection = sum(
                x == "1" and y == "1"
                for x, y in zip(reference_sift, sift_vector)
            )
            union = sum(
                x == "1" or y == "1"
                for x, y in zip(reference_sift, sift_vector)
            )
            tanimoto = intersection / union if union != 0 else 0.0
            tanimoto_coefficients.append(tanimoto)
        return tanimoto_coefficients


def main():
    coeff_value = input(
        "Put threshold value for Tanimoto coefficients (e.g. 0.75) : "
    )
    reference_sift_map = [
        "01010101010110",
        "00000101110010",
        "11110101111010",
        "10101010000001",
        "00000000001110",
        "11100011100011",
    ]

    obj1 = SiftBasedVirtualScreeningTool()
    obj1.file_reader()
    list_of_iterators = list(range(len(reference_sift_map)))
    list_of_empty_lists = [[] for _ in list_of_iterators]

    for nr, sift in enumerate(reference_sift_map):
        list_of_empty_lists[nr] = obj1.calculate_tanimoto_coefficients(sift)
    arr = np.array(list_of_empty_lists).astype(np.float32)

    total_sum = 0
    for idx, element in enumerate(arr, 1):
        total_sum += element
    output = total_sum / len(list_of_iterators)
    output_list = list(output)

    list_for_results = []
    for idx, coeff in enumerate(output_list, 1):
        if coeff >= float(coeff_value):
            list_for_results.append(coeff_value)
            print(
                f"Averaged Tanimoto coefficient for vector nr {idx} : {coeff}"
            )
    print()
    print(f'The number of vectors that satisfy the condition : {len(list_for_results)} ')
    print(f"Amount of reference SIFts : {len(reference_sift_map)}")



main()
