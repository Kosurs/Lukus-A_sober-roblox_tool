<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1 align="center">
        <img src="https://i.postimg.cc/KYg2SKGf/59a711a4-5083-43ac-a1fd-216876fba3e2-removalai-preview.png" width="40" alt="Logo"/> 
         Lukus - Sober FFlags Modifier 
    </h1>
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1 align="center">
        <img src="https://i.ibb.co/yBM2GKZ2/Captura-de-tela-de-2025-05-31-18-23-09.png"/>
        <img src="https://i.ibb.co/Cp6fCPkm/Captura-de-tela-de-2025-05-31-18-23-15.png"/>
    </h1>
</body>
</html>

# What is it?

Lukus - Sober FFlags Modifier is a GUI made for linux to view and modify Roblox Sober port FastFlags. It has an user-friendly interface to edit advanced graphics options, performance options, and experimental options for Sober without the need to manually edit JSONs

# How does it work?

Lukus reads and edits the config.json file from Sober, located at `~/.var/app/org.vinegarhq.Sober/config/sober/config.json`
The interface has three main tabs:

- Easy Access: Quick options and switches for FPS, graphics, lighting, and more.
FFlags: Manual FFlag editing, with a live preview and automatic backup.
- Credits: Information about the author and project.
#### All changes are applied only to the "fflags" field in the config file, keeping other settings untouched.The program automatically creates a backup of the original config file before saving.

# How to use it?

#### Requirements

Python 3.8+
GTK4 and PyGObject
Sober must have been started at least once (to create the config file)
Install dependencies on Ubuntu/Debian:

```
 sudo apt install python3-gi gir1.2-gtk-4.0
```
- Download or clone the code
- Save the lukus.py file in a folder.

- Run the program
-In the terminal, navigate to the folder and run:
```
python3 lukus.py
```
# TIP

If Sober hasn’t been started yet, run it once before using Lukus to ensure the config file exists.



