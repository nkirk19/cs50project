# THIS PROGRAM WAS RUN ON A LOCAL MACHINE.
# THE IDE WOULD KILL THE PROGRAM WHEN WE TRIED TO RUN IT
# DUE TO MEMORY ISSUES. THE OUTPUT FILES ARE LOCATED IN THE DATA
# FOLDER.

# INTRO
# Team members:
#  - Haruka Margaret Braun
#  - Nikolas Kirk
#  - Helen He

# This program downloads 5 files from the internet, creates choropleth maps from
# them,  joins them together, outputs all of the joined together datasets into
# a single file, and then creates correlations between the variables within the files.
# It compares US County level Unemployment, Poverty, Education level (bachelors
# or higher) data from 2017, as well as voting results from the 2016 Presedential
# Election to compare the correlation strength between the variables.
# The County level data is stored by their FIPS ("Federal Information
# Processing Standard") codes to enable the joining together of the datasets.

# Five datasets used:
#  1. FIPS: https://github.com/kjhealy/fips-codes/blob/master/county_fips_master.csv
#  2. 2016 Presidential results: https://raw.githubusercontent.com/tonmcg/US_County_Level_Election_Results_08-16/master/2016_US_County_Level_Presidential_Results.csv
#  3. Unemploymnt:  https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls (from https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
#  4. Poverty:  https://www.ers.usda.gov/webdocs/DataFiles/48747/PovertyEstimates.xls (from https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
#  5. Education:  https://www.ers.usda.gov/webdocs/DataFiles/48747/Education.xls (from https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)



#IMPORT LIBRARIES
import requests, pandas, numpy
#Set abbreviations for the following libraries
import plotly.figure_factory as ff
from plotly.offline import plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns



#PLACE FILES IN LOCATIONS
directory = '/users/nikolaskirk/project/code/data'
htmldirectory = '/users/nikolaskirk/project/code/website/templates'
pngdirectory = '/users/nikolaskirk/project/code/website/static'

FIPStxt = directory + '/' + 'FIPS.txt' #FIPS stands for Federal Information Processing Standards (a code for each US County)
ElectionFile = directory + '/' + '2016_US_County_Level_Presidential_Results.csv'
EmploymentFile = directory + '/' + 'Unemployment.xls'
PovertyFile = directory + '/' + 'PovertyEstimates.xls'
EducationFile = directory + '/' + 'Education.xls'
FIPSOut = directory + '/' + 'FullFIPS.csv'
CorrelationOut = pngdirectory + '/' + 'Correlation_PairedVals.png'
MapOut = pngdirectory + '/' + 'Correlation_Heatmap.png'




#READ FILES
#Read in FIPS codes to use as master list later when joining files together
myFIPSfile = requests.get('https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv')
open(FIPStxt, 'wb').write(myFIPSfile.content)
FIPSAll = pandas.read_csv(FIPStxt, header=None, usecols=[0,1,2], names=['FIPSCd', 'CountyName', 'StateCd'], encoding='latin-1')
FIPSAll['StateCd'] = FIPSAll['StateCd'].str.strip() #Strip of spaces around the State code due to how the file is formatted
FIPSCodeOnly = FIPSAll[['FIPSCd']] #Doing this bc will use this to limit other files to only valid FIPS codes via pandas merge with an inner join later on


#Read in the 2016 Presidential results
ogElectionResults = requests.get('https://raw.githubusercontent.com/tonmcg/US_County_Level_Election_Results_08-16/master/2016_US_County_Level_Presidential_Results.csv')
open(ElectionFile, 'wb').write(ogElectionResults.content) #Write file locally
ElectionResults = pandas.read_csv(ElectionFile, skiprows=1, header=None, usecols=[4,5,10], names=['PercentDem', 'PercentRep', 'FIPSCd'])
ElectionResults = ElectionResults[['FIPSCd', 'PercentDem', 'PercentRep']]
ElectionResults[['FIPSCd']] = ElectionResults[['FIPSCd']].astype(object)
ElectionResults = pandas.merge(FIPSCodeOnly, ElectionResults, on='FIPSCd', how='right') #inner join merge to limit to only valide FIPS code records

#Function to read, save, and return pandas dataframe with only the desired columns used by the Unemployment, Poverty, and Eduction Excel files
def process(url, file, name, skiprows, ogFIPSCol, ogDataCol, newFIPSCol, newDataCol):
    DataFile = requests.get(url)  #Get the file and put in variable
    open(file, 'wb').write(DataFile.content) #Write file locally
    excel = pandas.ExcelFile(file)  #Read into Excel file
    All = excel.parse(name, skiprows=skiprows, index_col=None) #Parse it into a dataframe
    Selected = All[[ogFIPSCol,ogDataCol]] #subset to the columns desired
    Selected.columns = [newFIPSCol, newDataCol]  #Rename the remaining columns
    Selected[[newFIPSCol]] = Selected[[newFIPSCol]].astype(object)
    Selected = pandas.merge(FIPSCodeOnly, Selected, on='FIPSCd', how='right') #inner join merge to limit to only valide FIPS code records
    return(Selected) #Return Pandas dataframe

#Call the function to process the Unemployment file
unemployment = process('https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls', EmploymentFile, 'Unemployment Med HH Inc', 7, 'FIPS', 'Unemployment_rate_2017', 'FIPSCd', 'UnemploymentPct')
#Call the function to process the Poverty file
poverty = process('https://www.ers.usda.gov/webdocs/DataFiles/48747/PovertyEstimates.xls', PovertyFile, 'Poverty Data 2017', 3, 'FIPStxt', 'PCTPOVALL_2017', 'FIPSCd', 'PovertyPct')
#Call the function to process the Education file
education = process('https://www.ers.usda.gov/webdocs/DataFiles/48747/Education.xls', EducationFile, 'Education 1970 to 2017', 4, 'FIPS Code', "Percent of adults with a bachelor's degree or higher, 2013-17", 'FIPSCd', 'EducBachlOrHigherPct')



# MAKE CHOROPLETH MAPS
# Function to create Choropleth file;
def CreateChoropleth(dataframe, percent, GraphTitle, LegendTitle, filename, filedirectory):
    ccolorscale = ["#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"]
    ColumnList = dataframe[percent].tolist() #Convert Pandas dataframe column to a list
    CleanList = sorted(i for i in ColumnList if i >= 0) #Get rid of any nan values
    TopPercent = numpy.nanpercentile(CleanList,95) #Get the 95th percentile element of the list to use
    ColorscaleRanges = list(numpy.linspace(1, TopPercent, len(ccolorscale) - 1)) #Get list for color groupings
    FIPSList = dataframe['FIPSCd'].tolist() #Put FIPs codes into a list fron Pandas dataframe column
    ColumnList = dataframe[percent].tolist()  #Put FIPs values into a list fron Pandas dataframe column
    choropleth = ff.create_choropleth( #Create the choropleth map
        fips = FIPSList, values = ColumnList,  #FIPS codes and their values
        binning_endpoints = ColorscaleRanges,  #Bin end / dividing points
        colorscale = ccolorscale, #HTML RGB colors from above
        show_state_data = True,  #Show lines around the states
        title = GraphTitle,  #Title on top of graph
        legend_title = LegendTitle)  #Legend title
    choropleth.layout.template = None #Not using layout template
    ChoroplethSave = filedirectory + '/' + filename #Create directory and filename combined
    plot(choropleth, validate=False, filename = ChoroplethSave, auto_open=False) #Create and save off the html file

#Create Choropleth files for the Unemployment, Poverty, and Education Excel files which were downloaded from the interweb (3 total from this section)
CreateChoropleth(unemployment, 'UnemploymentPct', 'Unemployment % by County', '% Unemployed', 'UnemplPctByCounty.html', htmldirectory)
CreateChoropleth(poverty, 'PovertyPct', '% in Poverty by County', '% Poverty', 'PovertyPctByCounty.html', htmldirectory)
CreateChoropleth(education, 'EducBachlOrHigherPct', 'Education Bachelor or Higher % by County', '% Bach or Higher', 'BachelorPctByCounty.html', htmldirectory)

#Create Choropleth file for 2016 Presidential Election results (1)
ElectionResults100 = ElectionResults #Creating copy of series bc will manipulate columns
ElectionResults100['PercentDem'] *= 100 # multiply column by 100
ElectionResults100['PercentRep'] *= 100 # multiply column by 100
ElectionResults100.PercentDem = ElectionResults100.PercentDem.round(decimals=1) # round to 1 decimal
ElectionResults100.PercentRep = ElectionResults100.PercentRep.round(decimals=1) # round to 1 decimal

CreateChoropleth(ElectionResults100, 'PercentRep', '2016 Pres Republican Voting % by County', '% GOP by County', 'PresElectRepPctByCounty.html', htmldirectory)
CreateChoropleth(ElectionResults100, 'PercentDem', '2016 Pres Democrat Voting % by County', '% Dem by County', 'PresElectDemPctByCounty.html', htmldirectory)



# JOIN + OUTPUT FILES
FullFIPS = pandas.merge(FIPSAll, unemployment[['FIPSCd', 'UnemploymentPct']], on='FIPSCd', how='right') #FIPS file and Unemployment file data
FullFIPS = pandas.merge(FullFIPS, poverty[['FIPSCd', 'PovertyPct']], on='FIPSCd', how='right') #Join in Poverty file data
FullFIPS = pandas.merge(FullFIPS, education[['FIPSCd', 'EducBachlOrHigherPct']], on='FIPSCd', how='right') #Join in Education file data
FullFIPS = pandas.merge(FullFIPS, ElectionResults[['FIPSCd', 'PercentDem', 'PercentRep']], on='FIPSCd', how='right') #Join in Election results file data

FullFIPS['UnemploymentPct'] *= 0.01 #Make a proper percentage
FullFIPS['PovertyPct'] *= 0.01 #Make a proper percentage
FullFIPS['EducBachlOrHigherPct'] *= 0.01 #Make a proper percentage
FullFIPS.to_csv(FIPSOut, sep=',', encoding='utf-8', index = None, header=True) #Write out to a file



# MAKE PAIRED VALUE CORRELATIONS + HEATMAP
# Remove columns so we only have the ones we need for heatmap
del FullFIPS['FIPSCd']
del FullFIPS['CountyName']
del FullFIPS['StateCd']

# get rid of non-numeric entries
ActualFIPS = FullFIPS.dropna()

#create correlation between variables
correlation = ActualFIPS.corr()

#graph pairs of data + save to file ("Correlation_PairedVals.png")
sns_plot = sns.pairplot(ActualFIPS,  height=2.5, dropna=True)
sns_plot.savefig(CorrelationOut)

# format + make heatmap figure ("Correlation_Heatmap.png")
fig, ax = plt.subplots(figsize =(14, 9)) # define size
xticks = correlation.columns # define horizontal axis label text
sns.heatmap(correlation, ax = ax, cmap ="Blues", linewidths = 0.1, annot=True, cbar_kws={'label': 'Correlation Scale', 'orientation': 'horizontal'}, fmt=".0%")

ax.set_title('Correlation Heatmap') #Give a title
bottom, top = ax.get_ylim() # don't cut off bottom and top of chart
ax.set_ylim(bottom + 0.5, top - 0.5) # don't cut off bottom and top of chart
plt.xticks(rotation=0) #rotate horizontal axis label text
plt.savefig(MapOut) #Save to a file