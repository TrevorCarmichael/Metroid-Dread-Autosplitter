# Metroid Dread Autosplitter

A simple auto split program in Python. This uses OCR to read parts of the screen and determine when an upgrade or location change has happened.

At the moment I can only split on these actions. I've been trying to think of methods to split in other spots but that's tricky and this was easy. 

Please understand updates will be slow to this. I do work fulltime and like playing vidyagames so during the week I probably won't spend much time working on this. If you're someone who knows python then I'd recommend someone smarter than me forking this and making it better, or just make your own idk. This project was really just a 'proof of concept' I made that I guess might mature eventually. 

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
