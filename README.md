# ARAM Balance Viewer

Simple program that displays the ARAM balance changes for your current champion while in champ select. Data is from the wiki, so it may not always be accurate.

## To Run
Download [the zip file](https://github.com/J-P-Walter/ARAM-Balance-Viewer/blob/main/ABV.zip).

Run Aram_Balance_Viewer_1.0.exe and choose your install location. Once installed, navigate to the folder and run Aram_Balance_Viewer.launch.pyw. Your next ARAM champ select should have a small GUI displaying the data. Because it is an .exe file, you should be able to add it to your Windows startup so it will be ready to go every time you open League.

Alternatively, feel free to run main.py if you have python installed.

## Future Implementation

Clean up code. The main code is all in one file, would like to have split the gui and driver up into separate files/classes, but strugged to do so with the threads.
Clean up GUI. Currently, it is very basic. Improving the look or doing something with .dll injection would make it look better.
