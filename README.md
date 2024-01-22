# Metroid Dread Autosplitter

A simple auto split program in Python. This uses OCR to read parts of the screen and determine when an upgrade or location change has happened.

Primarily this was made for metroid dread speedrunning. This interfaces with LiveSplit and OBS to read the game screen and send a signal to LiveSplit when certain actions are detected.

Please understand updates will be slow to this. I do work fulltime and like playing videogames so during the week I probably won't spend much time working on this. This project was really just a 'proof of concept' I made to see if the idea of using OCR on the game screen was viable, and surprisingly it was! 

## Prerequisites

1. Install TesseractOCR. I used the 64-bit binary from here: https://github.com/UB-Mannheim/tesseract/wiki

2. Install OBS & OBS-VirtualCam: https://obsproject.com/forum/resources/obs-virtualcam.949/. Start it by going to Tools -> VirtualCam -> Start. Maybe set to Auto-start so you don't gotta do this every time. 

3. Python: https://www.python.org/downloads/. I built this using Python 3.9 but 3.10 should work just fine. When installing, make sure you select 'Add Python to PATH'.  

4. Livesplit Server: https://github.com/LiveSplit/LiveSplit.Server. In LS add the 'LiveSplit Server' component to your layout in Livesplit, and then right click your splits and go to Control -> Start Server.

## How to use:

1. Download this repository to some location. 

2. Open a Command prompts to the repository directory. In that command prompt run 'pip install .' (note the period). If this doesn't work, try 'python -m pip install .' 

3. You should now be able to run main.py from the 'src' directory. 

## Configuring 

https://youtu.be/LtUYlbXf4HE

Pls report any bugs in the issues tab or feel free to leave any feature requests. I know there's a lot to add but right now i just kind of add stuff as I need it 
