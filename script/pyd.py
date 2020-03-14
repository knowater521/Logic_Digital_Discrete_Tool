from core.qm.qm import QM
import argparse
import sys
from colorclass import Windows

#TODO
#add validation for variables from CLI and GUI

#enable colours on terminal for windows 
if sys.platform == "win32":
    Windows.enable(auto_colors=True)

#used to check if a string can be an integer 
def representsInt(s):
    #checks if the string s represents an integer
    try: 
        int(s)
        return True
    except ValueError:
        return False

####### read and parse arguments from the command line ######################
parser = argparse.ArgumentParser(description='Quine McCluskey Circuit Minimizer')
parser.add_argument('minterms', metavar='m', type=str, nargs='+',
help='comma seperated list of minterms to be reduced')
parser.add_argument("-d", "--dont_cares", default="", help="comma seperated list of don't cares")
parser.add_argument("-v", "--variables", default="", help="comma seperated list of variables")
parser.add_argument("-s", "--show_steps", default="yes", help="show steps leading to solution")

args = parser.parse_args()

minterms  = args.minterms[0].split(',')

#make sure all the values in the values entered for minterms are valid integers
for mt in minterms:
    #if it is not a whitespace and it is not an integer 
    if (mt and not representsInt(mt)) or ((mt and representsInt(mt)) and int(mt) < 0):
        sys.exit('Error: Integer values expected for minterms')

#make sure all the values in the values entered for dont cares are valid integers
if args.dont_cares:
    dcares = args.dont_cares.split(',')
    #make sure the don't cares are all integer values
    for dc in dcares:
        if (dc and not representsInt(dc)) or ((dc and representsInt(dc)) and int(dc) < 0):
            sys.exit('Error : Integer values expected for don\'t cares')
        
        #a term cannot be a don't care and a minterm at the same time
        if dc in minterms:
            sys.exit('Error: A term cannot be a minterm and a don\'t care at the same time')

else:
    dcares = []

##################################add validation for variables here ####################
if args.variables:
    variables = args.variables.split(',')

    #filter out duplicates in the variables entered


    #if there were duplicate terms then let the user know
    if len(variables) != len(list(set(variables))):
        sys.exit("Error: Duplicate terms not allowed for variables")
    #make sure the variables entered are enough to represent the expression 
    #else raise a value error exception and close the program

    #check the number of variables needed
    #take into consideration the minterms as well

    mterms = map(lambda x : int(x),minterms)
    dcs = map(lambda x : int(x),dcares)
    max_minterm = max(list(mterms) + list(dcs))

    max_minterm = bin(max_minterm)[2:]

    if len(variables) != len(max_minterm):
        sys.exit("Error: Number of variables entered is not enough to represent expression")
else: 
    variables = []

#make sure show steps is either a yes or a no 
if args.show_steps.lower() != 'yes' and args.show_steps.lower() != 'no':
    sys.exit('show_steps expects yes or no')
    
#simply expression and print solution if necessary
qm = QM(minterms,dcares,variables)
# pis = qm.pis()
# epis = qm.primary_epis()
# sepis =  qm.secondary_epis()

sols = qm.minimize()
#f=open("script/anspy.txt",'w',encoding='utf-8')
#if args.show_steps == 'yes':
    #print(qm.procedure)
    #f.write(str(qm.procedure))
#else:
    #print('Solution')
    #print(sols[0])
    #f.write(sols[0])
    #if len(sols)>1:
        #for i in range(1,len(sols)):
            #print(sols[i])
            #f.write(sols[i])