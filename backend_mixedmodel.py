
# -------------- Data input ---------- #
# Input files:  
# data: csv, tsv, xlsx 
# input type of test
# input type of data (e.g. gene expression, methylation, etc.)
# input type of plots
import os 

data = input('Write the data-file name' + '\nThe format msut be included (ex. data.csv, data.tsv, data.xlsx)  ')


try:
	with open(data) as file:
	    print(file.read())
except FileNotFoundError:
	print('That file was not found')


# ------ Test function call ---------- #

# Inser mixed model code here


#def hello(name): ##specifichi dentro un argomento da richiamare
#	print(”Hello!”+name)
#	print(”Have a nice day!”)
#hello(”Bona”) ##stiamo inviando alla funzione hello() la stringa Bona



# ------- Plot function call ---------- #




# -------- Utils ---------------------- #

