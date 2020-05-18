#Taking videos

Using IC Capture on the Windows computer in the Campy room, I plugged in the camera attached to the microscope (black power cable and blue ethernet cable) and selected camera (DMK 23G618 (3410340)) from software - when opening for the first time, the Select camera dialog box should open automatically, otherwise, go to File -> New. Note - every once in a while, the software loses the camera or can't find it - just wiggle the black cable on top of the camera and File -> New or Fresh in the dialog box again to reacquire.
In camera software, have video selected (the little video camera icon along the top).
Change the frame rate (fps) to 60 = default is 120 (FPS drop down box in the top set of menus) and that can get jumpy - also, 60 frames a second is still lots.
Camera settings - 60 fps, auto ref 100, max brightness, 10 sec video. Camera had frame rate collection issues - went to menu at top (Device) and found setting reset (Reset properties) and reset back to defaults - helped get frame rate back to proper level
Get microscope slide in focus on the microscope. Use 100x oil immersion with Phase 3 (Ph3 on wheel under microscope stage). If the cells don't come out fairly dark, adjust the phase knobs under the stage to optimize. Make sure the lever on the right side of the eye pieces is pulled out so you get viewing through the eye pieces AND the camera.
On the far left of in the software is a settings icon (looks like a mini window with a red dot on it), click it to open a settings box. Click the Settings button at the bottom of the box to open all the settings. From the Video File tab, choose the folder to store the videos in and the name prefix. Keep the name having the Year-month-day-hour-minute-second the video starts. In the 3rd tab (Advanced) is an option to have the video stop after a certain period of time - select 10 seconds. Click OK to accept all the settings.
**Make sure to update the video name with each sample time (changing condition) so you recognize it later.**
To start a video, just click the red dot record button in the main Record Video File window. If you selected the auto stop above, the video will automatically stop after 10 sec.
**VERY important to let the slide settle to not have drift.**
Take 3 videos of each condition, moving to a completely different field of view each time. Watch the number of frames collected in the settings box and if less than 590 of the predicted 599 frames are collected, retake video.
If videos have difficult time collecting all the frames consistently (more than 10 videos in a row) or if the video is freezing at frame 2, it could mean the D:/Data drive is getting too full. See how much data is in Data (check properties) and move data to off computer and delete to allow for more room. 
Try to find focus plane where a reasonable number of cells are swimming, not focusing on cells stuck to the glass slide at the bottom or cover slip at the top. Start with RF buffer alone (1cP start) and work from high cP to low cP, alternating between MC and Ficoll. At end, do another RF buffer alone (1 cP end) to ensure that culture did not stop swimming or slow down during course of experiment.
When finished collecting all the videos, transfer to lab computer with WinSCP
Also, made negative stained grids of the stock culture (the OD600 = ~5.0) - standard procedure (glow discharge 300 mesh grids 10/30, add 2 ul sample to grid, 1 min sit, add 30 ul 2% uranyl acetate to dip off, 1 min sit, wick dry with filter paper). Had cells in media and did a wash in 10 mM HEPES pH 7.4.

#Processing videos for particle tracking

##Step 1 - Import stack into ImageJ/Fiji and invert black/white

Start Fiji on desktop by typing fiji at any command prompt in terminal/
Load video by going to File -> Open
Pick video
When dialog box comes up, make sure virtual stack is selected, click to add covert to greyscale

##Convert video to stack of images
Image -> Duplicate, click duplicate stack

##Convert the images black/white 
(the particle tracking software tracks white particles and the bacteria are currently phase contrast black in the video)
Edit -> Invert; yes to do for all images

##Particle tracking

Plugins -> Mosaic -> ParticleTracker 2D/3D; Asks if data is 3D - No
Software opens and you get a dialog box with parameters:
Particle Detection parameters:
Radius (how big each particle) - picked 4 for Campylobacter, 5 for Salmonella
Cutoff (space that has to be between particles) - 0
Per/abs (no idea, but this values works well) - 0.1

Can preview with preview button to make sure the first 3 parameters find reasonable particles.

##Particle Linking parameters
Linking range (how many frames can the particle be missing for - look ahead to track) - 5
Displacement (how many pixels can a particle maximally travel per frame) - 10
Dynamics (what type of movement is being tracked) - constant velocity

Then let it run by clicking OK. Can follow progress at the bottom of the main ImageJ window.

When finished, the Results window opens up. From the buttons in the lower half of the Results window, select the Visualize All Trajectories button to view the video of what you got. Slide the slider at the bottom of the video that pops up to see the trajectories.
You can filter the trajectories with fewer than a set number of frames with the Filter Options button at bottom of video - I selected 10 frames in the box to remove trajectories with less than 1/6 of a sec. Wait a few seconds while the software recalculates - you will see your new number of trajectories in the Results window.

##Step 4 - Saving trajectory video and spreadsheet

With the coloured trajectory video window active, go to File -> Save As -> AVI; Save it as JPEG for presentation in powerpoint file and Frame rate of 60 fps

Save trajectories pixel coordinates by going to Results window and clicking the All Trajectories to Table button (wait to load, can take a minute). In that window, go to File -> Save As -> and give name (saves as Excel sheet in .csv format - Note, the software has defaulted to .xls as the extension; my .py script below doesn't work with that, so just name .csv - works exactly the same)

Noted that processing several videos in a row causes Fiji to freeze - memory limitations. It works to close Fiji after each video and restart from command line.


I also took a picture of the 1 mm scale bar rule slide and measured it in ImageJ. 0.01 mm = 56 pixels. So 10 um = 56 pixels or 1 um = 5.6 pixels. Alternatively, that means 0.18 um/pixel.
As a reminder, I take the videos at 60 frames/sec, which is also 0.017 sec/frame

#Morgan wrote me a script called processTrajectories.py

This has the format:

processTrajectories.py input_file_name um/pixel_value frame_rate_value -t fewer_than_this_many_trajectories_remove > output_file

If I follow the process given above, this makes the command:
processTrajectories.py Organism_name_condition_time.csv 0.18 60 -t 10 > Organism_name_condition_time.csv.dat
processTrajectories.py Organism_name_condition_time.csv 0.18 60 -t 10 > Organism_name_condition_time.csv.dat

If I put all my tables into folders for each bug and create a new folder called "processed_data", I can process all the files at once as long as the input files are in directories below where I run this command:

find . -name "*.csv" | awk -F '/' '{print "processTrajectories.py "$_" 0.18 60 -t 10 > processed_data/"$3".csv"}' | sh

What this does is finds all the files that end in .csv, extract their names, print them to fill in the $_ or $3, and execute the command (sh)

Note: if you run this command once, you will generate results files with the ending .csv. If you then run the command again, you will get a bunch of errors saying improper number of arguments (or something similar) because the processTrajectories files your generated the first time don't have the same format as the video results file. You can delete the files in the processed_data folder and rerun everything or just move the new files you need to run to a new folder and do again somewhere on the system. 

Open the processTrajectories results files in a text editor or excel and get the mean swimming speed to graph.
