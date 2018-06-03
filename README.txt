Install + Setup
1.	Create a new folder (default location C:/tempPy/, if you use a different location, find where this line is in the gameBackups.py file and put the new location in instead. Line 32 currently. 
		Also modify the GameBackups.bat file to match this location. 
	
2.	Install Python 3 if not already installed, make sure it is added to the Windows PATH settings.

3.	Move gameBackups.py and GameBackups.bat to the folder created in step 1.

4. 	Modify gameBackups.py file with your settings.
		Set the 'path' variable on line 26 to the directory you want your game files saved to.
		Add all of your game folders to the program following the examples shown at line 41
		Only modify things that are in the 'def main():' section of code, that is where all of the user settings are.
		Read the comments for more information on what each variable does.

5.	Create a shortcut for the 'GameBackups.bat' file and copy this, then paste it in your Windows Start menu, in the 'Startup' folder. This will launch the program every time you log in. Or create a service call, or any other method you choose.


How this works: You provide a list of folders and names for the folders (these names will be the name of the zip file created, not the name of the source folder.) You provide a folder location to save to, I use a sync'd cloud folder. 
	Every time the program runs, it zips each folder individually, then creates a checksum for that zip. It compares that checksum to the files already in the save folder. If that checksum exists, nothing has changed in that folder since
	the previous backup, and it will not save. Other wise, it saves the zip file to the save folder with the name and a datetime stamp in the name. This allows you to back up your settings folders frequently without clogging up your cloud storage.
	