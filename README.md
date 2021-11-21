This is a Help Lightning camera state playground.
## What the project does
Running the script `camerastate.py` will open a GUI window where you can play with various widgets to simulate the camera state changes in a Help Lightning call.
## Why the project is useful
Help Lightning has many properties that interact with each other and affect the state of the physical camera on the device as well as the participant's `camera_on` state as presented to all participants in the call.

Local device settings:
- physical camera detected
- camera permissions granted
- a button in call to toggle the camera state

In call settings that indirectly affect the camera:
- Role
- Task field source

Administrative settings that affect the camera:
- Call Center Mode

More features are regularly added that impact the calculation for whether or not the camera should actually be on or not.

With this tool, the web, iOS, Android, Server, and Product teams can quickly test state changes to make sure we all agree on the state transitions and implement them in a consistent way.
## How to get started
Before getting started, make sure you have tkinter installed.
```
brew install python-tk
```
Use python3 to run `camerastate.py`. A window should be created where you can manipulate the various properties that affect the camera in HL.

![screenshot](/camerastate_screenshot.png)
The bottom row of settings (GSS Camera State and Physical Camera State) are particularly important, and will be the hardest to get right.
## Who maintains the project
This project will only be useful if multiple people from multiple teams interact with it and give feedback. Scott Wehby will maintain the project, but anyone is welcome to submit pull requests.