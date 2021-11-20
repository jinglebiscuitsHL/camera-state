from tkinter import *


# Call Center Mode, Turn Off Giver's (Agent's) Camera, Permissions, Role, Task Field Source, GHoD mode, Camera Menu Toggle, GSS camera_on

class CameraState():
    def __init__(self):
        self.callCenterMode = BooleanVar()
        self.turnOffAgentCamera = BooleanVar()
        self.permissionsGranted = BooleanVar()
        self.role = StringVar() # f2f, giver, receiver, observer
        self.role.set("f2f")
        self.taskFieldSource = StringVar() #live, freeze, photo, document
        self.taskFieldSource.set("live")
        self.ghodMode = "navigating" #navigating, presenting
        self.cameraMenuButtonOn = BooleanVar()
        self.cameraMenuButtonOn.set(True)
        self.gssCameraOn = BooleanVar()
        self.gssCameraOn.set(True)
        self.physicalCameraIsOn = BooleanVar()
        self.physicalCameraIsOn.set(True)

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
        callCenterFrame.pack(side = LEFT, anchor=NW)
        self.callCenterVar = IntVar()
        self.callCenterToggle = Checkbutton(callCenterFrame, text="Call Center Mode", variable=self.cameraState.callCenterMode)
        self.callCenterToggle.pack()
        self.agentCameraToggle = Checkbutton(callCenterFrame, text="Agent Camera Off", state="disabled", variable=self.cameraState.turnOffAgentCamera)
        self.agentCameraToggle.pack()
        
        permissionsFrame = LabelFrame(root, text="Camera Permissions")
        permissionsFrame.pack(side = LEFT, anchor=NW)
        self.cameraPermissionsToggle = Checkbutton(permissionsFrame, text="Camera Permissions Granted", variable=self.cameraState.permissionsGranted)
        self.cameraPermissionsToggle.pack()

        roleFrame = LabelFrame(root, text="Role")
        roleFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(roleFrame, text="f2f", variable=self.cameraState.role, value="f2f", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="giver", variable=self.cameraState.role, value="giver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="receiver", variable=self.cameraState.role, value="receiver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="observer", variable=self.cameraState.role, value="observer", command=self.onRoleChanged).pack(anchor=NW)

        self.taskFieldSourceFrame = LabelFrame(root, text="Task Field Source")
        self.taskFieldSourceFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="live", variable=self.cameraState.taskFieldSource, value="live").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="freeze", variable=self.cameraState.taskFieldSource, value="freeze").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="photo", variable=self.cameraState.taskFieldSource, value="photo").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="document", variable=self.cameraState.taskFieldSource, value="document").pack(anchor=NW)

        cameraMenuFrame = LabelFrame(root, text="Camera Menu")
        cameraMenuFrame.pack(side=LEFT, anchor=NW)
        Checkbutton(cameraMenuFrame, text="Camera On", variable=self.cameraState.cameraMenuButtonOn).pack()

        gssCameraStateFrame = LabelFrame(root, text="GSS Camera State")
        gssCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.gssCameraState = Checkbutton(gssCameraStateFrame, text="GSS Camera State On", variable=self.cameraState.cameraMenuButtonOn, state="disabled").pack()

        physicalCameraStateFrame = LabelFrame(root, text="Physical Camera State")
        physicalCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.physicalCameraState = Checkbutton(physicalCameraStateFrame, text="Physical Camera On", variable=self.cameraState.physicalCameraIsOn, state="disabled").pack()

    def create_callbacks(self):
        self.callCenterToggle["command"] = self.onCallCenterModeToggled

    def onCallCenterModeToggled(self):
        self.toggle_widget(self.agentCameraToggle)

    def onRoleChanged(self):
        if self.cameraState.role.get() == "f2f":
            for widget in self.taskFieldSourceFrame.winfo_children():
                widget["state"] = "disabled"
            self.cameraState.taskFieldSource.set("live")
        else:
            for widget in self.taskFieldSourceFrame.winfo_children():
                widget["state"] = "normal"


    def onCameraToggleButtonPressed(self):
        if not self.cameraState.cameraMenuButtonOn.get():
            self.cameraState.gssCameraOn.set(False)
        else:
            self.cameraState.gssCameraOn.set(True)

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
