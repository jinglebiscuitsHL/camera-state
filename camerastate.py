from tkinter import *


# Call Center Mode, Turn Off Giver's (Agent's) Camera, Permissions, Role, Task Field Source, GHoD mode, Camera Menu Toggle, GSS camera_on

class CallCenterState():
    def __init__(self):
        self.callCenterMode = BooleanVar()
        self.callCenterMode.set(False)
        self.turnOffAgentCamera = BooleanVar()
        self.turnOffAgentCamera.set(False)
        self.userIsAgent = BooleanVar()
        self.userIsAgent.set(False)
    
    def isCameraDisabled(self):
        return self.callCenterMode.get() and self.turnOffAgentCamera.get() and self.userIsAgent.get()

class CameraState():
    def __init__(self, camera_disabled):
        self.permissionsGranted = BooleanVar()
        self.role = StringVar()  # f2f, giver, receiver, observer
        self.taskFieldSource = StringVar()  # live, freeze, photo, document
        self.cameraMenuAvailable = BooleanVar()
        self.cameraMenuButtonOn = BooleanVar()
        self.gssCameraOn = BooleanVar()
        self.physicalCameraState = StringVar()
        self.startCall(camera_disabled)

    def startCall(self, camera_disabled):
        self.cameraDisabled = camera_disabled # from GSS join extra permissions.
        self.permissionsGranted.set(True)
        self.role.set("f2f")
        self.taskFieldSource.set("live")
        self.ghodMode = "navigating"  # navigating, presenting
        self.cameraMenuAvailable.set(not self.cameraDisabled)
        self.cameraMenuButtonOn.set(not self.cameraDisabled)
        self.gssCameraOn.set(True)
        if self.cameraDisabled:
            self.physicalCameraState.set("Off")
        else:
            self.physicalCameraState.set("On")

    def turnCameraOn(self):
        if (self.role.get() == "observer" or not self.permissionsGranted.get() or not self.cameraMenuButtonOn.get()
                or self.cameraDisabled):
            return
        self.physicalCameraState.set("On")

    def turnCameraOff(self):
        self.physicalCameraState.set("Off")

    def verifyState(self):
        """Returns -1 if the state is incorrect. Returns 0 otherwise"""
        if (self.role.get() == 'observer' or not self.permissionsGranted.get() or not self.cameraMenuButtonOn.get()
            or (self.role.get() == 'receiver' and self.taskFieldSource.get() != 'live')
                or self.cameraDisabled):
            if self.physicalCameraState.get() == "On":
                # perm granted, receiver, freeze, cam on, physical cam on, switch on call center mode
                raise Exception
        if (not self.shouldCameraMenuBeAvailable() and self.cameraMenuAvailable.get()):
            if self.cameraMenuAvailable.get():
                raise Exception

    def shouldCameraMenuBeAvailable(self):
        if (self.role.get() == 'observer' or not self.permissionsGranted.get() or
            (self.role.get() == 'receiver' and self.taskFieldSource.get() != 'live') or
                self.cameraDisabled):
            return False
        else:
            return True


class CameraStateUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.callCenterState = CallCenterState()
        self.cameraState = CameraState(self.callCenterState.isCameraDisabled())
        self.callCenterFrame = Frame(self.master)
        self.callCenterFrame.pack(side=TOP, anchor=NW)
        self.inCallUIFrame = Frame(self.master)
        self.inCallUIFrame.pack(side=TOP, anchor=NW)
        self.stateFrame = Frame(self.master, pady=30)
        self.stateFrame.pack(side=TOP, anchor=NW)
        self.create_widgets()

    def create_widgets(self):
        callCenterFrame = LabelFrame(self.callCenterFrame, text="Call Center Mode")
        callCenterFrame.pack(side=LEFT, anchor=NW)
        Label(callCenterFrame, text="Changing these settings resets the call.").pack(anchor=NW)
        self.callCenterToggle = Checkbutton(callCenterFrame, text="Call Center Mode",
                                            variable=self.callCenterState.callCenterMode, command=self.onCallCenterModeChanged)
        self.callCenterToggle.pack(anchor=NW)
        self.agentCameraToggle = Checkbutton(
            callCenterFrame, text="Agent Camera Off", state="disabled", variable=self.callCenterState.turnOffAgentCamera, command=self.onCallCenterModeChanged)
        self.agentCameraToggle.pack(anchor=NW)
        self.userIsAgentToggle = Checkbutton(
            callCenterFrame, text="User Is Agent", state="disabled", variable=self.callCenterState.userIsAgent, command=self.onCallCenterModeChanged)
        self.userIsAgentToggle.pack(anchor=NW)

        permissionsFrame = LabelFrame(self.inCallUIFrame, text="Camera Permissions")
        permissionsFrame.pack(side=LEFT, anchor=NW)
        self.cameraPermissionsToggle = Checkbutton(permissionsFrame, text="Camera Permissions Granted",
                                                   variable=self.cameraState.permissionsGranted, command=self.onPermissionsChanged).pack()

        roleFrame = LabelFrame(self.inCallUIFrame, text="Role")
        roleFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(roleFrame, text="f2f", variable=self.cameraState.role,
                    value="f2f", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="giver", variable=self.cameraState.role,
                    value="giver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="receiver", variable=self.cameraState.role,
                    value="receiver", command=self.onRoleChanged).pack(anchor=NW)
        Radiobutton(roleFrame, text="observer", variable=self.cameraState.role,
                    value="observer", command=self.onRoleChanged).pack(anchor=NW)

        self.taskFieldSourceFrame = LabelFrame(
            self.inCallUIFrame, text="Task Field Source")
        self.taskFieldSourceFrame.pack(side=LEFT, anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="live",
                    variable=self.cameraState.taskFieldSource, value="live", state="disabled", command=self.onTaskFieldChanged).pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="freeze",
                    variable=self.cameraState.taskFieldSource, value="freeze", state="disabled", command=self.onTaskFieldChanged).pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="photo",
                    variable=self.cameraState.taskFieldSource, value="photo", state="disabled", command=self.onTaskFieldChanged).pack(anchor=NW)
        Radiobutton(self.taskFieldSourceFrame, text="document",
                    variable=self.cameraState.taskFieldSource, value="document", state="disabled", command=self.onTaskFieldChanged).pack(anchor=NW)

        self.cameraMenuFrame = LabelFrame(self.inCallUIFrame, text="Camera Menu")
        self.cameraMenuFrame.pack(side=LEFT, anchor=NW)
        self.cameraOnToggle = Checkbutton(self.cameraMenuFrame, text="Camera On",
                                          variable=self.cameraState.cameraMenuButtonOn, command=self.onCameraToggleButtonPressed)
        self.cameraOnToggle.pack()

        gssCameraStateFrame = LabelFrame(
            self.stateFrame, text="GSS Camera State")
        gssCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.gssCameraState = Checkbutton(gssCameraStateFrame, text="GSS Camera State On",
                                          variable=self.cameraState.cameraMenuButtonOn, state="disabled").pack()
        self.cameraState.cameraMenuAvailable.trace_add(
            "write", self.updateCameraMenuFrame)

        physicalCameraStateFrame = LabelFrame(
            self.stateFrame, text="Physical Camera State")
        physicalCameraStateFrame.pack(side=LEFT, anchor=NW)
        self.physicalCameraState = Checkbutton(
            physicalCameraStateFrame, text="Physical Camera On", variable=self.cameraState.physicalCameraState, onvalue="On", offvalue="Off", state="disabled").pack()
        self.cameraLabel = Label(
            physicalCameraStateFrame, textvariable=self.cameraState.physicalCameraState).pack()

    def onCallCenterModeChanged(self):
        print("onCallCenterModeChanged")
        if self.callCenterState.callCenterMode.get():
            self.enableWidget(self.agentCameraToggle)
            self.enableWidget(self.userIsAgentToggle)
        else:
            self.disableWidget(self.agentCameraToggle)
            self.disableWidget(self.userIsAgentToggle)
        if self.userIsAgentToggle['state'] == "disabled":
            self.callCenterState.userIsAgent.set(False)
        self.cameraState.startCall(self.callCenterState.isCameraDisabled())
        self.onRoleChanged()
        self.cameraState.verifyState()

    def onPermissionsChanged(self):
        print("onPermissionsChanged")
        if self.cameraState.permissionsGranted.get():
            self.enableCameraMenu()
        else:
            self.disableCameraMenu()
            self.cameraState.turnCameraOff()
            self.cameraState.cameraMenuButtonOn.set(False)
        self.cameraState.verifyState()

    def onRoleChanged(self):
        print("onRoleChanged")
        if self.cameraState.role.get() == "f2f":
            for widget in self.taskFieldSourceFrame.winfo_children():
                self.disableWidget(widget)
            self.cameraState.taskFieldSource.set("live")
            self.enableCameraMenu()
        else:
            for widget in self.taskFieldSourceFrame.winfo_children():
                self.enableWidget(widget)
            if self.cameraState.role.get() == 'giver':
                self.enableCameraMenu()
                self.onTaskFieldChanged()
            if self.cameraState.role.get() == 'receiver':
                self.cameraState.cameraMenuButtonOn.set(True)
                self.enableCameraMenu()
                self.onTaskFieldChanged()
            if self.cameraState.role.get() == 'observer':
                self.disableCameraMenu()
        self.cameraState.verifyState()

    def onTaskFieldChanged(self):
        print("onTaskFieldChanged")
        if self.cameraState.role.get() == "receiver":
            if self.cameraState.taskFieldSource.get() == "live":
                self.cameraState.turnCameraOn()
                self.enableCameraMenu()
            else:
                self.cameraState.turnCameraOff()
                self.disableCameraMenu()
        self.cameraState.verifyState()

    def onCameraToggleButtonPressed(self):
        print("onCameraToggleButtonPressed")
        if self.cameraState.cameraMenuButtonOn.get():
            self.cameraState.gssCameraOn.set(True)
            self.cameraState.turnCameraOn()
        else:
            self.cameraState.gssCameraOn.set(False)
            self.cameraState.turnCameraOff()
        self.cameraState.verifyState()

    def updateCameraMenuFrame(self, var, indx, mode):
        if self.cameraState.cameraMenuAvailable.get():
            self.cameraMenuFrame.pack()
        else:
            self.cameraMenuFrame.pack_forget()

    def enableCameraMenu(self):
        if self.cameraState.shouldCameraMenuBeAvailable():
            self.cameraState.cameraMenuAvailable.set(True)
            if self.cameraState.cameraMenuButtonOn.get():
                self.cameraState.turnCameraOn()

    def disableCameraMenu(self):
        self.cameraState.turnCameraOff()
        self.cameraState.cameraMenuAvailable.set(False)

    def disableWidget(self, widget):
        widget['state'] = "disabled"

    def enableWidget(self, widget):
        widget['state'] = "normal"


root = Tk()
root.title("HL Camera State Machine")
app = CameraStateUI(master=root)
app.mainloop()
