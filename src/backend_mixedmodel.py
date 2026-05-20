
# -------------- Data input ---------- #
# Input files:  
# data: csv, tsv, xlsx 
# input type of test
# input type of data (e.g. gene expression, methylation, etc.)
# input type of plots
import os 
import pandas as pd

data = input(
    'Write the data-file name\n'
    'The format must be included (ex. data.csv, data.tsv, data.xlsx): '
)


try:
    if data.endswith('.csv'):
        df = pd.read_csv(data)
    elif data.endswith('.tsv'):
        df = pd.read_csv(data, sep='\t')
    elif data.endswith('.xlsx'):
        df = pd.read_excel(data)
    else:
        print("Unsupported file format. Please provide a .csv, .tsv, or .xlsx file.")
        df = None
    if df is not None:
        print("The data file looks like this:")
        print(df.head())

except FileNotFoundError:
    print("That file was not found")


test_type = input(
    'What type of test do you want to perform?\n'
    'mixed model: 1\n'
    'other test: 2\n'
)

# Search for the metadata/factors 
# The idea is to check for strings and numbers to identify metadata


# Variable1

# Variable2

# Variable3

print("The variables identified are: ", variable1, variable2, variable3)





# ------ Test function call ---------- #

# Inser mixed model code here


#def hello(name): ##specifichi dentro un argomento da richiamare
#	print(”Hello!”+name)
#	print(”Have a nice day!”)
#hello(”Bona”) ##stiamo inviando alla funzione hello() la stringa Bona



# ------- Plot function call ---------- #




# -------- Utils ---------------------- #

