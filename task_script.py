# Generic Image Rating Task
#   In this task, participants are presented with individual images and
#   rate them acording to the scales defined below.
#
# Modfied:
#   March 2017 (Damien Crone)
#
# Preliminaries ---------------------------------------------------------------

# Import modules
import os
import csv
import datetime
from psychopy import gui, core, visual, event # This may require installation
import sys
from random import shuffle

# Set working directory to script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Specify paths in dictionary
path = {}
path = {
    "stim_dir": "stimuli/", # Location of images
    "out": "raw_data/" # Location to save raw data (this will be created automatically)
}

# Make directories (if necessary)
if not os.path.exists(path["out"]):
    os.makedirs(path["out"])

# Define task versions
task_versions = [
    "moral",
    "valence",
    "arousal"
]

# Initialise task parameter dictionary
param = {
    'session_start': '{:%y%m%d_%H%M%S}'.format(datetime.datetime.now()),
    'version': "unspecified"
}


# Get participant info ---------------------------------------------------------

# Get participant ID
gui_id = gui.Dlg() # create box
gui_id.addField("ID:")
gui_id.show()

if gui_id.OK:
    param["id"] = gui_id.data[0]
else:
    sys.exit("user cancelled")


# Get task version -------------------------------------------------------------

while param["version"] == "unspecified":

    gui_task = gui.Dlg() # create box
    gui_task.addField("Task version:", choices=task_versions)
    gui_task.show()

    if gui_task.OK:
        param["version"] = gui_task.data[0]
    else:
        sys.exit("user cancelled")


# Assign rating scale ----------------------------------------------------------

if param["version"] == "moral":

    param["question"] = "This image portrays something..."
    param["anchors"] = "Immoral/Blameworthy(1) - Moral/Praiseworthy(5)"
    param["choices"] = [1, 2, 3, 4, 5]
    param["keys"] = ['1', '2', '3', '4', '5']

elif param["version"] == "valence":

    param["question"] = "This image is..."
    param["anchors"] = "Unpleasant or Negative(1) - Pleasant or Positive(5)"
    param["choices"] = [1, 2, 3, 4, 5]
    param["keys"] = ['1', '2', '3', '4', '5']

elif param["version"] == "arousal":

    param["question"] = "This image is..."
    param["anchors"] = "Calming(1) - Exciting(5)"
    param["choices"] = [1, 2, 3, 4, 5]
    param["keys"] = ['1', '2', '3', '4', '5']

else:

    sys.exit("No rating scale available for task version")


# Select stimuli ---------------------------------------------------------------

# List stimuli in directory
all_files = os.listdir(path["stim_dir"])
stim_list = [s for s in all_files if "b" in s]
print(len(stim_list))

# Randomise stimlus order
shuffle(stim_list)


# Generate session file --------------------------------------------------------

# Generate filename
fn_str = param["version"] + "_" + param["id"] + "_" + param["session_start"] + ".csv"

# Concatenate output path with filename
if param["id"] == "test":
    path["out_fn"] = path["out"] + "TESTFILE_" + fn_str
else:
    path["out_fn"] = path["out"] + fn_str

# Initialise csv file
task_output = open(path["out_fn"], 'wb')
wr = csv.writer(task_output, quoting=csv.QUOTE_ALL)
wr.writerow(["id","version","img","rating","rt","timestamp"])


# Open window ------------------------------------------------------------------

win = visual.Window(
    size=[1000, 750],
    units="pix",
    color=[1, 1, 1],
    allowGUI=False,
    fullscr=False,
)


# Begin loop through stimuli ---------------------------------------------------

trial_n = 0

for stimulus in stim_list:

    trial_n = trial_n + 1

    # Get image filename
    img_fn = path["stim_dir"] + stimulus

    # Pause for 100ms
    core.wait(0.1)

    # Construct image component
    imgStim = visual.ImageStim(win, image=img_fn)

    # Construct text component above image
    txtQuestion = visual.TextStim(
        win,
        text=param["question"],
        alignHoriz="center",
        pos=(0, 250),
        color=[0, 0, 0]
    )
    txtAnchor = visual.TextStim(
        win,
        text=param["anchors"],
        alignHoriz="center",
        pos=(0, 230),
        color=[0, 0, 0]
    )

    # Construct text component above image
    counter_txt = str(trial_n) + "/" + str(len(stim_list))
    txtCounter = visual.TextStim(
        win,
        text=counter_txt,
        alignHoriz="center",
        pos=(0, 210),
        color=[0, 0, 0]
    )

    # Construct rating scale component below image
    ratingScale = visual.RatingScale(
        win,
        pos=(0, -250),
        textColor=[0, 0, 0],
        choices=param["choices"],
        respKeys=param["keys"],
        tickMarks=None
    )

    # Draw components and listen for response
    while ratingScale.noResponse:

        imgStim.draw()
        txtQuestion.draw()
        txtAnchor.draw()
        txtCounter.draw()
        ratingScale.draw()
        win.flip()

        theseKeys = event.getKeys(keyList=['escape'])

        # check for quit:
        if "escape" in theseKeys:
            core.quit()

    # Extract response
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()

    # Store relevant information in array - each element goes in a separate
    # column of the session csv file
    trial_result = [
        param["id"],                                            # Participant ID
        param["version"],                                       # Image feature
        stimulus,                                               # Image name
        rating,                                                 # Response
        decisionTime,                                           # RT
        '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())  # Timestamp
    ]

    # Append row with trial data to participant's csv file
    task_output = open(path["out_fn"], 'a')
    wr = csv.writer(task_output, quoting=csv.QUOTE_ALL)
    wr.writerow(trial_result)

    # Print trial data to console
    print(trial_result)

    # End loop through trials


# Tidy up ----------------------------------------------------------------------

win.close()
print("Task complete.")
