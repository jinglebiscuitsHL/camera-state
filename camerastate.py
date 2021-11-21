from tkinter import *


# Call Center Mode, Turn Off Giver's (Agent's) Camera, Permissions, Role, Task Field Source, GHoD mode, Camera Menu Toggle, GSS camera_on

class CameraState():
    def __init__(self):
        self.callCenterMode = BooleanVar()
        self.turnOffAgentCamera = BooleanVar()
        self.userIsAgent = BooleanVar()
        self.permissionsGranted = BooleanVar()
        self.permissionsGranted.set(True)
        self.role = StringVar()  # f2f, giver, receiver, observer
        self.role.set("f2f")
        self.taskFieldSource = StringVar()  # live, freeze, photo, document
        self.taskFieldSource.set("live")
        self.ghodMode = "navigating"  # navigating, presenting
        self.cameraMenuButtonOn = BooleanVar()
        self.cameraMenuButtonOn.set(True)
        self.gssCameraOn = BooleanVar()
        self.gssCameraOn.set(True)
        self.physicalCameraState = StringVar()
        self.physicalCameraState.set("On")


class CameraStateUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.cameraState = CameraState()
        self.topFrame = Frame(self.master)
        self.topFrame.pack(side=TOP, anchor=NW)
        self.bottomFrame = Frame(self.master)
        self.bottomFrame.pack(side=TOP, anchor=NW)
        self.stateFrame = Frame(self.master, pady=30)
        self.stateFrame.pack(side=TOP, anchor=NW)
        self.create_widgets()

    def test_command(self, text):
        print(text)

    def create_widgets(self):
        callCenterFrame = LabelFrame(self.topFrame, text="Call Center Mode")
        callCenterFrame.pack(side=LEFT, anchor=NW)
        self.callCenterToggle = Checkbutton(callCenterFrame, text="Call Center Mode",
                                            variable=self.cameraState.callCenterMode, command=self.onCallCenterModeChanged)
        self.callCenterToggle.pack(anchor=NW)
        self.agentCameraToggle = Checkbutton(
            callCenterFrame, text="Agent Camera Off", state="disabled", variable=self.cameraState.turnOffAgentCamera, command=self.onCallCenterModeChanged)
        self.agentCameraToggle.pack(anchor=NW)
        self.userIsAgentToggle = Checkbutton(
            callCenterFrame, text="User Is Agent", state="disabled", variable=self.cameraState.userIsAgent, command=self.onCallCenterModeChanged)
        self.userIsAgentToggle.pack(anchor=NW)

        permissionsFrame = LabelFrame(self.topFrame, text="Camera Permissions")
        permissionsFrame.pack(side=LEFT, anchor=NW)
        self.cameraPermissionsToggle = Checkbutton(permissionsFrame, text="Camera Permissions Granted",
                                                   variable=self.cameraState.permissionsGranted, command=self.onPermissionsChanged).pack()

        roleFrame = LabelFrame(self.bottomFrame, text="Role")
        roleFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(roleFrame, text="f2f", variable=self.cameraState.role,
                    value="f2f", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="giver", variable=self.cameraState.role,
                    value="giver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="receiver", variable=self.cameraState.role,
                    value="receiver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="observer", variable=self.cameraState.role,
                    value="observer", command=self.onRoleChanged).pack(anchor=NW)

        self.taskFieldSourceFrame = LabelFrame(self.bottomFrame, text="Task Field Source")
        self.taskFieldSourceFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="live",
                    variable=self.cameraState.taskFieldSource, value="live", state="disabled").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="freeze",
                    variable=self.cameraState.taskFieldSource, value="freeze", state="disabled").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="photo",
                    variable=self.cameraState.taskFieldSource, value="photo", state="disabled").pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="document",
                    variable=self.cameraState.taskFieldSource, value="document", state="disabled").pack(anchor=NW)

        self.cameraMenuFrame = LabelFrame(self.bottomFrame, text="Camera Menu")
        self.cameraMenuFrame.pack(side=LEFT, anchor=NW)
        self.cameraOnToggle = Checkbutton(self.cameraMenuFrame, text="Camera On",
                                          variable=self.cameraState.cameraMenuButtonOn, command=self.onCameraToggleButtonPressed)
        self.cameraOnToggle.pack()

        gssCameraStateFrame = LabelFrame(self.stateFrame, text="GSS Camera State")
        gssCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.gssCameraState = Checkbutton(gssCameraStateFrame, text="GSS Camera State On",
                                          variable=self.cameraState.cameraMenuButtonOn, state="disabled").pack()

        physicalCameraStateFrame = LabelFrame(
            self.stateFrame, text="Physical Camera State")
        physicalCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.physicalCameraState = Checkbutton(
            physicalCameraStateFrame, text="Physical Camera On", variable=self.cameraState.physicalCameraState, onvalue="On", offvalue="Off", state="disabled").pack()
        self.cameraLabel = Label(physicalCameraStateFrame, textvariable=self.cameraState.physicalCameraState).pack()

    def onCallCenterModeChanged(self):
        if self.cameraState.callCenterMode.get():
            self.enable_widget(self.agentCameraToggle)
            self.enable_widget(self.userIsAgentToggle)
        else:
            self.disable_widget(self.agentCameraToggle)
            self.disable_widget(self.userIsAgentToggle)
        if self.userIsAgentToggle['state'] == "disabled":
            self.cameraState.userIsAgent.set(False)
        if (self.cameraState.turnOffAgentCamera.get() and self.cameraState.userIsAgent.get()):
            self.disableCameraMenu()
        else:
            self.enableCameraMenu()

    def toggle_widget(self, widget):
        if widget["state"] != "disabled":
            widget["state"] = "disabled"
        else:
            widget["state"] = "normal"

    def onPermissionsChanged(self):
        if self.cameraState.permissionsGranted.get():
            self.enableCameraMenu()
        else:
            self.disableCameraMenu()
            self.cameraState.physicalCameraState.set("Off")
            self.cameraState.cameraMenuButtonOn.set(False)

    def onRoleChanged(self):
        if self.cameraState.role.get() == "f2f":
            for widget in self.taskFieldSourceFrame.winfo_children():
                widget["state"] = "disabled"
            self.cameraState.taskFieldSource.set("live")
            self.enableCameraMenu()
        else:
            for widget in self.taskFieldSourceFrame.winfo_children():
                widget["state"] = "normal"
            if self.cameraState.role.get() == 'giver':
                self.enableCameraMenu()
            if self.cameraState.role.get() == 'observer':
                self.disableCameraMenu()

    def onCameraToggleButtonPressed(self):
        if self.cameraState.cameraMenuButtonOn.get():
            self.cameraState.gssCameraOn.set(True)
            self.cameraState.physicalCameraState.set("On")
        else:
            self.cameraState.gssCameraOn.set(False)
            self.cameraState.physicalCameraState.set("Off")

    def disable_widget(self, widget):
        widget.configure(state="disabled")

    def enable_widget(self, widget):
        widget.configure(state="normal")

    def enableCameraMenu(self):
        if ((self.cameraState.userIsAgent.get() and self.cameraState.turnOffAgentCamera.get())
            or not self.cameraState.permissionsGranted.get()
                or self.cameraState.role.get() == "observer"):
            return
        else:
            self.cameraOnToggle['state'] = "normal"

    def disableCameraMenu(self):
        self.cameraOnToggle['state'] = "disabled"


root = Tk()
app = CameraStateUI(master=root)
app.mainloop()
