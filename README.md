# Dependencies
Make sure you have [Python 3.11](https://www.python.org/downloads/release/python-3116/) installed.

# Setup
1. Clone the repo
2. `cd` to the root directory of the repo
3. `python3 -m pip install -r requirements.txt` to install all dependencies
4. `python3 main.py` to run the main program
   
Replace `python3` with  `python` or `python3.11` if necessary.

# Example usage
```console
justinkeung@justinkeung:~/slurm-generator$ python3 main.py
Which question set do you want the SLURM tossups from? 2021 ACF Winter
2021 ACF Winter has 16 packets. Which packet number do you want? 1
How many times do you want the tossups to be translated? 100
Give your SLURM packet a name: winter2021
Specify the output directory (defaults to ./output):
Generating SLURM packet...
SLURM packet generation complete. Time taken: 422.89102387428284.
```
