# ARAM Balance Viewer

Simple program that displays the ARAM balance changes for your current champion while in champ select. Data is from the wiki, so it may not always be accurate. Created over a few days, so don't expect it to be perfect

![image](https://github.com/J-P-Walter/ARAM-Balance-Viewer/assets/70927525/8ed963cc-bdf1-4574-a9d7-76416785f189)

## To Run

Download [the zip file](https://github.com/J-P-Walter/ARAM-Balance-Viewer/blob/main/AramBalanceViewer.zip).

Run AramBalanceViewer.exe. Your next ARAM champ select should have a small GUI displaying the data. Because it is an .exe file, you should be able to add it to your Windows startup so it will be ready to go every time you open League. The program is designed to stay running in the background until champ select, so you should be able to run it once and be good.

Any errors will be logged to error.log, I am sure there are still some bugs so please let me know if you run into any.

## Future Implementation

Clean up code. The main code is all in one file, would like to have split the gui and driver up into separate files/classes, but strugged to do so with the threads.
Clean up GUI. Currently, it is very basic. Improving the look or doing something with .dll injection would make it look better.
