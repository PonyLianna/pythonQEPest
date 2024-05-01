					xxxxxxxxxxxxxxxxxx
					xx              xx
					xxx   QEPest   xxx
					xx              xx
					xxxxxxxxxxxxxxxxxx

QEPest is a free Java program addressing the filed of agrochemicals. It allows the scoring of molecules 
as herbicides (QEH), insecticides (QEI) and fungicides (QEF) according to pesticide class-specific scoring functions. 

Although these are basic molecular descriptors, multiple approximations of logP are available. The parameterization 
of the desirability functions has been performed using descriptors generated with JChem (6.0.0, 2013, ChemAxon, 
http://www.chemaxon.com). Hence, in order to assure maximum accuracy, we recommend the usage of ChemAxon’s logP.  

Before running QEPest.jar, please make sure:
	- Java Runtime Engine 1.6 or later installed is installed on your computer
	- The file "data.txt", containing the molecules to be scored, respects the structure as described below (### Input file ###) 
	 (tab sepatated file with header, each molecule in a different row)
	- QEPest.jar and data.txt are placed in the same directory
	
### Input file 
The input for QEPest consists of a tab-separated text file containing molecules (in rows) and seven columns (in this order): 
	- molecule name (Name)
	- molecular weight (MW)
	- hydrophobicity (LogP)
	- number of hydrogen bond acceptors (HBA)
	- number of hydrogen bond donors (HBD)
	- number of rotatable bounds (RB) 
	- number of aromatic rings (arR)

Example of data.txt
Name	MW	LogP	HBA	HBD	RB	arR
mol1	240.2127	3.2392	5	1	4	1
mol2	249.091	3.0273	3	1	5	1
mol3	308.354	2.1086	1	0	7	1
mol4	360.444	4.0137	3	0	8	0
mol5	295.335	4.9335	2	0	1	1



#### Running QEPest.jar 
QEPest.jar will read the data.txt file and compute QEH, QEI and QEF. If an error occurs in a row (e.g., missing value, 
bad number of fields etc), the an error message will indicate the molecule and the computation will proceed to the next
row. An message will indicate the end of the and an output file (i.e., data.txt.out) will be written in the same directory.
 
For any question please write to 5orin.4vram@gmail.com

Have fun!!!