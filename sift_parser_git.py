import re
import os
import pandas as pd


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
    reference_sift_map = {
        1: (
            "000...000",
            "Description 1",
        ),
        2: (
            "000...000",
            "Description 2",
        ),
        3: (
            "000...000",
            "Description 3",
        ),
        4: (
            "000...000",
            "Description 4",
        ),
    }

    obj1 = SiftBasedVirtualScreeningTool()
    obj1.file_reader()

    try:
        reference_sift_key = int(
            input(
                """Select '1' to set as a reference Description 1,
                Select '2' to set as a reference Description 2, 
                Select '3' to set as a reference Description 3,  
                Select '4' to set as a reference Description 4: """
            )
        )
        reference_sift, description = reference_sift_map[reference_sift_key]
        print(f"Selected as reference {description}")
        print("Outputs (threshold >=0.7): ")
    except (ValueError, KeyError):
        print("An unsupported value was provided, rerun script")
        return

    tanimoto_coefficients = obj1.calculate_tanimoto_coefficients(reference_sift)
    dict_for_output = {
        idx: coeff
        for idx, coeff in enumerate(tanimoto_coefficients, start=1)
        if coeff >= 0.7
    }

    for idx, coeff in dict_for_output.items():
        print(f"\tTanimoto coefficient for vector {idx}: {coeff}")


main()
