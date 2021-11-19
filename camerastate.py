from tkinter import *


# Call Center Mode, Turn Off Giver's (Agent's) Camera, Permissions, Role, Task Field Source, GHoD mode, Camera Menu On, Camera Menu Off

class CameraState():
    def __init__(self):
        self.callCenterMode = BooleanVar()
        self.turnOffAgentCamera = BooleanVar()
        self.permissionsGranted = BooleanVar()
        self.role = "f2f" # f2f, giver, receiver, observer
        self.taskFieldSource = "none" #live, freeze, photo, document
        self.ghodMode = "navigating" #navigating, presenting

class CameraStateUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.cameraState = CameraState()
        self.create_widgets()
        self.create_callbacks()
    
    def test_command(self, text):
        print(text)

    def create_widgets(self):
        callCenterFrame = LabelFrame(root, text="Call Center Mode")
        callCenterFrame.pack(side = LEFT)

        self.callCenterVar = IntVar()
        self.callCenterToggle = Checkbutton(callCenterFrame, text="Call Center Mode", variable=self.cameraState.callCenterMode)
        self.callCenterToggle.pack()
        self.agentCameraToggle = Checkbutton(callCenterFrame, text="Agent Camera Off", state="disabled", variable=self.cameraState.turnOffAgentCamera)
        self.agentCameraToggle.pack()
        
        permissionsFrame = LabelFrame(root, text="Camera Permissions")
        permissionsFrame.pace(side = LEFT)

    def create_callbacks(self):
        self.callCenterToggle["command"] = self.onCallCenterModeToggled

    def onCallCenterModeToggled(self):
        self.toggle_widget(self.agentCameraToggle)

    def toggle_widget(self, widget):
        print(self.cameraState.callCenterMode.get())
        print("jedi", widget["state"])
        if widget["state"] != "disabled":
            widget["state"] = "disabled"
        else:
            widget["state"] = "normal"

    def disable_widget(self, widget):
        widget.configure(state="disabled")

    def enable_widget(self, widget):
        widget.configure(state="normal")


root = Tk()
app = CameraStateUI(master=root)
app.mainloop()
