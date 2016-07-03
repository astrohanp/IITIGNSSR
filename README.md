# Polar-xS GNSS Receiver IIT Indore

This program is a wrapper in Python for analysing the Total Electron Content data of GNSS satellite constellations like GPS and GLONASS.

The PolaRxS is a multi-frequency multi-constellation receiver dedicated to ionospheric monitoring and space weather applications.
It operates on dual frequencies of L1 and L2 bands. The signals coming from the satellites are right circularly polarised which 
is received by the receiver and converted into ASCII format and saved in that format as an SBF file, which is then converted
to a comma delimited ISMR file by the sbf2ismr program. The program extracts data from these ismr files and makes the necessary
conversions for plotting the data.

## Running the program

* Start by downloading/cloning the repository in your system. Please check that you have all the required packages and version mentioned in the REQUIRE file.
* Unzip the data.zip file.
* If you have updated data put it in the data folder.
* Next open a terminal/command prompt and navigate to the directory of the project. Then type

  `~$ cd src`
  
  `~$ python main_file.py`
* The Program has the following 3 options for generating the plot according to user's choice:
    1. TEC vs Time
    2. Vertical TEC vs Time
    3. Iono-delay vs Time
* The program will then show the date range of data available. Then enter valid dates that are in this range whose plot is required.
* For generating the plot of a single day just enter the same start and end date.
