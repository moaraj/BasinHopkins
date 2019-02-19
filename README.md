# Basin Hopping Guide

| ![](https://github.com/moaraj/BasinHopkins/blob/master/docs/image21.gif) | ![](https://github.com/moaraj/BasinHopkins/blob/master/docs/Opt.png) | ![](https://github.com/moaraj/BasinHopkins/blob/master/docs/image20.gif) |
|----------------------------------------------------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------------|

1. Installation
2.  Input file
3. What is needed for a job
4. Analysis
5. The restart function
6. Submitting a job

# Installation
Installing Basin hopping on your sharcnet account is very simple.
1.	Log into sharcnet and move the latest copy of Basing hoping into your scratch directory. 
 
2.	In putty go to your scratch directory (cd /scatch/#username)
3.	You can type the command ls to view all the files in your scratch. When ready type the following command: python bh_2.1.py (or whatever version you have). The program will ask for your sharcnet username, enter it and hit enter.  After this type ls to make sure all the files are installed there should be 10 new files.
 
Basin hopping is now installed on your sharcnet account and ready to run. 

# The input file

The file named Bh_ipf.txt is a template input file. Here is what needs to be filled out

1. int_file: is the initial gjf it must end in _1.gjf
2. sav_file: is the name of a check point file used in restarting basin hopping
3. save as: is the place where data will be saved, two files will be produced data.txt and data_unique.txt. data will contain all the data from the basing hopping run while the unique file will contain all the data from the files deemed unique from the analysis section.
4. Steps = is the number of Basin hoping steps
5. job wall time = this a feature that should be kept off unless absolutely needed. It makes each job run for the specified number of seconds, only use if Gaussian is freezing on a gjf.
6. box size = is the containment radius of the molecule
7. nrg term = is the characters after the hf= in the log file, note that if the log file has hf=-1.11123212312\S2 then the nrg term is \\S2.
8. temp = is the temperature that the basin hopping routine will be run at.
9. nrg var = is part of the analysis this is a energy requirement, if two files are within this energy window then the higher nrg of the two will be considered a double.
10. geom var = files are unique if any of there geometries are larger than this value, therefore the smaller this value the more unique files there will be.
11. method = this is where you put the method there is 5 different methods that you can use check the template ipf for proper formatting.
12. restart: this is a handy feature if a job wall times simply change restart to yes and resubmit.
13. custom check: this is if you have a special requirement of the systems geometry. 
14. header = is the key words in the gjf 
15. connectivity: this is everything after the geometry in the gjf and must start on this line.
That is everything that is needed with in the input file.

# What do you need for each and every job?
You need three things.
1.	Your intal .gjf file ending _1.gjf
2.	A unique input file
3.	A file to be submitted. 
The file to be submitted is a .py file the template is Basin_hopping.py
This needs to be:
from engine import *
def bh():
	Basin_hop(‘/scratch/username/yourinputfile’, ‘folder to move all files’)
Bh()

# Analysis 
At the end of every job the data.txt file and data_unique.txt files are produced and these contain the energy for analysis. The .gjf and .log files will be moved to the folder specified in the .py file, and put into subdirectories Unique and Doubles. 

# The restart function
The restart function has many more uses than just restarting wall timed jobs.
If a job finishes and you want to add more steps, simply move all the .gjf and .log files back to the scratch folder and change restart: no-end to restart: yes-end and change the steps to the desired number. This will also require the .sav file to be in the scratch as well.
Another thing is that you can change the analysis varriables, put restart to yes, move all the .gjf and .log files back to the scratch adjust the variables in the input file and resubmit them. 

# Submitting a job
The command is 
sqsub -q serial --mpp=4g -r10h -o your_inputfile.txt python you_submited_file.py
Comment questions concerns? Email me moaraj.hasan@gmail.com
