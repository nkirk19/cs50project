Our project consists of two main parts: one Python script to analyze publicly available datasets and a Flask script
to create a website to display the results. The two main scripts which will be run are entitled CCP1.py (this is the
data analysis script) and application.py (this is the Flask script).

CCP1.py downloads 5 files from the internet, creates choropleth maps from
them,  joins them together, outputs all of the joined together datasets into
a single file, and then creates correlations between the variables within the files.
It compares US County level Unemployment, Poverty, Education level (bachelors
or higher) data from 2017, as well as voting results from the 2016 Presedential
Election to compare the correlation strength between the variables.
The County level data is stored by their FIPS ("Federal Information
Processing Standard") codes to enable the joining together of the datasets.

To run CCP1.py, we used our local machine since the IDE did not support it due to
memory issues. To run the script on your own machine, you will need to change a few things
in the script itself related to saving files. In lines 43-45, you will need to change where in your
machine you will be saving the files. Most likely, you will want a project folder with a code folder in it.
In the code folder, you will want a data folder and a website folder. In the website folder, you will want two folders:
static and templates. The file CCP1.py should be in the code folder, and application.py should be in the website folder.
Additionally, you will need a blank .txt file called FIPS.txt in the data folder in order for the program to work.

In order for the CCP1.py script to work on your computer, you will need to download the following libraries:
requests, pandas, numpy, plotly, matplotlib, and seaborn. We used pip install. Then, you can switch into the
code directory and run the CCP1.py script. While running, if you notice some pop-ups regarding unrecognized FIPS codes,
that is totally okay – those values are ignored and the script will keep running.
You should see 5 files in the templates folder, two in the static folder,
and a total of 6 files in the data folder. Go into the templates folder and open each choropleth map.
At the top right of each page, there should be a button to download each map as a png.
Be sure to do this and then move those files to the output folder. The png files should be called:
edu.png, dem.png, pov.png, rep.png, unemployment.png. Now, be sure to move these files over to the IDE and place them in their
corresponding folders (the IDE directory should be set up the exact same way with files related to the Flask script).

In the IDE, switch into the website directory and execute "flask run." This will allow you to view the wesbite we created
This step is really crucial. Do not misplace any files or change their names; otherwise, the website won't work. We're sorry about
this step – we wish we could've just done everything on the IDE.