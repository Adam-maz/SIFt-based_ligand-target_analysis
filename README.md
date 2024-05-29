Description:
Here I am sharing a package containing scripts for SIFt analysis. These tools enable the user to compare the SIFts of docked ligands with a reference SIFt by calculating the Tanimoto coefficient. Additionally, the script analyzes all input SIFts values of docked ligands to find and characterize (by numbering) amino acids involved in interactions with the ligand in the active center of target protein.

Manual:
To run the tool, paste "python sequence_analysis_git.py" in the terminal.  The script requires a file containing SIFts of the docked ligands, ending with "fp.dat", in the same location. To save the output to some file, paste "python sequence_analysis_git.py > filename.txt" in the terminal.
It is worth mentioning that the reference_sift_map dictionary in the main() function in the sift_parser.py script can be freely edited to adjust the number of SIFts references to specific tasks.

Comment: The regex pattern contained in these scripts may not be suitable for another user, so you may need to define the regular expression pattern yourself.


