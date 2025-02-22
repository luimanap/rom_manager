# ROM Manager

ROM Manager is a graphical tool developed in Python using `customtkinter` that helps organize and rename ROMs based on a `.dat` file (commonly used in emulators like RetroArch, Twilight Menu++, and others). This application handles the organization of ROM files based on their MD5 or SHA1 hash, along with performing checks like verifying CRC32 and file size.

## Features

- **Load `.dat` files**: Reads a `.dat` file containing information about ROMs and their hashes.
- **Rename ROMs**: Renames ROM files based on their MD5 or SHA1 hashes and associated metadata (name, size, CRC, etc.).
- **Organize ROMs into region-based folders**: Organizes ROMs into separate folders based on region.
- **Additional organization for Twilight Menu++**: Option to organize ROMs into batches of 200 per folder, ideal for use with Twilight Menu++.
- **Graphical Interface**: Built with `customtkinter` to provide a modern and functional user experience.

![image](https://github.com/user-attachments/assets/0772a7c7-0003-484e-a679-aee66d43566b)


## Requirements

- Python 3.x
- `customtkinter`
- `tkinter`
- `hashlib`
- `shutil`
- `binascii`
- `xml.etree.ElementTree`

You can install the required dependencies using `pip`:

```bash

pip install customtkinter

```

Usage
1. Select the ROMs folder
Click the "Browse" button next to the "ROMs Folder" input to select the folder where your ROMs are stored.

2. Select the .dat file
Click the "Browse" button next to the "DAT File" input to select the .dat file containing the ROM metadata (this could be a file used by emulators like RetroArch or similar).

3. Configure organization method
Check the "Organize for Twilight Menu++" box if you want to organize the ROMs into batches of 200 per folder.
The program will organize the ROMs by region (if available in the .dat file).
4. Execute the process
Click the "Execute" button to start the process. The app will verify the ROMs by comparing their hashes with those in the .dat file. If everything is correct, the ROMs will be renamed and organized into subfolders by region and, if selected, into batches of 200 for Twilight Menu++.

5. Check the result
Progress messages and any errors will be displayed in the output box at the bottom of the window.

Additional Features
Size Verification: If the size of a ROM file does not match the expected size, a mismatch warning will be shown.
CRC32 Verification: If the CRC32 of a ROM does not match the expected value, a warning will also be displayed.
Example Workflow
Select the ROM folder you want to organize.
Select the corresponding .dat file.
Check the "Organize for Twilight Menu++" box if desired.
Click "Execute" and let the program process the ROMs.
The program will rename and move the ROMs into their respective folders according to the .dat file and organize them into subfolders if the Twilight Menu++ option is selected.

Contribution
If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. Be sure to follow best coding practices and add comments to your code.

License
This project is licensed under the MIT License - see the LICENSE file for details.
