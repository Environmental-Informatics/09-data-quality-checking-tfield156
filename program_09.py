#!/bin/env python
'''
The program loads in the file DataQualityChecking.txt and runs
four checks for data quality. There are four variables in the
dataset: Precipitation (mm), Maximum Temperature (°C), Minimum
Temperature (°C), and Wind Speed (m/s). Summary statistics are
output before and after each check to analyze the changes made,
and this data is compiled into a final table summarizing the
effect of each quality check. Additionally, plots for each variable,
before and after each relevant check are outputted as PNG images
for graphical confirmation of significant changes. Two files are output:
DataQualityCheckingChangesMade_Field.txt which is a tab delimited
text file with a table of the number of replaced values for each
check and DataQualityCheckingComplete_Field.txt which is the revised
dataset after all quality checking has been performed, outputted as
a space delimited text file.

@authors: tfield
@github: tfield156
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    # replaces -999 with NaN
    newDF = DataDF.replace(to_replace=-999, value=np.NaN)
    # determine the number of changes in each column and store them in RVDF
    ReplacedValuesDF.iloc[0] = DataDF.count() - newDF.count()
    
    plt.figure(figsize=(9,6.5))
    DataDF['Precip'].plot(style='r')
    newDF['Precip'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Precipitation (mm)')
    plt.title('Removal of Precipitation NoData Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_1.1_NoData_Precip.png')
    
    plt.figure(figsize=(9,6.5))
    DataDF['Max Temp'].plot(style='r')
    newDF['Max Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Max Temperature NoData Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_1.2_NoData_MaxTemp.png')
    
    plt.figure(figsize=(9,6.5))
    DataDF['Min Temp'].plot(style='r')
    newDF['Min Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Min Temperature NoData Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_1.3_NoData_MinTemp.png')
    
    plt.figure(figsize=(9,6.5))
    DataDF['Wind Speed'].plot(style='r')
    newDF['Wind Speed'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Removal of Wind Speed NoData Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_1.4_NoData_WindSpeed.png')
    
    # set the new dataframe values in the dataframe to be returned
    DataDF = newDF

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    # make modifications to newDF so they can be compared when finished
    oldDF = DataDF
    oldCount = DataDF.count()
    DataDF['Precip'].loc[(DataDF['Precip'] < 0) | (DataDF['Precip'] > 25)] = np.NaN
    DataDF['Max Temp'].loc[(DataDF['Max Temp'] < -25) | (DataDF['Max Temp'] > 35)] = np.NaN
    DataDF['Min Temp'].loc[(DataDF['Min Temp'] < -25) | (DataDF['Min Temp'] > 35)] = np.NaN
    DataDF['Wind Speed'].loc[(DataDF['Wind Speed'] < 0) | (DataDF['Wind Speed'] > 10)] = np.NaN
    
    plt.figure(figsize=(9,6.5))
    oldDF['Precip'].plot(style='r')
    DataDF['Precip'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Precipitation (mm)')
    plt.title('Removal of Precipitation Gross Error Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_2.1_Gross_Precip.png')
    
    plt.figure(figsize=(9,6.5))
    oldDF['Max Temp'].plot(style='r')
    DataDF['Max Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Max Temperature Gross Error Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_2.2_Gross_MaxTemp.png')
    
    plt.figure(figsize=(9,6.5))
    oldDF['Min Temp'].plot(style='r')
    DataDF['Min Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Min Temperature Gross Error Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_2.3_Gross_MinTemp.png')
    
    plt.figure(figsize=(9,6.5))
    oldDF['Wind Speed'].plot(style='r')
    DataDF['Wind Speed'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Removal of Wind Speed Gross Error Values - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_2.4_Gross_WindSpeed.png')
    
    # Determine the number of changes made for each variable
    changesMade = oldCount - DataDF.count()
    changesMade = changesMade.to_frame().transpose()
    changesMade = changesMade.rename(index={0:'2. Gross Error'})
    # append number of new changes to RVDF
    ReplacedValuesDF = ReplacedValuesDF.append(changesMade)    
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    oldDF = DataDF
    diff = DataDF['Max Temp'] - DataDF['Min Temp'] #Less than zero for values that need to be swapped
    swapped = diff[diff < 0].count() #Number of swapped rows
    DataDF['Max Temp'].loc[diff < 0] = oldDF['Min Temp'].loc[diff < 0] #Replace max with min
    DataDF['Min Temp'].loc[diff < 0] = oldDF['Max Temp'].loc[diff < 0] #Repalce min with max

    plt.figure(figsize=(9,6.5))
    oldDF['Max Temp'].plot(style='r')
    DataDF['Max Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Swapping of Max Temperature for T_min > T_max - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_3.2_Swapped_MaxTemp.png')
    
    plt.figure(figsize=(9,6.5))
    oldDF['Min Temp'].plot(style='r')
    DataDF['Min Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Swapping of Min Temperature for T_min > T_max - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_3.3_Swapped_MinTemp.png')
    
    # Determine the number of changes made for each variable
    changesMade = pd.Series([0, swapped ,swapped, 0])
    changesMade = changesMade.to_frame().transpose()
    changesMade = changesMade.rename(index={0:'3. Swapped'}, columns={0:'Precip',1:'Max Temp',2:'Min Temp',3:'Wind Speed'})
    # append number of new changes to RVDF
    ReplacedValuesDF = ReplacedValuesDF.append(changesMade)    
    return( DataDF, ReplacedValuesDF )
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    oldDF = DataDF
    oldCount = DataDF.count()
    diff = DataDF['Max Temp'] - DataDF['Min Temp'] #Less than zero for values that need to be swapped
    DataDF['Max Temp'].loc[diff > 25] = np.NaN
    DataDF['Min Temp'].loc[diff > 25] = np.NaN
    
    plt.figure(figsize=(9,6.5))
    oldDF['Max Temp'].plot(style='r')
    DataDF['Max Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Max Temperature for T_max-T_min > 25C - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_4.2_Range_MaxTemp.png')
    
    plt.figure(figsize=(9,6.5))
    oldDF['Min Temp'].plot(style='r')
    DataDF['Min Temp'].plot(style='g')
    plt.grid(True)
    plt.xlabel('Day')
    plt.ylabel('Temperature (C)')
    plt.title('Removal of Min Temperature for T_max-T_min > 25C - Field')
    plt.legend(['Before Quality Checking', 'After Quality Checking'], loc='best')
    plt.savefig('QC_4.3_Range_MinTemp.png')
    
    # Determine the number of changes made for each variable
    changesMade = oldCount - DataDF.count()
    changesMade = changesMade.to_frame().transpose()
    changesMade = changesMade.rename(index={0:'4. Range Fail'})
    # append number of new changes to RVDF
    ReplacedValuesDF = ReplacedValuesDF.append(changesMade)    
    return( DataDF, ReplacedValuesDF )
    return( DataDF, ReplacedValuesDF )

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    
    
    
    
    ReplacedValuesDF.to_csv("DataQualityCheckingChangesMade_Field.txt",header=True,sep='\t')
    
    
    

    
    DataDF.to_csv("DataQualityCheckingComplete_Field.txt", header=False, sep=' ')
    

    
    
    
    
    