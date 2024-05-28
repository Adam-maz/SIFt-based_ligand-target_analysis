import re
import os
import textwrap
import pandas as pd
from sift_parser import main


class SiftBasedVirtualScreeningTool:
    def __init__(self):
        self.list_for_fps = []
        self.df = pd.DataFrame()

    def dict_reader(self):
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

    def aa_number(self):
        """Processes the SIFt data and formats it with aminoacid positions."""
        tagged_aminoacids = []
        results = []

        for i, row in self.df.iterrows():
            result = f"SIFt {i + 1} -------------------------\n"
            chunks = textwrap.wrap(row["SIFt"], 9)
            tagged_chunks = [
                f"{chunk}_{idx + 1}aa" for idx, chunk in enumerate(chunks)
            ]

            tagged_aminoacids.append(tagged_chunks)
            result += "\n".join(
                f"\t{idx + 1} : {chunk}"
                for idx, chunk in enumerate(tagged_chunks)
                if "1" in chunk[:9]
            )
            results.append(result + "\n")

        return results

    def save_aa_results_to_file(self, results, filename):
        """Saves the formatted SIFt data to a file."""
        with open(filename, "w") as file:
            file.writelines(results)

    def interactive_aa(self):
        """Reads results from file and prints sorted amino acid interactions."""
        interactive_aa_pattern = re.compile(r"_(\d+)aa")
        list_for_interactive_aa = []

        with open("Results_SIFt.txt", "r") as file:
            content = file.read()
            output = re.findall(interactive_aa_pattern, content)
            list_for_interactive_aa = [int(element) for element in output]

        sorted_list_for_interactive_aa = sorted(list_for_interactive_aa)
        aa_set = set(sorted_list_for_interactive_aa)

        print(
            "Numbers of all aminoacids forming interactions based on SIFt analysis: "
        )
        print(sorted(aa_set))
        print(f"Aminoacids amount: {len(aa_set)}")


if __name__ == "__main__":
    tool = SiftBasedVirtualScreeningTool()
    tool.dict_reader()
    results = tool.aa_number()
    tool.save_aa_results_to_file(results, "Results_Bit_SIFt.txt")
    print("----------")
    print(
        "The amino acids with the corresponding bits were saved as Results_Bit_SIFt.txt"
    )
    tool.interactive_aa()
