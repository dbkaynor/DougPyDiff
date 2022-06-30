#!/usr/bin/python StartFile
import sys
import os
import time
import platform
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
import hashlib  # sha1
import filecmp
import binascii
import shutil
import argparse
import re
import subprocess
import inspect
import __main__ as main
from ToolTip import ToolTip
from send2trash import send2trash
from MultiListbox import MultiListbox

Main = tkinter.Tk()

Geometry = tkinter.StringVar()
ProgramVersionNumber = tkinter.StringVar()
OptionsTopLevelVar = None
BatchTopLevelVar = None
FileInfoTopLevelVar = None
SplashTopLevelVar = None
FileRenameTopLevelVar = None
DataBox = None
DataFrame = None
CommentsListVar = []
SelectedListVar = []

CheckSumAutoVar = tkinter.BooleanVar()
CheckSumTypeVar = tkinter.IntVar()
FileTimeTriggerScaleVar = tkinter.IntVar()
TriggerNumberOfFilesVar = tkinter.IntVar()
DoNotAskNumberOfFilesVar = tkinter.BooleanVar()
StatusVar = tkinter.StringVar()
ShowLineNumberVar = tkinter.StringVar()
LogFileNameVar = tkinter.StringVar()
ProjectFileNameVar = tkinter.StringVar()
ProjectFileExtensionVar = tkinter.StringVar()
FileLeftNameVar = tkinter.StringVar()
FileRightNameVar = tkinter.StringVar()
SystemEditorVar = tkinter.StringVar()
SystemDifferVar = tkinter.StringVar()
SystemRenamerVar = tkinter.StringVar()
SystemLocaterVar = tkinter.StringVar()
StartUpDirectoryVar = tkinter.StringVar()
ShowBothCheckVar = tkinter.BooleanVar()
ShowDiffCheckVar = tkinter.BooleanVar()
ShowLeftCheckVar = tkinter.BooleanVar()
ShowRightCheckVar = tkinter.BooleanVar()
ShowDirectoriesCheckVar = tkinter.BooleanVar()
AutoRefreshCheckVar = tkinter.BooleanVar()
RecycleCheckVar = tkinter.BooleanVar()
ConfirmCopyCheckVar = tkinter.BooleanVar()
ConfirmDeleteCheckVar = tkinter.BooleanVar()
ConfirmRenameCheckVar = tkinter.BooleanVar()
HelpFileVar = tkinter.StringVar()
LeftPathEntry = None
RightPathEntry = None
FilterEntry = None
SearchEntryBatch = None
SearchEntryMain = None
SearchRowStart = 0
SelectEntryBatch = None
SelectEntryMain = None
StartRowEntry = None
StopRowEntry = None
LeftSearchVar = tkinter.BooleanVar()
RightSearchVar = tkinter.BooleanVar()
StatusSearchVar = tkinter.BooleanVar()
MoreSearchVar = tkinter.BooleanVar()
CaseSearchVar = tkinter.BooleanVar()
BatchBlockMode = tkinter.BooleanVar()
BatchNumberItemsVar = tkinter.StringVar()
ProgramVersionNumber.set('1.0.0')

StartUpDirectory = os.path.split(sys.argv[0])[0]
os.chdir(StartUpDirectory)
# HelpFileVar.set(os.path.join(StartUpDirectoryVar.get(), 'DougPyDiff.hlp'))
debugFile = os.path.join(StartUpDirectory, "DougPyDiff.txt")
if os.path.exists(debugFile):
    os.remove(debugFile)


def line_info(message="nothing", show=False):
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    tString = f"{os.path.basename(i.filename)}:{i.lineno}  called from {i.function}  {message}" + os.linesep
    file1 = open(debugFile, "a")
    file1.write(tString)
    file1.close()
    if show:
        print(tString)

# ------------------------------
# This will either delete a file or move it to trash
# ------------------------------


def ShowResize(TraceString, Item):
    global GeometryVar
    if str(GeometryVar) != str(Item.geometry()):
        GeometryVar = Item.geometry()
        return ':'.join([TraceString, GeometryVar])


def MyMessageBox(
    Title='MyMessageBox',
    LabelText=[],
    TextMessage=None,
    bgColor='black',
    fgColor='white',
    Buttons=['Close'],
    Center=None,
    Geometry=None,
):

    def ButtonHandle(data):
        global ButtonResult
        ButtonResult = data
        MyMBMain.destroy()
        return data

    MyMBMain = tkinter()  # Create a main window
    MyMBMain.title(Title)
    MyMBMain.config(bg=bgColor)

    # This prints out the window geometry on configure event
    MyMBMain.bind('<Configure>', lambda e: ShowResize('MyMessageBox', MyMBMain))
    # parses the geometry parameter
    line_info(' '.join([Center, Geometry]))
    if not Geometry:
        Geometry = '250x250+10+20'
    Geom = Geometry.split('+')
    Size = Geom[0].split('x')
    XPos = int(Geom[1])
    YPos = int(Geom[2])
    XSize = int(Size[0])
    YSize = int(Size[1])

    # print(MyTrace(GFI(CF())), XPos, YPos, XSize, YSize)

    if 'None' in str(type(Center)):  # Uses the Geometry option
        line_info(' '.join(['Geometry: ', Geometry]))
    elif 'tkinter.Tk' in str(type(Center)):

        # center of the item pointed to
        # parses the geometry of the CenterParam window

        CenterParamGeometry = Center.geometry()

        # These are the values from the passed in parameters

        CenterParamGeom = CenterParamGeometry.split('+')
        CenterParamSize = CenterParamGeom[0].split('x')
        CenterParamXPos = int(CenterParamGeom[1])
        CenterParamYPos = int(CenterParamGeom[2])
        CenterParamXSize = int(CenterParamSize[0])
        CenterParamYSize = int(CenterParamSize[1])

        # These are the values from the message box

        MyMBMainGeom = Geometry.split('+')
        MyMBSize = MyMBMainGeom[0].split('x')
        # MyMBXPos = int(MyMBMainGeom[1])
        # MyMBYPos = int(MyMBMainGeom[2])
        MyMBXSize = int(MyMBSize[0])
        MyMBYSize = int(MyMBSize[1])

        # This is the calculated position for the messagebox

        XPos = CenterParamXPos + CenterParamXSize / 2 - MyMBXSize / 2
        YPos = CenterParamYPos + CenterParamYSize / 2 - MyMBYSize / 2
    elif 'center' in Center.lower():

        # center of the screen

        XPos = MyMBMain.winfo_screenwidth() / 2 - XSize / 2
        YPos = MyMBMain.winfo_screenheight() / 2 - YSize / 2

    MyMBMain.geometry('%dx%d+%d+%d' % (XSize, YSize, XPos, YPos))

    # Add some buttons
    # Theoretically an unlimited number of buttons can be added

    ButtonFrame = tkinter.Frame(MyMBMain, relief=tkinter.SUNKEN, bd=1, bg=bgColor)
    ButtonFrame.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)
    for a in reversed(Buttons):
        tkinter.Button(ButtonFrame, text=a, command=lambda a=a:
                       ButtonHandle(a)).pack(side=tkinter.RIGHT)

    # This adds labels for each message
    # Theoretically an unlimited number of labels can be added

    for x in range(len(LabelText)):

        tkinter.Label(MyMBMain, text=LabelText[x],
                      relief=tkinter.GROOVE,
                      fg=fgColor,
                      bg=bgColor).pack(expand=tkinter.FALSE,
                                       fill=tkinter.X)

    # A text box http://effbot.org/tkinterbook/text.htm

    if TextMessage:
        Yscrollbar = tkinter.Scrollbar(MyMBMain, orient=tkinter.VERTICAL)
        Yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        Xscrollbar = tkinter.Scrollbar(MyMBMain, orient=tkinter.HORIZONTAL)
        Xscrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        Textbox = tkinter.Text(
            MyMBMain,
            wrap=tkinter.NONE,
            width=XSize,
            height=YSize,
            bg=bgColor,
            fg=fgColor,
            yscrollcommand=Yscrollbar.set,
            xscrollcommand=Xscrollbar.set,
        )
        Textbox.pack()

        Yscrollbar.config(command=Textbox.yview)
        Xscrollbar.config(command=Textbox.xview)
        Textbox.insert(tkinter.END, TextMessage)

    MyMBMain.resizable(1, 1)
    MyMBMain.mainloop()


def RemoveAFile(File, Trash):
    line_info(os.path.join(['Remove a file: ', File, str(Trash)]))
    if not os.path.exists(File):
        return
    if Trash:
        try:
            send2trash(File)
            line_info(os.path.join(['Success send2Trash: ', File]))
        except OSError:
            tkinter.messagebox.showerror('Send file to trash error. ',
                                         os.path.join([File, 'Permissions?']))
            line_info(''.join(['Failed send2Trash: ', File]))
    else:
        try:
            os.remove(File)
            line_info(''.join(['Success remove: ', File]))
        except OSError:
            tkinter.messagebox.showerror('Delete a file error. ',
                                         os.path.join([File, 'Permissions?']))
            line_info(''.join(['Failed remove: ', File]))


# ------------------------------
# Show Disk Space
def DiskSpace():
    DiskSpace = shutil.disk_usage('/')
    message = os.path.join(['Diskspace:',
                            'Free: %f Gbytes' % (DiskSpace.free / 1e9),
                            'Used: %f Gbytes' % (DiskSpace.used / 1e9),
                            'Total: %f Gbytes' % (DiskSpace.total / 1e9)])
    tkinter.messagebox.showinfo('Disk space', message)
    line_info(message)
# ------------------------------


def StartFile(filename, args=[], Wait=True):
    command = []
    command.append(filename)
    command.extend(args)
    line_info(' '.join(['StartFile arguments: ', str(command)]))
    ce = None

    try:
        if Wait:
            ce = subprocess.call(command)
        else:
            ce = subprocess.Popen(command)

        # line_info(str(command) + ' ' + str(Wait) + '  ' + str(ce))
    except OSError:
        tkinter.messagebox.showerror('StartFile did a Badddddd thing ',
                                     ' '.join(['Arguments:',
                                               str(command),
                                               'Return code:',
                                               str(ce)]))
        return
# ------------------------------
# Parse the command line


def ParseCommandLine():
    parser = argparse.ArgumentParser(description='A tool to compare to directories and move files')
    parser.add_argument('-debug',
                        help='Enable debugging',
                        action='store_true')
    args = parser.parse_args()

    if args.debug:
        import pdb
        pdb.set_trace()
        line_info('debug is on')
    else:
        line_info('debug is off')

# ------------------------------
# Checks if file name exists
# File may be either on the system path
# or file may be a full path


def SearchPath(name):
    path = os.environ['PATH']
    for dir in path.split(os.pathsep):
        binpath = os.path.join(dir, name)
        if os.path.exists(binpath):
            return True
    return False


# ------------------------------
# Set up defaults in case there is no project file
# Initialize the variables
# Written over by StartUpStuff and by ProjectLoad
def SetDefaults():
    line_info('SetDefaults')
    LeftPathEntry.delete(0, tkinter.END)
    RightPathEntry.delete(0, tkinter.END)
    FilterEntry.delete(0, tkinter.END)
    SystemEditorVar.set('')
    SystemDifferVar.set('')
    SystemRenamerVar.set('')
    SystemLocaterVar.set('')
    ShowRightCheckVar.set(True)
    ShowLeftCheckVar.set(True)
    ShowBothCheckVar.set(True)
    ShowDiffCheckVar.set(True)
    ShowDirectoriesCheckVar.set(True)
    AutoRefreshCheckVar.set(True)
    ConfirmCopyCheckVar.set(True)
    ConfirmRenameCheckVar.set(True)
    ConfirmDeleteCheckVar.set(True)
    RecycleCheckVar.set(True)
    CheckSumAutoVar.set(True)
    CheckSumTypeVar.set(True)
    FileTimeTriggerScaleVar.set('10')
    TriggerNumberOfFilesVar.set('10')
    LeftSearchVar.set(True)
    RightSearchVar.set(True)
    StatusSearchVar.set(False)
    MoreSearchVar.set(False)
    CaseSearchVar.set(False)


# ------------------------------
# Initialize the program
def StartUpStuff():
    # -- Lots of startup stuff ------------------------------------
    # The following are defaults which may be over-written by a project file
    line_info('StartUpStuff')
    if sys.platform.startswith('linux'):
        SystemEditorVar.set('gedit')
        SystemDifferVar.set('meld')
        SystemRenamerVar.set('pyrename')
        SystemLocaterVar.set('dolphin')
        ProjectFileExtensionVar.set('prjl')
    elif sys.platform.startswith('win32'):
        SystemEditorVar.set('c:\\windows\\notepad.exe')
        SystemDifferVar.set('C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe')
        SystemRenamerVar.set('C:\\Program Files (x86)\\Ant Renamer\\Renamer.exe')
        SystemLocaterVar.set('explorer.exe')
        ProjectFileExtensionVar.set('prjw')

    StartUpDirectoryVar.set(os.getcwd())
    HelpFileVar.set(os.path.join(StartUpDirectoryVar.get(), 'PyDiffTk.hlp'))
    LogFileNameVar.set(os.path.join(StartUpDirectoryVar.get(), 'PyDiffTk.log'))

    line_info(' '.join(["OS:", str(os.environ.get('OS'))]))
    line_info(' '.join(["uname:", str(platform.uname())]))
    line_info(' '.join(["Number of argument(s):", str(len(sys.argv))]))
    line_info(' '.join(['Argument List: ', str(sys.argv)]))
    ProjectLoad('default')  # Now get the project settings


# ------------------------------
# This updates the ShowLineNumberVar label
def Update():
    line_info('Update')
    ShowLineNumberVar.set(' '.join([(str(DataBox.curselection()),
                                     'of',
                                     str(DataBox.size() - 1))]))
    BatchNumberItemsVar.set(' '.join([(str(DataBox.curselection()),
                                      'of',
                                       str(DataBox.size() - 1))]))
# ------------------------------


# Bound to F7
# x is a junk parameter
# Displays SelectedListVar by updating DataBox
def ShowSelectedList(x=''):
    global SelectedListVar
    line_info('Update')
    # if BatchBlockMode.get(): return
    DataBox.selection_clear(0, 99999)
    for x in SelectedListVar:
        DataBox.selection_set(x)
        DataBox.see(x)
    Update()


# ------------------------------
# Bound to F8
# x is a junk parameter
# Adds any selected rows to SelectedListVar and updates DataBox
def AddSelectedToList(x=''):
    global SelectedListVar
    line_info('AddSelectedToList')
    if BatchBlockMode.get():
        return
    # Get the currently selected index
    Current = str(DataBox.curselection())
    # Clean it up and extend to the list
    Current = re.sub('[(),\']', '', Current)

    if len(Current) < 1:
        return  # Nothing is selected so abort

    tmp = Current.split(' ')
    SelectedListVar.extend(tmp)

    # Now remove the dups from the list
    TempList = []
    for x in SelectedListVar:
        if x not in TempList:
            TempList.append(x)
    SelectedListVar = TempList

    # Clear DataBox and then repopulate it
    DataBox.selection_clear(0, 99999)
    for row in SelectedListVar:
        DataBox.selection_set(row)
        DataBox.see(row)
    Update()


# ------------------------------
# Will Remove a row from SelectedListVar and the Databox
def RemoveARow():
    message = 'Not ready yet'
    tkinter.messagebox.showerror('RemoveARow', message)
    line_info(message)
    Update()


# ------------------------------
# Bound to F9
# x is a junk parameter
# Clears SelectedListVar and the Databox
def ClearSelectedList(x=''):
    global SelectedListVar
    line_info('ClearSelectedList')
    SelectedListVar = []
    DataBox.selection_clear(0, tkinter.END)
    StartRowEntry.delete(0, tkinter.END)
    StopRowEntry.delete(0, tkinter.END)
    Update()


# ------------------------------
if __name__ == '__main__':  # noqa: C901

    # ------------------------------
    # This clears everything, terminal, GUI etc.
    def ClearAll():
        line_info('ClearAll')
        FileRenameTopLevelVar.withdraw()
        FileInfoTopLevelVar.withdraw()
        OptionsTopLevelVar.withdraw()
        BatchTopLevelVar.withdraw()
        DataBox.delete(0, tkinter.END)
        os.system(['clear', 'cls'][os.name == 'nt'])
        Main.update_idletasks()

# ------------------------------
    def UpdatePathEntry(trace, Path):
        line_info(' '.join(['UpdatePathEntry', trace, Path]))
        if os.path.isdir(Path):
            if not os.path.isdir(Path) or not os.access(Path, os.W_OK):
                tkinter.messagebox.showinfo('UpdatePathEntry error',
                                            os.linesep.join(['Path not a directory or not writable',
                                                             trace,
                                                             Path]))
        if trace == 'Left':
            LeftPathEntry.delete(0, tkinter.END)
            LeftPathEntry.insert(0, Path)
        elif trace == 'Right':
            RightPathEntry.delete(0, tkinter.END)
            RightPathEntry.insert(0, Path)
        else:
            tkinter.messagebox.showinfo('UpdatePathEntry error',
                                        os.linesep.join(['Bad trace',
                                                         trace,
                                                         Path]))

    # ------------------------------
    # This searches for matching strings in the data and selects the lines that match
    # If type is search then when a match is found high lite it a stop
    # If type is select all line that match are selected
    # CaseSearchVar enables/disables case sensitive searches
    # The user can select what data columns to search
    # Null search is not allowed
    # Type is search or select
    def SearchData(Mode, SearchType):
        global SearchRowStart
        line_info(os.linesep.join(['SearchData', Mode, SearchType]))
        DataBox.selection_clear(0, DataBox.size())
        if Mode == 'main':
            DataToFind = SearchEntryMain.get()
        if Mode == 'batch':
            DataToFind = SearchEntryBatch.get()
        if len(DataToFind) < 1:
            return  # No null searches
        if CaseSearchVar.get():
            DataToFind = DataToFind.upper()

        if 'select' in SearchType:
            SearchRowStart = 0
        for x in range(SearchRowStart, DataBox.size()):
            Found = False
            DataToTest = DataBox.get(x)
            if CaseSearchVar.get():
                DataToTest = [x.upper() for x in DataToTest]
            if LeftSearchVar.get():
                if DataToFind in DataToTest[0]:
                    Found = True
            if RightSearchVar.get():
                if DataToFind in DataToTest[1]:
                    Found = True
            if StatusSearchVar.get():
                if DataToFind in DataToTest[2]:
                    Found = True
            if MoreSearchVar.get():
                if DataToFind in DataToTest[3]:
                    Found = True
            if Found:
                DataBox.selection_set(x)
                DataBox.see(x)
                if 'search' in SearchType:
                    SearchRowStart = x + 1
                    break
            # When the end of tha DataBox is reached, wrap around
            if x == DataBox.size() - 1:
                SearchRowStart = 0

# ------------------------------
    def ResetSearchData():
        global SearchRowStart
        line_info('ResetSearchData')
        DataBox.selection_clear(0, DataBox.size())
        DataBox.see(0)
        SearchRowStart = 0

# ------------------------------
# Quit the program
    def Quit():
        line_info('Quit')
        if tkinter.messagebox.askyesno('Quit', 'Really quit?'):
            Main.destroy()
            sys.exit(0)

# ------------------------------
    def GetType(FileName):
        line_info(' '.join(['GetType:', FileName]))
        tmp = ''
        if os.path.isfile(FileName):
            tmp = 'File, '
        if os.path.isdir(FileName):
            tmp += 'Dir, '
        if os.path.islink(FileName):
            tmp += 'Link, '
        if os.path.ismount(FileName):
            tmp += 'Mount, '
        if not os.access(FileName, os.W_OK):
            tmp += 'Read only, '
        return tmp

# ------------------------------
    def FetchDirectories(Trace):
        line_info(' '.join(['FetchDirectories:', Trace]))
        dir_opt = options = {}
        DoNotAskNumberOfFilesVar.set(False)
        if Trace == 'Both':
            DataBox.delete(0, tkinter.END)
            FileRenameTopLevelVar.withdraw()
            FileInfoTopLevelVar.withdraw()
            StatusVar.set('Fetch directories')

        if Trace == 'Left' or Trace == 'Both':
            options['title'] = 'Select left directory'
            options['initialdir'] = LeftPathEntry.get()
            New = tkinter.filedialog.askdirectory(**dir_opt)
            if len(New) > 0:
                UpdatePathEntry('Left', New)

        if Trace == 'Right' or Trace == 'Both':
            options['title'] = 'Select right directory'
            options['initialdir'] = RightPathEntry.get()
            New = tkinter.filedialog.askdirectory(**dir_opt)
            if len(New) > 0:
                UpdatePathEntry('Right', New)

# ------------------------------
    # Return a checksum for the FileName
    # Force overrides CheckSumAuto
    def GetCheckSum(FileName, Force=False):
        if not os.path.isfile(FileName):
            return 'Checksum not tested. Not a file.'
        if not CheckSumAutoVar.get() and not Force:
            return 'Checksum not auto-enabled.'
        if CheckSumTypeVar.get() == 1:  # crc32file
            return str(crc32file(FileName))
        elif CheckSumTypeVar.get() == 2:  # md5file
            return str(md5file(FileName))
        elif CheckSumTypeVar.get() == 3:  # sha1file
            return str(sha1file(FileName))
        else:
            tkinter.messagebox.showerror('GetCheckSum(FileName) error',
                                         os.linesep.join(['Invalid checksum type',
                                                          'Values from 1 to 3 are valid',
                                                          ProjectFileNameVar.get(),
                                                          str(CheckSumAutoVar.get()),
                                                          str(CheckSumTypeVar.get())]))
            raise SystemExit
            return 0

# ------------------------------
# This displays a splash screen. It is always centered in the main window
# It also enables/disables menu buttons as appropriate
    def SplashScreen(Message, Show):
        SplashTopLevelVar = tkinter.Toplevel(Main)
        if Show:  # Display the splashscreen and disable the button
            FetchDataButton.config(state=tkinter.DISABLED)
            # SplashTopLevelVar = tkinter.Toplevel(Main)
            SplashTopLevelVar.title(Message)

            Main.update()
            SplashTopLevelSizeX = 500
            SplashTopLevelSizeY = 200
            Mainsize = Main.geometry().split('+')
            x = int(Mainsize[1]) + SplashTopLevelSizeX / 2
            y = int(Mainsize[2]) + SplashTopLevelSizeY / 2
            SplashTopLevelVar.geometry("%dx%d+%d+%d" %
                                       (SplashTopLevelSizeX,
                                        SplashTopLevelSizeY,
                                        x,
                                        y))
            SplashTopLevelVar.resizable(1, 1)

            w = tkinter.Label(SplashTopLevelVar,
                              text=Message,
                              fg='yellow',
                              bg='blue',
                              font=("Helvetica",
                                    30))
            w.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
            SplashTopLevelVar.wm_transient(Main)
            Main.update()
        else:  # Destroy the splashscreen and enable the button
            SplashTopLevelVar.destroy()
            FetchDataButton.config(state=tkinter.NORMAL)

    # ------------------------------
    def FetchData():
        SplashScreen('FetchData is running', True)
        line_info('FetchData')

        DataBoxCurrentLine = re.sub("[^0-9]", "", str(DataBox.curselection()))
        DataBox.delete(0, tkinter.END)

        if not os.path.isdir(LeftPathEntry.get()):
            tkinter.messagebox.showerror('Left path does not exist',
                                         ''.join(['Left path error:',
                                                  os.linesep,
                                                  LeftPathEntry.get()]))
            StatusVar.set('Left path error')
            SplashScreen('FetchData is closing', False)
            return

        if not os.path.isdir(RightPathEntry.get()):
            tkinter.messagebox.showerror('Right path does not exist',
                                         os.linesep.join(['Right path error:',
                                                          RightPathEntry.get()]))
            StatusVar.set('Right path error')
            SplashScreen('FetchData is closing', False)
            return

        LeftNumberOfFiles = len([item for item in os.listdir(LeftPathEntry.get()) if os.path.isfile(os.path.join(LeftPathEntry.get(), item))])
        RightNumberOfFiles = len([item for item in os.listdir(RightPathEntry.get()) if os.path.isfile(os.path.join(RightPathEntry.get(), item))])
        ActualTotalFiles = ''.join([LeftNumberOfFiles, RightNumberOfFiles])
        line_info(' '.join(['Disable stuff:',
                            str(ActualTotalFiles),
                            str(TriggerNumberOfFilesVar.get())]))

        # Decide to disable autorefresh and/or checksum
        if (ActualTotalFiles > TriggerNumberOfFilesVar.get()) and not DoNotAskNumberOfFilesVar.get():
            DoNotAskNumberOfFilesVar.set(True)
            if AutoRefreshCheckVar.get():  # enabled
                if tkinter.messagebox.askyesno(' '.join([str(ActualTotalFiles),
                                                         'files to be processed']),
                                               'Disable autorefresh?'):
                    AutoRefreshCheckVar.set(False)
            if CheckSumAutoVar.get():  # enabled
                if tkinter.messagebox.askyesno(' '.join([str(ActualTotalFiles),
                                                         ' files to be processed']),
                                               'Disable checksum?'):
                    CheckSumAutoVar.set(False)

        StatusVar.set('Starting the compare')
        comparison = filecmp.dircmp(LeftPathEntry.get(), RightPathEntry.get())

        if ShowBothCheckVar.get():
            new = sorted(comparison.common)
            for name in new:
                if FilterEntry.get().upper() in name.upper():
                    LeftName = os.path.join(LeftPathEntry.get(), name)
                    RightName = os.path.join(RightPathEntry.get(), name)
                    CompareString = ''
                    CompareString += GetType(LeftName)
                    CompareString += GetType(RightName)

                    if not ShowDirectoriesCheckVar.get():  # Don't show directories
                        if 'Dir' in CompareString:
                            continue

                    if os.path.getsize(LeftName) != os.path.getsize(RightName):
                        CompareString += 'Size, '
                    # Check sum is tested only if CheckSumAutoVar is True and item is in both left and right
                    if CheckSumAutoVar.get() and GetCheckSum(LeftName) != GetCheckSum(RightName):
                        CompareString += 'CheckSum, '

                    TimeDiff = abs(os.path.getmtime(LeftName) - os.path.getmtime(RightName))
                    if TimeDiff < 1:
                        pass
                    elif TimeDiff > FileTimeTriggerScaleVar.get():
                        CompareString += 'TIME, '  # Big time difference
                    else:
                        CompareString += 'time, '  # Small time difference
                    DataBox.insert(tkinter.END,
                                   (name, name,
                                    'Both',
                                    CompareString))

        Dict = {}
        new1 = sorted(comparison.left_only)
        for s in new1:
            if (ShowLeftCheckVar.get()) and FilterEntry.get().upper() in s.upper():
                if os.path.isdir(os.path.join(LeftPathEntry.get(), s)):
                    if ShowDirectoriesCheckVar.get():
                        DataBox.insert(tkinter.END, (s, '', 'Left', 'Directory'))
                else:
                    DataBox.insert(tkinter.END, (s, '', 'Left', 'File'))
            if not s.upper() in Dict:
                Dict[s.upper()] = 0
            else:
                Dict[s.upper()] += 1

        new2 = sorted(comparison.right_only)
        for s in new2:
            if (ShowRightCheckVar.get()) and FilterEntry.get().upper() in s.upper():
                if os.path.isdir(os.path.join(RightPathEntry.get(), s)):
                    if ShowDirectoriesCheckVar.get():
                        DataBox.insert(tkinter.END, ('', s, 'Right', 'Directory'))
                else:
                    DataBox.insert(tkinter.END, ('', s, 'Right', 'File'))
            if not s.upper() in Dict:
                Dict[s.upper()] = 0
            else:
                Dict[s.upper()] += 1

        if ShowDiffCheckVar.get():
            for key, value in Dict.items():
                for s in new1:
                    if s.upper() == key and value > 0 and FilterEntry.get().upper() in s.upper():
                        DataBox.insert(tkinter.END, (s, '', 'Diff', 'Diff'))
                        line_info(' '.join(['Show diff new1: ', s]))
                for s in new2:
                    if s.upper() == key and value > 0 and FilterEntry.get().upper() in s.upper():
                        DataBox.insert(tkinter.END, ('', s, 'Diff', 'Diff'))
                        line_info(' '.join(['Show diff new2: ', s]))

        StatusVar.set(' '.join(['Compare complete. Items:',
                                str(DataBox.size() - 1)]))
        ShowLineNumberVar.set(' '.join(['No line selected of',
                                        str(DataBox.size() - 1)]))
        SplashScreen('FetchData is closing', False)

        try:
            DataBox.selection_set(DataBoxCurrentLine)
            DataBox.see(DataBoxCurrentLine)
        except Exception as e:
            line_info(str(e))
            DataBox.selection_set(0)
            DataBox.see(0)

        Main.update()

# ------------------------------
    def crc32file(filename):
        filedata = open(filename, 'rt').read()
        return binascii.crc32(bytearray(filedata, 'utf-8'))

# ------------------------------
    def md5file(filename, block_size=256 * 128):
        md5 = hashlib.md5()
        with open(filename, 'rt') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

# ------------------------------
    def sha1file(filename):
        sha1 = hashlib.sha1()
        f = open(filename, 'rb')
        try:
            sha1.update(f.read())
        except Exception as e:
            line_info(' '.join(['whoops', str(e)]))
        finally:
            f.close()
        return sha1.hexdigest()

# ------------------------------
    # All copying is done here (Both batch and individual).
    # Checks for status before and after copy
    # Check for user OK
    def CopyAFile(Trace, src, dst, IsBatch):
        if os.path.isdir(dst):
            dst = os.path.join(dst, "")
        line_info('Trace: % s SRC: % s DST: % s IsBatch: % d' % (Trace, src, dst, IsBatch))
        # errors = []
        if os.path.isdir(src):
            line_info(' '.join([src, ' is directory']))
            if tkinter.messagebox.askyesno(Trace, os.linesep.join(['Copy directory tree?',
                                                                   src,
                                                                   'to',
                                                                   dst])):
                try:
                    line_info(''.join([dst, os.path.basename(src)]))
                    shutil.copytree(src,
                                    ''.join([dst, os.path.basename(src)]),
                                    symlinks=False,
                                    ignore=None)
                except shutil.Error as e:
                    line_info('Directory not copied. Error: %s' % e)
                # Any error saying that the directory doesn't exist
                except OSError as e:
                    line_info('Directory not copied. Error: %s' % e)
                if AutoRefreshCheckVar.get() and not IsBatch:
                    FetchData()
            return

        if ConfirmCopyCheckVar.get():
            if not tkinter.messagebox.askyesno(Trace,
                                               os.linesep.join(['Copy',
                                                                src,
                                                                'to',
                                                                dst,
                                                                '?'])):
                line_info(os.linesep.join(['Copy aborted by user', src, 'to', dst]))
                return
        try:
            line_info(shutil.copy2(src, dst))
        except Exception as e:
            tkinter.messagebox.showerror(Trace,
                                         os.linesep.join(['Retry copy',
                                                          src,
                                                          'to',
                                                          dst,
                                                          str(e)]))
            line_info(os.linesep.join(['Copy failed',
                                       src,
                                       'to',
                                       dst,
                                       str(e)]))
            return

        if AutoRefreshCheckVar.get() and not IsBatch:
            FetchData()
        return

    def CopyLeft():
        src = os.path.join(LeftPathEntry.get(), FileLeftNameVar.get())
        dst = RightPathEntry.get()
        CopyAFile('CopyLeft', src, dst, False)

    def CopyRight():
        src = os.path.join(RightPathEntry.get(), FileRightNameVar.get())
        dst = LeftPathEntry.get()
        CopyAFile('CopyRight', src, dst, False)
        # ------------------------------

    # All deleting is done here (Both batch and individual).
    # Checks for status before and after delete
    # Check for user OK
    def DeleteAFile(file1, file2):
        if RecycleCheckVar.get() == 0:
            Message = 'Delete'
        else:
            Message = 'Recycle'

        line_info(' '.join(['DeleteAFile  left:',
                            file1,
                            '<< right:',
                            file2,
                            '<<',
                            Message]))
        Main.update_idletasks()
        if ConfirmDeleteCheckVar.get():
            if not tkinter.messagebox.askyesno(' '.join([Message, ' file(s)?']),
                                               file1,
                                               file2):
                line_info(os.linesep.join([Message, 'aborted', file1, file2]))
                return

        if RecycleCheckVar.get() == 0:
            line_info('os.remove')
            RemoveAFile(file1, Trash=False)
            RemoveAFile(file2, Trash=False)
            # if os.path.exists(file1): os.remove(file1)
            # if os.path.exists(file2): os.remove(file2)
        else:
            if os.path.exists(file1):
                # send2trash(file1)
                RemoveAFile(file1, Trash=True)
                if os.path.exists(file1):  # This tests to see if the operation worked
                    if tkinter.messagebox.showerror(' '.join([Message, 'failed']), file1):
                        line_info(' '.join([Message, 'failed', file1]))
            if os.path.exists(file2):
                # send2trash(file2)
                RemoveAFile(file2, Trash=True)
                if os.path.exists(file2):  # This tests to see if the operation worked
                    tm = ' '.join([Message, 'failed'])
                    if tkinter.messagebox.showerror(tm, file2):
                        line_info(' '.join([Message, 'failed', file2]), True)

        if AutoRefreshCheckVar.get():
            FetchData()
        else:
            StatusVar.set('Refresh needed')

    def DeleteBoth():
        file1 = os.path.join(LeftPathEntry.get(), FileLeftNameVar.get())
        file2 = os.path.join(RightPathEntry.get(), FileRightNameVar.get())
        DeleteAFile(file1, file2)

    def DeleteLeft():
        file = os.path.join(LeftPathEntry.get(), FileLeftNameVar.get())
        DeleteAFile(file, '')

    def DeleteRight():
        file = os.path.join(RightPathEntry.get(), FileRightNameVar.get())
        DeleteAFile('', file)

# ------------------------------
# This class handles file rename for the file info menu
    class FileRename:
        RenameEntry = None
        Trace = 'Bullpoo'

        def FileRenameBoth(self):
            line_info('')
            if len(FileLeftNameVar.get()) > 0 and len(FileRightNameVar.get()) > 0:
                self.Trace = 'Both'
                self.RenameAFile()

        def FileRenameRight(self):
            if len(FileRightNameVar.get()) > 0:
                self.Trace = 'Right'
                self.RenameAFile()

        def FileRenameLeft(self):
            if len(FileLeftNameVar.get()) > 0:
                self.Trace = 'Left'
                self.RenameAFile()

    # ------------------------------
        def Swapcase(self):
            filename = self.RenameEntry.get()
            self.RenameEntry.delete(0, tkinter.END)
            self.RenameEntry.insert(0, filename.swapcase())

        def Titlecase(self):
            '''
            return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                            ''.join([lambda mo: mo.group(0)[0].upper(),
                                    mo.group(0)[1:].lower(),
                                    s]))
            '''
            filename = self.RenameEntry.get()
            self.RenameEntry.delete(0, tkinter.END)
            # self.RenameEntry.insert(0, titlecase(filename))
            self.RenameEntry.insert(0, filename.title())

        def Uppercase(self):
            filename = self.RenameEntry.get()
            self.RenameEntry.delete(0, tkinter.END)
            self.RenameEntry.insert(0, filename.upper())
            self.RenameEntry.focus_set()

        def Lowercase(self):
            filename = self.RenameEntry.get()
            self.RenameEntry.delete(0, tkinter.END)
            self.RenameEntry.insert(0, filename.lower())
            self.RenameEntry.focus_set()

        def Capitalize(self):
            filename = self.RenameEntry.get()
            self.RenameEntry.delete(0, tkinter.END)
            self.RenameEntry.insert(0, filename.capitalize())
            self.RenameEntry.focus_set()

        def Done(self):  # Filename will always be the same
            filenameL = FileLeftNameVar.get()
            filenameR = FileRightNameVar.get()
            filepathL = LeftPathEntry.get()
            filepathR = RightPathEntry.get()
            try:
                if self.Trace == 'Both':
                    os.rename(os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    self.RenameTest(os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    os.rename(os.path.join(filepathR, filenameR), os.path.join(filepathR, self.RenameEntry.get()))
                    self.RenameTest('Both Right', os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    line_info('os.rename both')
                elif self.Trace == 'Left':
                    os.rename(os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    self.RenameTest(os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    line_info('os.rename left')
                elif self.Trace == 'Right':
                    os.rename(os.path.join(filepathR, filenameR), os.path.join(filepathR, self.RenameEntry.get()))
                    self.RenameTest(os.path.join(filepathL, filenameL), os.path.join(filepathL, self.RenameEntry.get()))
                    line_info('os.rename right')
                else:
                    line_info('OPPS. Bad trace value ' + self.Trace)
            except Exception as e:
                line_info('*********************************')
                tkinter.messagebox.showerror('Rename error',
                                             os.linesep.join(['Source file does not exist',
                                                              'Refresh needed',
                                                              str(e)]))

            FileRenameTopLevelVar.withdraw()
            if AutoRefreshCheckVar.get():
                FetchData()

        # If the two names are the same then the rename succeeded
        def RenameTest(self, left, right):
            if left == right:
                line_info('os.rename test: ' + self.Trace + ' FAIL ')
            else:
                line_info('os.rename test: ' + self.Trace + ' PASS ')

        def Cancel(self):
            FileRenameTopLevelVar.withdraw()

        StatusVar.set('Refresh needed (Fetch Data)')

        def RenameAFile(self):
            FileRenameTopLevelVar = tkinter.Toplevel()
            FileRenameTopLevelVar.title(self.Trace + ' file rename')
            FileRenameTopLevelVar.resizable(0, 0)

            Main.update()
            FileRenameTopLevelSizeX = 460
            FileRenameTopLevelSizeY = 110
            Mainsize = Main.geometry().split('+')
            x = int(Mainsize[1]) + FileRenameTopLevelSizeX / 2
            y = int(Mainsize[2]) + FileRenameTopLevelSizeY / 2
            FileRenameTopLevelVar.geometry("%dx%d+%d+%d" % (FileRenameTopLevelSizeX, FileRenameTopLevelSizeY, x, y))
            FileRenameTopLevelVar.resizable(1, 1)

            FileRenameFrame1 = tkinter.Frame(FileRenameTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileRenameFrame1.pack(side=tkinter.TOP)
            FileRenameFrame2 = tkinter.Frame(FileRenameTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileRenameFrame2.pack(side=tkinter.TOP)
            FileRenameFrame3 = tkinter.Frame(FileRenameTopLevelVar, relief=tkinter.SUNKEN, bd=1)

            if self.Trace == 'Both':
                filename = FileRightNameVar.get()
            elif self.Trace == 'Left':
                filename = FileLeftNameVar.get()
            elif self.Trace == 'Right':
                filename = FileRightNameVar.get()
            else:
                line_info('OPPS. Bad trace value')

            tkinter.Label(FileRenameFrame1, text=filename).pack()
            self.RenameEntry = tkinter.Entry(FileRenameFrame1, width=50)
            self.RenameEntry.pack()
            self.RenameEntry.delete(0, tkinter.END)
            self.RenameEntry.insert(0, filename)
            self.RenameEntry.focus_set()

            FileRenameFrame3.pack(side=tkinter.TOP)
            tkinter.Button(FileRenameFrame2, text='Done', width=12, command=self.Done).pack(side=tkinter.LEFT)
            tkinter.Button(FileRenameFrame2, text='Cancel', width=12, command=self.Cancel).pack(side=tkinter.LEFT)
            tkinter.Button(FileRenameFrame2, text='Title', width=12, command=self.Titlecase).pack(side=tkinter.LEFT)

            tkinter.Button(FileRenameFrame3, text='Upper', width=12, command=self.Uppercase).pack(side=tkinter.LEFT)
            tkinter.Button(FileRenameFrame3, text='Lower', width=12, command=self.Lowercase).pack(side=tkinter.LEFT)
            tkinter.Button(FileRenameFrame3, text='Swap', width=12, command=self.Swapcase).pack(side=tkinter.LEFT)
            tkinter.Button(FileRenameFrame3, text='Capitalize', width=12, command=self.Capitalize).pack(side=tkinter.LEFT)

# ------------------------------
# TODO 'This does not work for linux'
    def LocateFile(path):
        line_info(path)
        subprocess.call([SystemLocaterVar.get(), path])

    def LocateRight():
        path = str(RightPathEntry.get())
        LocateFile(path)

    def LocateLeft():
        path = str(LeftPathEntry.get())
        LocateFile(path)

    def LocateBoth():
        LocateLeft()
        LocateRight()

# This works when both exist
    def DiffBoth():
        line_info()
        Left = os.path.join(LeftPathEntry.get(), FileLeftNameVar.get())
        Right = os.path.join(RightPathEntry.get(), FileRightNameVar.get())
        StartFile(SystemDifferVar.get(), Left, Right)

# ------------------------------
    class FileInfo:
        LeftButtons = True
        RightButtons = True

        BothDeleteButton = None
        BothDiffButton = None
        BothCheckSUMButton = None
        LeftCopyButton = None
        LeftDeleteButton = None
        RightCopyButton = None
        RightDeleteButton = None
        LeftCheckSumButton = None
        RightCheckSumButton = None

        LeftPathAndNameVar = tkinter.StringVar()
        RightPathAndNameVar = tkinter.StringVar()
        RowInfoVar = tkinter.StringVar()
        FileStatusVar = tkinter.StringVar()
        TypeStatusVar = tkinter.StringVar()
        SizeStatusVar = tkinter.StringVar()
        TimeStatusVar = tkinter.StringVar()
        CheckSumStatusVar = tkinter.StringVar()
        StatType = None
        StatSize = None
        StatTime = None
        StatCheckSum = None
        FileLeftTypeVar = tkinter.StringVar()
        FileRightTypeVar = tkinter.StringVar()
        FileLeftSizeVar = tkinter.StringVar()
        FileRightSizeVar = tkinter.StringVar()
        FileRightTimeVar = tkinter.StringVar()
        FileLeftTimeVar = tkinter.StringVar()
        FileLeftCheckSumVar = tkinter.StringVar()
        FileRightCheckSumVar = tkinter.StringVar()
        FileInfoBGColor = tkinter.StringVar()

        def ClearInfoForm(self):
            FileLeftNameVar.set('')
            FileRightNameVar.set('')
            self.FileLeftTypeVar.set('')
            self.FileRightTypeVar.set('')
            self.FileLeftTimeVar.set('')
            self.FileRightTimeVar.set('')
            self.FileLeftSizeVar.set('')
            self.FileRightSizeVar.set('')
            self.FileLeftCheckSumVar.set('')
            self.FileRightCheckSumVar.set('')
            self.TypeStatusVar.set('')
            self.TimeStatusVar.set('')
            self.SizeStatusVar.set('')
            self.CheckSumStatusVar.set('')

            self.StatType.config(bg=self.FileInfoBGColor.get())
            self.StatTime.config(bg=self.FileInfoBGColor.get())
            self.StatSize.config(bg=self.FileInfoBGColor.get())
            self.StatCheckSum.config(bg=self.FileInfoBGColor.get())
            self.RowInfoVar.set('')
            self.FileStatusVar.set('')

        def UpdateCheckSumStatus(self):
            # The following updates the checksum status bar
            if self.FileLeftCheckSumVar.get().find('Checksum') > -1 and \
               self.FileRightCheckSumVar.get().find('Checksum') > -1:
                self.StatCheckSum.config(bg='yellow')
                self.CheckSumStatusVar.set('Checksum not tested')
            else:
                if self.FileLeftCheckSumVar.get() == 'Checksum not tested' or \
                        self.FileLeftCheckSumVar.get() == 'Checksum not tested':
                    self.CheckSumStatusVar.set('Checksums not tested')
                    self.StatCheckSum.config(bg='grey')
                elif self.FileLeftCheckSumVar.get() != self.FileRightCheckSumVar.get():
                    self.CheckSumStatusVar.set('Checksums are different')
                    self.StatCheckSum.config(bg='red')
                else:
                    self.CheckSumStatusVar.set('Checksums are the same')
                    self.StatCheckSum.config(bg='green')

        # This builds the file information form
        def BuildFileInfoForm(self):
            def FileInfoXButton():
                line_info()
                FileInfoTopLevelVar.withdraw()

            FileInfoTopLevelVar = tkinter.Toplevel()
            # FileInfoTopLevelVar.overrideredirect(1)
            FileInfoTopLevelVar.title('File information')
            FileInfoTopLevelVar.resizable(1, 1)
            FileInfoTopLevelVar.wm_transient(Main)
            FileInfoTopLevelVar.protocol('WM_DELETE_WINDOW', FileInfoXButton)

            FileInfoFrame1 = tkinter.Frame(FileInfoTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileInfoFrame1.pack(side=tkinter.TOP, fill=tkinter.X)
            FileInfoFrame2 = tkinter.Frame(FileInfoTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileInfoFrame2.pack(side=tkinter.TOP, fill=tkinter.X)
            FileInfoFrame3 = tkinter.Frame(FileInfoTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileInfoFrame3.pack(side=tkinter.TOP, fill=tkinter.X)
            FileInfoFrame4 = tkinter.Frame(FileInfoTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileInfoFrame4.pack(side=tkinter.TOP, fill=tkinter.X)
            FileInfoFrame5 = tkinter.Frame(FileInfoTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            FileInfoFrame5.pack(side=tkinter.TOP, fill=tkinter.X)

            # These are the definitions for the top frame (status)
            tkinter.Label(FileInfoFrame1, textvariable=self.FileStatusVar).pack(fill=tkinter.X)
            self.RowInfoLabel = tkinter.Label(FileInfoFrame1, textvariable=self.RowInfoVar)
            self.RowInfoLabel.pack(fill=tkinter.X)
            ToolTip(self.RowInfoLabel, 'Selected row(s) and total rows in data')

            self.StatType = tkinter.Label(FileInfoFrame1, textvariable=self.TypeStatusVar)
            self.StatType.pack(fill=tkinter.X)
            ToolTip(self.StatType, text='Dir or file and read only status (both)')

            # The next line saves the defaut BG color so it can be restored to various items later
            self.FileInfoBGColor.set(self.StatType.cget('bg'))

            # Status labels for type, size, time/date, amd checksum
            self.StatSize = tkinter.Label(FileInfoFrame1, textvariable=self.SizeStatusVar)
            self.StatSize.pack(fill=tkinter.X)
            ToolTip(self.StatSize, text='File size status (both)')
            self.StatTime = tkinter.Label(FileInfoFrame1, textvariable=self.TimeStatusVar)
            self.StatTime.pack(fill=tkinter.X)
            ToolTip(self.StatTime, text='File date and time status (both)')
            self.StatCheckSum = tkinter.Label(FileInfoFrame1, textvariable=self.CheckSumStatusVar)
            self.StatCheckSum.pack(fill=tkinter.X)
            ToolTip(self.StatCheckSum, text='File checksum status (both)')

            # Now define the buttons for frame 1 in the ButtonFrame
            ButtonFrame = tkinter.Frame(FileInfoFrame1, relief=tkinter.SUNKEN, bd=1)
            ButtonFrame.pack(fill=tkinter.X)
            self.BothDeleteButton = tkinter.Button(ButtonFrame, text='Delete', width=8, command=DeleteBoth)
            self.BothDeleteButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.BothDeleteButton, text='Delete both left and right selected items')
            self.BothDiffButton = tkinter.Button(ButtonFrame, text='Diff', width=10, command=DiffBoth)
            self.BothDiffButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.BothDiffButton, text='Call an external difference program to compare the selected files/directories')

            def BothCheckSUM():
                self.FileLeftCheckSumVar.set(GetCheckSum(self.LeftPathAndNameVar.get(), True))
                self.FileRightCheckSumVar.set(GetCheckSum(self.RightPathAndNameVar.get(), True))
                self.UpdateCheckSumStatus()
            self.BothCheckSUMButton = tkinter.Button(ButtonFrame, text='CheckSUM', width=8, command=BothCheckSUM)
            self.BothCheckSUMButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.BothCheckSUMButton, text='Compute checksums for both files')

            def ChangeDir():
                LeftPathEntry.delete(0, tkinter.END)
                RightPathEntry.delete(0, tkinter.END)
                UpdatePathEntry('Left', self.LeftPathAndNameVar.get())
                UpdatePathEntry('Right', self.RightPathAndNameVar.get())
                if AutoRefreshCheckVar.get():
                    FetchData()
                else:
                    StatusVar.set('Refresh needed')

            self.BothChangeDirButton = tkinter.Button(ButtonFrame, text='Change Dir', width=16, command=ChangeDir)
            self.BothChangeDirButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.BothChangeDirButton, text='Change to the selected directories')

            # The definitions for Left begin here
            tkinter.Label(FileInfoFrame2, text='Left information', fg='blue').pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame2, textvariable=FileLeftNameVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame2, textvariable=self.FileLeftTypeVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame2, textvariable=self.FileLeftSizeVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame2, textvariable=self.FileLeftTimeVar).pack(fill=tkinter.X)

            def LeftCheckSum():
                self.FileLeftCheckSumVar.set(GetCheckSum(self.LeftPathAndNameVar.get(), True))
                self.UpdateCheckSumStatus()
            self.LeftCheckSumButton = tkinter.Button(FileInfoFrame2, textvariable=self.FileLeftCheckSumVar, command=LeftCheckSum)
            self.LeftCheckSumButton.pack(fill=tkinter.X)
            ToolTip(self.LeftCheckSumButton, 'Compute left checksum')
            self.LeftCopyButton = tkinter.Button(FileInfoFrame3, text='Copy', command=CopyLeft, width=10, state=tkinter.DISABLED)
            self.LeftCopyButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.LeftCopyButton, 'Copy left side item to the right side')
            self.LeftDeleteButton = tkinter.Button(FileInfoFrame3, text='Delete', command=DeleteLeft, width=10, state=tkinter.DISABLED)
            self.LeftDeleteButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.LeftDeleteButton, 'Delete the left side item')

            # The following section creates the rename toplevel instance
            FileRenameInstance = FileRename()

            self.LeftRenameButton = tkinter.Button(FileInfoFrame3, text='Rename', command=FileRenameInstance.FileRenameLeft, width=10, state=tkinter.DISABLED)
            self.LeftRenameButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.LeftRenameButton, 'Rename the left side item')
            self.LeftLocateButton = tkinter.Button(FileInfoFrame3, text='Locate', command=LocateLeft, width=10, state=tkinter.DISABLED)
            self.LeftLocateButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.LeftLocateButton, 'Open the directoty containing the left side item')

            self.RightCopyButton = tkinter.Button(FileInfoFrame5, text='Copy', command=CopyRight, width=10, state=tkinter.DISABLED)
            self.RightCopyButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.RightCopyButton, 'Copy right side item to the left side')
            self.RightDeleteButton = tkinter.Button(FileInfoFrame5, text='Delete', command=DeleteRight, width=10, state=tkinter.DISABLED)
            self.RightDeleteButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.RightDeleteButton, 'Delete the right side item')
            self.RightRenameButton = tkinter.Button(FileInfoFrame5, text='Rename', command=FileRenameInstance.FileRenameRight, width=10, state=tkinter.DISABLED)
            ToolTip(self.RightRenameButton, 'Rename the right side item')
            self.RightRenameButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            self.RightLocateButton = tkinter.Button(FileInfoFrame5, text='Locate', command=LocateRight, width=10, state=tkinter.DISABLED)
            self.RightLocateButton.pack(side=tkinter.LEFT, fill=tkinter.X)
            ToolTip(self.RightLocateButton, 'Open the directory containing the right side item')

            # The definitions for Right begin here
            tkinter.Label(FileInfoFrame4, text='Right information', fg='blue').pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame4, textvariable=FileRightNameVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame4, textvariable=self.FileRightTypeVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame4, textvariable=self.FileRightSizeVar).pack(fill=tkinter.X)
            tkinter.Label(FileInfoFrame4, textvariable=self.FileRightTimeVar).pack(fill=tkinter.X)

            def RightCheckSum():
                self.FileRightCheckSumVar.set(GetCheckSum(self.RightPathAndNameVar.get(), True))
                self.UpdateCheckSumStatus()
            self.RightCheckSumButton = tkinter.Button(FileInfoFrame4, textvariable=self.FileRightCheckSumVar, command=RightCheckSum)
            ToolTip(self.RightCheckSumButton, 'Compute right checksum')
            self.RightCheckSumButton.pack(fill=tkinter.X)
            FileInfoTopLevelVar.withdraw()

        def ShowFileInfo(self):
            self.ClearInfoForm()
            FileInfoTopLevelVar.deiconify()
            FileInfoTopLevelVar.wm_transient(Main)
            FileInfoTopLevelX = 400
            FileInfoTopLevelY = 510
            Mainsize = Main.geometry().split('+')
            x = int(Mainsize[1]) + (FileInfoTopLevelX / 2)
            y = int(Mainsize[2]) + (FileInfoTopLevelX / 2)

            FileInfoTopLevelVar.geometry("%dx%d+%d+%d" % (FileInfoTopLevelX, FileInfoTopLevelY, x, y))
            FileInfoTopLevelVar.resizable(1, 1)

            line_info('ShowFileInfoForm')
            if DataBox.size() < 0:
                tkinter.messagebox.showerror('Data box error', 'Databox is empty')
                return

            if not DataBox.curselection():
                tkinter.messagebox.showerror('Data box error', 'Nothing is selected')
                return

            self.RowInfoVar.set('Row ' + str(DataBox.curselection()[0]) + ' of ' + str(DataBox.size() - 1))
            t = DataBox.curselection()

            FileLeftNameVar.set(DataBox.get(t)[0])
            FileRightNameVar.set(DataBox.get(t)[1])

            if len(FileLeftNameVar.get()) > 0:
                self.LeftPathAndNameVar.set(os.path.join(LeftPathEntry.get(), FileLeftNameVar.get()))
            else:
                self.LeftPathAndNameVar.set('')
            if len(FileRightNameVar.get()) > 0:
                self.RightPathAndNameVar.set(os.path.join(RightPathEntry.get(), FileRightNameVar.get()))
            else:
                self.RightPathAndNameVar.set('')

            FileInfoTopLevelVar.deiconify()
            FileInfoTopLevelVar.lift()

            # Enable or disable button depending on file/directory status and location
            # Disable all 'both' buttons by default
            self.BothDeleteButton.config(state=tkinter.DISABLED)
            self.BothDiffButton.config(state=tkinter.DISABLED)
            self.BothCheckSUMButton.config(state=tkinter.DISABLED)
            self.BothChangeDirButton.config(state=tkinter.DISABLED)

            if len(FileLeftNameVar.get()) == 0:  # left file/directory does not exist
                self.FileLeftSizeVar.set('No left file')
                self.LeftCopyButton.config(state=tkinter.DISABLED)
                self.LeftDeleteButton.config(state=tkinter.DISABLED)
                self.LeftRenameButton.config(state=tkinter.DISABLED)
                self.LeftLocateButton.config(state=tkinter.DISABLED)
                self.LeftCheckSumButton.config(state=tkinter.DISABLED)
            else:  # left file/directory does exist
                self.statinfoLeft = os.stat(self.LeftPathAndNameVar.get())
                self.FileLeftTypeVar.set(GetType(self.LeftPathAndNameVar.get()))
                self.FileLeftSizeVar.set('File size: {:,}'.format(self.statinfoLeft.st_size))
                self.FileLeftTimeVar.set('Modified:  %s' % time.ctime(self.statinfoLeft.st_mtime))
                self.FileLeftCheckSumVar.set(str(GetCheckSum(self.LeftPathAndNameVar.get())))
                self.LeftCopyButton.config(state=tkinter.NORMAL)
                self.LeftDeleteButton.config(state=tkinter.NORMAL)
                self.LeftRenameButton.config(state=tkinter.NORMAL)
                self.LeftLocateButton.config(state=tkinter.NORMAL)
                self.LeftCheckSumButton.config(state=tkinter.NORMAL)

            if len(FileRightNameVar.get()) == 0:  # right file/directory does not exist
                self.FileRightSizeVar.set('No right file')
                self.RightCopyButton.config(state=tkinter.DISABLED)
                self.RightDeleteButton.config(state=tkinter.DISABLED)
                self.RightRenameButton.config(state=tkinter.DISABLED)
                self.RightLocateButton.config(state=tkinter.DISABLED)
                self.RightCheckSumButton.config(state=tkinter.DISABLED)
            else:  # right file/directory does exist
                self.statinfoRight = os.stat(self.RightPathAndNameVar.get())
                self.FileRightTypeVar.set(GetType(self.RightPathAndNameVar.get()))
                self.FileRightSizeVar.set('File Size: {:,}'.format(self.statinfoRight.st_size))
                self.FileRightTimeVar.set('Modified:  %s' % time.ctime(self.statinfoRight.st_mtime))
                self.FileRightCheckSumVar.set(str(GetCheckSum(self.RightPathAndNameVar.get())))
                self.RightCopyButton.config(state=tkinter.NORMAL)
                self.RightDeleteButton.config(state=tkinter.NORMAL)
                self.RightRenameButton.config(state=tkinter.NORMAL)
                self.RightLocateButton.config(state=tkinter.NORMAL)
                self.RightCheckSumButton.config(state=tkinter.NORMAL)

            # If both sides exist and they are the same type enable 'BothDeleteButton' and 'BothDiffButton' buttons
            if os.path.exists(self.LeftPathAndNameVar.get()) and \
               os.path.exists(self.RightPathAndNameVar.get()) and \
               self.FileLeftTypeVar.get() == self.FileRightTypeVar.get():
                self.BothDeleteButton.config(state=tkinter.NORMAL)
                self.BothDiffButton.config(state=tkinter.NORMAL)

            # If both sides exist and are not directories enable 'BothCheckSUMButton' buttons
            if os.path.isfile(self.LeftPathAndNameVar.get()) and \
               os.path.isfile(self.RightPathAndNameVar.get()):
                self.BothCheckSUMButton.config(state=tkinter.NORMAL)

            # If both sides exist and both are directories enable 'Change Dir' button
            if os.path.isdir(self.LeftPathAndNameVar.get()) and \
               os.path.isdir(self.RightPathAndNameVar.get()):
                self.BothChangeDirButton.config(state=tkinter.NORMAL)

            # Display the size, time and checksum status
            if len(FileRightNameVar.get()) > 0 and len(FileLeftNameVar.get()) > 0:
                if os.path.getsize(self.LeftPathAndNameVar.get()) != os.path.getsize(self.RightPathAndNameVar.get()):
                    self.SizeStatusVar.set('Sizes are different')
                    self.StatSize.config(bg='red')
                else:
                    self.SizeStatusVar.set('Sizes are the same')
                    self.StatSize.config(bg='green')

                self.UpdateCheckSumStatus()

                if self.FileLeftTypeVar.get() != self.FileRightTypeVar.get():
                    self.TypeStatusVar.set('Types are different')
                    self.StatType.config(bg='red')
                else:
                    self.TypeStatusVar.set('Types are the same')
                    self.StatType.config(bg='green')

                TimeDiff = abs(os.path.getmtime(self.LeftPathAndNameVar.get()) - os.path.getmtime(self.RightPathAndNameVar.get()))
                if TimeDiff < 1:
                    self.TimeStatusVar.set('Times are the same')
                    self.StatTime.config(bg='green')
                elif TimeDiff > FileTimeTriggerScaleVar.get():
                    self.TimeStatusVar.set('Times are different')
                    self.StatTime.config(bg='red')
                else:
                    self.TimeStatusVar.set('Times are close')
                    self.StatTime.config(bg='yellow')

            self.FileStatusVar.set('Status: ' + DataBox.get(t)[2])

            return 0

# ------------------------------
    # Loads a project file
    # Lines without a ~ in the line are ignored and may be used as comments
    # Lines with # in position 0 may be used as comments
    def ProjectLoad(LoadType='none'):
        global CommentsListVar
        line_info(' '.join(['ProjectLoad', LoadType]))
        if LoadType == 'default':
            ProjectFileNameVar.set(os.path.join(StartUpDirectoryVar.get(), 'PyDiffTk.' + ProjectFileExtensionVar.get()))
        else:
            ProjectFileNameVar.set(tkinter.filedialog.askopenfilename(
                                   defaultextension=ProjectFileExtensionVar.get(),
                                   filetypes=[('Project file', ''.join(['DougPyDiff*.',
                                                                        ProjectFileExtensionVar.get()]),
                                              ('All files', '*.*'))],
                                   initialdir=os.path.dirname(StartUpDirectoryVar.get()),
                                   initialfile=''.join(['PyDiffTk.',
                                                        ProjectFileExtensionVar.get()]),
                                   title='Load a PyDiffTk project file',
                                   parent=Main))
        line_info(''.join(['Project Load', ProjectFileNameVar.get()]))

        ProjectEntry.delete(0, tkinter.END)
        ProjectEntry.insert(0, ProjectFileNameVar.get())

        try:
            f = open(ProjectFileNameVar.get(), 'r')
        except IOError as e:
            error_message = os.linesep.join(['Requested file does not exist.',
                                             ProjectFileNameVar.get(),
                                             str(e)])
            line_info(error_message)
            tkinter.messagebox.showerror('Project file error', error_message)
            return

        lines = f.readlines()
        f.close()

        tmp = 'PyDiffTk.py project file ' + sys.platform
        if tmp not in lines[0]:
            error_message = os.linesep.join(['Not a valid project file.', lines[0]])
            line_info(error_message)
            tkinter.messagebox.showerror('Project file error', error_message)
            return

        del lines[0]  # remove the first line so it won't be added to the comments list
        # Clear any widgets that need to be
        CommentsListVar = []
        for line in lines:
            if '~' in line and line[0] != '#':
                t = line.split('~')
                if 'False' in t[1]:
                    t[1] = 0
                elif 'True' in t[1]:
                    t[1] = 1
                if 'LeftPathEntry' in line:
                    x = os.path.normpath(t[1].strip())
                    UpdatePathEntry('Left', x)
                if 'RightPathEntry' in line:
                    x = os.path.normpath(t[1].strip())
                    UpdatePathEntry('Right', x)
                if 'FilterEntry' in line:
                    FilterEntry.delete(0, tkinter.END)
                    FilterEntry.insert(0, t[1].strip())
                if 'SearchEntryBatch' in line:
                    # SearchEntryBatch.delete(0, tkinter.END)
                    # SearchEntryBatch.insert(0, t[1].strip())
                    pass
                if 'SearchEntryMain' in line:
                    SearchEntryMain.delete(0, tkinter.END)
                    SearchEntryMain.insert(0, t[1].strip())
# TODO
                if 'LeftSearchVar' in line:
                    LeftSearchVar.set(int(t[1]))
                if 'RightSearchVar' in line:
                    RightSearchVar.set(int(t[1]))
                if 'StatusSearchVar' in line:
                    StatusSearchVar.set(int(t[1]))
                if 'MoreSearchVar' in line:
                    MoreSearchVar.set(int(t[1]))
                if 'CaseSearchVar' in line:
                    CaseSearchVar.set(int(t[1]))
                if 'SystemEditorVar' in line and len(t[1]) > 1:
                    SystemEditorVar.set(t[1].strip())
                if 'SystemDifferVar' in line and len(t[1]) > 1:
                    SystemDifferVar.set(t[1].strip())
                if 'SystemRenamerVar' in line and len(t[1]) > 1:
                    SystemRenamerVar.set(t[1].strip())
                if 'SystemLocaterVar' in line and len(t[1]) > 1:
                    SystemLocaterVar.set(t[1].strip())
                if 'ShowLeftCheckVar' in line:
                    ShowLeftCheckVar.set(int(t[1]))
                if 'ShowRightCheckVar' in line:
                    ShowRightCheckVar.set(int(t[1]))
                if 'ShowBothCheckVar' in line:
                    ShowBothCheckVar.set(int(t[1]))
                if 'ShowDiffCheckVar' in line:
                    ShowDiffCheckVar.set(int(t[1]))
                if 'ShowDirectoriesCheckVar' in line:
                    ShowDirectoriesCheckVar.set(int(t[1]))
                if 'AutoRefreshCheckVar' in line:
                    AutoRefreshCheckVar.set(int(t[1]))
                if 'ConfirmCopyCheckVar' in line:
                    ConfirmCopyCheckVar.set(int(t[1]))
                if 'ConfirmDeleteCheckVar' in line:
                    ConfirmDeleteCheckVar.set(int(t[1]))
                if 'ConfirmRenameCheckVar' in line:
                    ConfirmRenameCheckVar.set(int(t[1]))
                if 'RecycleCheckVar' in line:
                    RecycleCheckVar.set(int(t[1]))
                if 'CheckSumAutoVar' in line:
                    CheckSumAutoVar.set(int(t[1]))
                if 'CheckSumTypeVar' in line:
                    CheckSumTypeVar.set(int(t[1]))
                if 'FileTimeTriggerScaleVar~' in line:
                    FileTimeTriggerScaleVar.set(int(t[1]))
                if 'TriggerNumberOfFilesVar~' in line:
                    TriggerNumberOfFilesVar.set(int(t[1]))
            else:
                # All lines with # in the first column are comments
                # All line that do not contain ~ are comments
                CommentsListVar.append(line)

        if not SearchPath(SystemEditorVar.get()):
            line_info(os.linesep.join(['File does not exist:',
                                       SystemEditorVar.get()]), True)
        if not SearchPath(SystemDifferVar.get()):
            line_info(os.linesep.join(['File does not exist:',
                                       SystemDifferVar.get()]), True)
        if not SearchPath(SystemRenamerVar.get()):
            line_info(os.linesep.join(['File does not exist:',
                                       SystemRenamerVar.get()]), True)
        if not SearchPath(SystemLocaterVar.get()):
            line_info(os.linesep.join(['File does not exist:',
                                       SystemLocaterVar.get()]), True)

        line_info(''.join(['Project opened: ', ProjectFileNameVar.get()]))
        if AutoRefreshCheckVar.get():
            FetchData()

# ------------------------------
# Saves a project file
    def ProjectSave():
        global CommentsListVar
        line_info(ProjectFileNameVar.get())

        ProjectFileNameVar.set(tkinter.filedialog.asksaveasfilename(
            defaultextension=ProjectFileExtensionVar.get(),
            filetypes=[('Project file', ''.join(['PyDiff*.', ProjectFileExtensionVar.get()])),
                       ('All files', '*.*')],
            initialdir=os.path.dirname(StartUpDirectoryVar.get()),
            initialfile=''.join(['PyDiffTk.', ProjectFileExtensionVar.get()]),
            title='Save a PyDiffTk project file',
            parent=Main))

        ProjectEntry.delete(0, tkinter.END)
        ProjectEntry.insert(0, ProjectFileNameVar.get())

        try:
            f = open(ProjectFileNameVar.get(), 'w')
        except IOError:
            tkinter.messagebox.showerror('Project file error',
                                         os.linesep.join(['Requested file does not exist.',
                                                          ProjectFileNameVar.get()]))
            return

        f.write(''.join(['PyDiffTk.py project file', sys.platform, os.linesep]))
        for item in CommentsListVar:
            f.write(item)
        f.write(''.join(['LeftPathEntry~', LeftPathEntry.get().strip(), os.linesep]))
        f.write(''.join(['RightPathEntry~', RightPathEntry.get().strip(), os.linesep]))
        f.write(''.join(['FilterEntry~', FilterEntry.get().strip(), os.linesep]))
        f.write(''.join(['SearchEntryMain~', SearchEntryMain.get().strip(), os.linesep]))
        f.write(''.join(['SearchEntryBatch~', SearchEntryBatch.get().strip(), os.linesep]))
        f.write(''.join(['LeftSearchVar~', str(LeftSearchVar.get()), os.linesep]))
        f.write(''.join(['RightSearchVar~', str(RightSearchVar.get()), os.linesep]))
        f.write(''.join(['StatusSearchVar~', str(StatusSearchVar.get()), os.linesep]))
        f.write(''.join(['MoreSearchVar~', str(MoreSearchVar.get()), os.linesep]))
        f.write(''.join(['CaseSearchVar~', str(CaseSearchVar.get()), os.linesep]))
        f.write(''.join(['SystemEditorVar~', SystemEditorVar.get().strip(), os.linesep]))
        f.write(''.join(['SystemLocaterVar~', SystemLocaterVar.get().strip(), os.linesep]))
        f.write(''.join(['SystemDifferVar~', SystemDifferVar.get().strip(), os.linesep]))
        f.write(''.join(['SystemRenamerVar~', SystemRenamerVar.get().strip(), os.linesep]))
        f.write(''.join(['ShowRightCheckVar~', str(ShowRightCheckVar.get()), os.linesep]))
        f.write(''.join(['ShowLeftCheckVar~', str(ShowLeftCheckVar.get()), os.linesep]))
        f.write(''.join(['ShowBothCheckVar~', str(ShowBothCheckVar.get()), os.linesep]))
        f.write(''.join(['ShowDiffCheckVar~', str(ShowDiffCheckVar.get()), os.linesep]))
        f.write(''.join(['ShowDirectoriesCheckVar~', str(ShowDirectoriesCheckVar.get()), os.linesep]))
        f.write(''.join(['AutoRefreshCheckVar~', str(AutoRefreshCheckVar.get()), os.linesep]))
        f.write(''.join(['ConfirmCopyCheckVar~', str(ConfirmCopyCheckVar.get()), os.linesep]))
        f.write(''.join(['ConfirmRenameCheckVar~', str(ConfirmRenameCheckVar.get()), os.linesep]))
        f.write(''.join(['ConfirmDeleteCheckVar~', str(ConfirmDeleteCheckVar.get()), os.linesep]))
        f.write(''.join(['RecycleCheckVar~', str(RecycleCheckVar.get()), os.linesep]))
        f.write(''.join(['CheckSumAutoVar~', str(CheckSumAutoVar.get()), os.linesep]))
        f.write(''.join(['CheckSumTypeVar~', str(CheckSumTypeVar.get()), os.linesep]))
        f.write(''.join(['FileTimeTriggerScaleVar~', str(FileTimeTriggerScaleVar.get()), os.linesep]))
        f.write(''.join(['TriggerNumberOfFilesVar~', str(TriggerNumberOfFilesVar.get()), os.linesep]))

        f.close()
        line_info(ProjectFileNameVar.get())

# ------------------------------
# Edit a project file
    def ProjectEdit():
        line_info(ProjectEntry.get())
        ShowEditFile(ProjectEntry.get())

# ------------------------------
# Show selected row in a message box
    def ShowRow():
        Current = str(DataBox.curselection())
        Current = re.sub('[(),\']', '', Current)

        try:
            ShowRowTopLevel = tkinter.Toplevel()
            ShowRowTopLevel.title('Show row')
            ShowRowTopLevel.wm_transient(Main)
            ShowRowTopLevelX = 250
            ShowRowTopLevelY = 120
            Mainsize = Main.geometry().split('+')
            x = int(Mainsize[1]) + (ShowRowTopLevelX / 2)
            y = int(Mainsize[2]) + (ShowRowTopLevelY / 2)
            ShowRowTopLevel.geometry("%dx%d+%d+%d" % (ShowRowTopLevelX, ShowRowTopLevelY, x, y))
            ShowRowTopLevel.resizable(1, 0)

            tkinter.Label(ShowRowTopLevel,
                          text='Left:  ' + DataBox.get(Current)[0],
                          relief=tkinter.GROOVE).pack(expand=tkinter.FALSE, fill=tkinter.X)
            tkinter.Label(ShowRowTopLevel,
                          text='Right:  ' + DataBox.get(Current)[1],
                          relief=tkinter.GROOVE).pack(expand=tkinter.FALSE, fill=tkinter.X)
            tkinter.Label(ShowRowTopLevel,
                          text='Status:  ' + DataBox.get(Current)[2],
                          relief=tkinter.GROOVE).pack(expand=tkinter.FALSE, fill=tkinter.X)
            tkinter.Label(ShowRowTopLevel,
                          text='More:  ' + DataBox.get(Current)[3],
                          relief=tkinter.GROOVE).pack(expand=tkinter.FALSE, fill=tkinter.X)
            tkinter.Button(ShowRowTopLevel,
                           text='Close',
                           command=lambda: ShowRowTopLevel.destroy()).pack()
        except Exception as e:
            line_info(str(e))
            pass

# ------------------------------
    class Batch:
        AbortVar = tkinter.BooleanVar()
        AbortVar.set(False)

        def ShowBatchForm(self):
            BatchTopLevelVar.deiconify()
            BatchTopLevelVar.wm_transient(Main)
            BatchTopLevelX = 530
            BatchTopLevelY = 250
            Mainsize = Main.geometry().split('+')
            x = int(Mainsize[1]) + (BatchTopLevelX / 2)
            y = int(Mainsize[2]) + (BatchTopLevelY / 2)

            BatchTopLevelVar.geometry("%dx%d+%d+%d" % (BatchTopLevelX, BatchTopLevelY, x, y))
            BatchTopLevelVar.resizable(1, 0)
            line_info()

        def BuildBatchForm(self):
            BatchTopLevelVar = tkinter.Toplevel()
            BatchTopLevelVar.title('Batch')
            BatchTopLevelVar.withdraw()
            BatchTopLevelVar.wm_transient(Main)

            # Get currently selected line
            def GetCurrentSelection():
                Current = str(DataBox.curselection())
                ShowLineNumberVar.set(Current)
                ShowLineNumberVar.set(' '.join([str(DataBox.curselection()),
                                               'of',
                                                str(DataBox.size() - 1)]))
                Current = re.sub('[(),\']', '', Current)
                if ' ' in Current:
                    Current = '-1'
                return Current

            # Get currently selected line information and total line count
            def SelectBlockRows():
                StartRow = re.sub('[(),\']', '', StartRowEntry.get())
                StopRow = re.sub('[(),\']', '', StopRowEntry.get())
                line_info(''.join(['start>', StartRow, '<', 'stop>', StopRow, '<']))
                DataBox.selection_clear(0, 199999)
                if StartRow.isdigit() and StopRow.isdigit():
                    for Row in range(int(StartRow), int(StopRow) + 1):
                        DataBox.selection_set(Row)
                        DataBox.see(Row)
                Update()
                BatchNumberItemsVar.set(ShowLineNumberVar.get())

            # Lists displaylist to command line
            def TestTheData():
                global SelectedListVar
                line_info(str(SelectedListVar))
                line_info(SelectedListVar)
                DataBox.selection_clear(0, 199999)
                for x in SelectedListVar:
                    line_info(''.join([str(x), DataBox.get(x)]))
                    DataBox.selection_set(x)
                    DataBox.see(x)

            # Fetch the first line to perform the batch action on
            def GetLineNumberStart():
                ClearSelectedList()
                tmp = GetCurrentSelection()
                line_info(tmp)
                if len(tmp) > 0:
                    StartRowEntry.insert(0, tmp)
                else:
                    StartRowEntry.insert(0, 0)
                SelectBlockRows()

            # Fetch the last line to perform the batch action on
            def GetLineNumberStop():
                StopRowEntry.delete(0, tkinter.END)
                tmp = GetCurrentSelection()
                line_info(tmp)
                if len(tmp) > 0:
                    StopRowEntry.insert(0, tmp)
                else:
                    StopRowEntry.insert(0, str(DataBox.size() - 1))
                SelectBlockRows()

            # StartRow = '-1'
            # StopRow = '-1'
            BatchStatusVar = tkinter.StringVar()
            # BatchWorkingCount = 0
            BatchStatusVar.set('This is batch mode')

            # TODO VerifyInput(trace)
            def VerifyInput(trace):
                StartRow = str(StartRowEntry.get())
                StopRow = str(StopRowEntry.get())
                BatchStatusVar.set(trace + '\nSuccess')
                TestMessage = ''
                if not StartRow.isdigit() or not StopRow.isdigit():
                    TestMessage = 'Start and stop row must be positive integer values'
                    BatchStatusVar.set(trace + '\n' + TestMessage)
                    tkinter.messagebox.showerror('Bad entry value', trace + '\n' + TestMessage)
                    SplashScreen('Batch copy is closing', False)
                    return 1
                line_info('Start row:' + str(StartRow) + '  Number of items:' + str(DataBox.size() - 1))
                if int(StartRow) < 0:
                    TestMessage += '\nStart must be 0 or more\n'
                if int(StartRow) > int(DataBox.size() - 1):
                    TestMessage += '\nStart must be less than or equal to ' + str(DataBox.size() - 1)
                if int(StartRow) > int(StopRow):
                    TestMessage += '\nStart must be less than or equal to stop'
                if int(StopRow) > int(DataBox.size() - 1):
                    TestMessage += '\nStop must be less than or equal to ' + str(DataBox.size() - 1)
                if len(TestMessage) > 0:
                    TestMessage += '\nStart: ' + str(StartRow) + ' Stop: ' + str(StopRow)
                    BatchStatusVar.set(trace + '\n' + TestMessage)
                    tkinter.messagebox.showerror('Bad entry value', trace + '\n' + TestMessage)
                    return 1
                return 0

            def BatchRefresh():
                GetLineNumberStart()
                GetLineNumberStop()
                BatchNumberItemsVar.set(str(DataBox.size() - 1))

            def GetFilePathList(trace):  # This gets the selected items and puts them in FilePathList
                FilePathList = []  # SelectedListVar
                if VerifyInput(trace) != 0:
                    return
                DataBox.selection_clear(0, 199999)
                try:
                    DataBox.selection_set(int(StartRowEntry.get()), int(StopRowEntry.get()))
                except Exception as e:
                    line_info(str(e))
                    return

                ShowLineNumberVar.set(str(DataBox.curselection()) + ' of ' + str(DataBox.size() - 1))
                for i in range(int(StartRowEntry.get()), int(StopRowEntry.get()) + 1):
                    FileLeftNameVar.set(DataBox.get(i)[0])
                    FileRightNameVar.set(DataBox.get(i)[1])

                    FileLeftNameVar.set(DataBox.get(i)[0])
                    FileRightNameVar.set(DataBox.get(i)[1])
                    if len(FileLeftNameVar.get()) < 1:
                        left = LeftPathEntry.get() + os.linesep
                    else:
                        left = os.path.join(LeftPathEntry.get(), FileLeftNameVar.get())
                    if len(FileRightNameVar.get()) < 1:
                        right = RightPathEntry.get() + os.linesep()
                    else:
                        right = os.path.join(RightPathEntry.get(), FileRightNameVar.get())
                    FilePathList.append(left + '~' + right)
                line_info(FilePathList)
                return FilePathList

            # The batch rename functions call external renamer programs
            # Linux: /usr/bin/pyrenamer
            # Windows (x64): C:\Program Files (x86)\Ant Renamer\Renamer.exe
            # Windows (x32): C:\Program Files\Ant Renamer\Renamer.exe
            def BatchRename(Trace):
                line_info(Trace)
                if Trace == 'left':  # Rename left
                    StartFile(SystemRenamerVar.get(), LeftPathEntry.get())
                elif Trace == 'right':  # Rename right
                    StartFile(SystemRenamerVar.get(), RightPathEntry.get())
                else:
                    line_info(' '.join(['ERROR with batch rename trace',
                                        Trace,
                                        SystemRenamerVar.get()]))
                return

            def BatchRenameRight():
                BatchRename('right')

            def BatchRenameLeft():
                BatchRename('left')

            # This either sends item to trash or deletes them depending on options setting
            def BatchDeleteOrTrash(Trace):
                SplashScreen('Batch Delete is running:' + Trace, True)
                self.AbortVar.set(False)
                BatchDeleteList = GetFilePathList('Batch delete')
                if BatchDeleteList is None:
                    return
                line_info(Trace)
                BatchDeleteCount = 0

                for RowStr in BatchDeleteList:
                    Main.update_idletasks()
                    if self.AbortVar.get():
                        break
                    BatchDeleteCount += 1
                    BatchStatusVar.set('Batch delete:' + str(BatchDeleteCount))
                    Main.update_idletasks()
                    RowStrSplit = RowStr.split('~')
                    if Trace == 'left':
                        line_info(' '.join(['Delete left.', RowStrSplit[0]]))
                        if os.path.exists(RowStrSplit[0]) and os.path.isfile(RowStrSplit[0]):
                            if RecycleCheckVar.get() == 0:
                                RemoveAFile(RowStrSplit[0], Trash=False)
                            else:
                                RemoveAFile(RowStrSplit[0], Tras=True)
                    elif Trace == 'right':  # Delete right
                        line_info(' '.join(['Delete right:', RowStrSplit[0]]))
                        if os.path.exists(RowStrSplit[1]) and os.path.isfile(RowStrSplit[1]):
                            if RecycleCheckVar.get() == 0:
                                RemoveAFile(RowStrSplit[1], Trash=False)
                            else:
                                RemoveAFile(RowStrSplit[1], Trash=True)
                    elif Trace == 'auto':  # Delete auto deletes whatever exists
                        line_info(' '.join(['Delete auto.', RowStrSplit[0]]))
                        if os.path.exists(RowStrSplit[0]) and os.path.isfile(RowStrSplit[0]):
                            if RecycleCheckVar.get() == 0:
                                RemoveAFile(RowStrSplit[0], Trash=False)
                                # os.remove(RowStrSplit[0])
                            else:
                                RemoveAFile(RowStrSplit[0], Trash=True)
                                # send2trash(RowStrSplit[0])

                        if os.path.exists(RowStrSplit[1]) and os.path.isfile(RowStrSplit[1]):
                            if RecycleCheckVar.get() == 0:
                                RemoveAFile(RowStrSplit[1], Trash=False)
                                # os.remove(RowStrSplit[1])
                            else:
                                # send2trash(RowStrSplit[1])
                                RemoveAFile(RowStrSplit[1], Trash=True)
                    else:
                        line_info(' '.join(['ERROR with batch delete ', Trace]))
                StartRowEntry.delete(0, tkinter.END)
                StopRowEntry.delete(0, tkinter.END)
                SplashScreen(' '.join(['Batch Delete is closing:', Trace]), False)
                if AutoRefreshCheckVar.get():
                    FetchData()
                    tkinter.update()
                    BatchNumberItemsVar.set(str(DataBox.size() - 1))

            # ---------------------------------
            def BatchCopy(Trace):
                self.AbortVar.set(False)
                BatchCopyList = GetFilePathList('Batch copy')
                if BatchCopyList is None:
                    return
                SplashScreen(' '.join(['Batch copy is running', Trace]), True)

                line_info(Trace)
                BatchCopyCount = 0
                for RowStr in BatchCopyList:
                    Main.update_idletasks()
                    if self.AbortVar.get():
                        break
                    BatchCopyCount += 1
                    BatchStatusVar.set(' '.join(['Batch copy', str(BatchCopyCount)]))
                    Main.update_idletasks()
                    RowStrSplit = RowStr.split('~')
                    line_info(str(RowStrSplit))
                    if Trace == 'right':  # Copy right
                        src = RowStrSplit[1]  # right
                        dst = RowStrSplit[0]  # left
                        CopyAFile(' '.join(['Batch copy right to left', Trace]), src, dst, True)
                    elif Trace == 'left':  # Copy left
                        src = RowStrSplit[0]  # left
                        dst = RowStrSplit[1]  # right
                        CopyAFile(' '.join(['Batch copy left to right', Trace]), src, dst, True)
                    elif Trace == 'auto':  # Copy auto
                        src = RowStrSplit[1]  # right
                        dst = RowStrSplit[0]  # left
                        CopyAFile(' '.join(['Batch copy right to left', Trace]), src, dst, True)
                        src = RowStrSplit[0]  # right
                        dst = RowStrSplit[1]  # left
                        CopyAFile(' '.join(['Batch copy right to left', Trace]), src, dst, True)
                StartRowEntry.delete(0, tkinter.END)
                StopRowEntry.delete(0, tkinter.END)
                if AutoRefreshCheckVar.get():
                    FetchData()
                StatusVar.set(' '.join(['Batch copy complete. Files copied:',
                                        str(BatchCopyCount)]))
                SplashScreen(' '.join(['Batch copy is closing', Trace]), False)

            # ---------------------------------
            line_info('Batch')
            BatchTopLevelVar = tkinter.Toplevel()
            BatchTopLevelVar.title('Batch')

            # Status frame and abort
            BatchFrame1 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame1.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

            # Block mode
            BatchFrame2 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame2.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

            # This frame is for search
            BatchFrame3 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame3.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

            # This frame is for add/remove/clear buttons
            BatchFrame4 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame4.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

            # The following frames are used for the action buttons
            BatchFrame5 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame5.pack(side=tkinter.TOP, fill=tkinter.X)

            BatchFrame5a = tkinter.Frame(BatchFrame5, relief=tkinter.SUNKEN, bd=1)
            BatchFrame5a.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.Y)

            BatchFrame5b = tkinter.Frame(BatchFrame5, relief=tkinter.SUNKEN, bd=1)
            BatchFrame5b.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.Y)

            BatchFrame5c = tkinter.Frame(BatchFrame5, relief=tkinter.SUNKEN, bd=1)
            BatchFrame5c.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.Y)

            # Display number of lines
            BatchFrame6 = tkinter.Frame(BatchTopLevelVar, relief=tkinter.SUNKEN, bd=1)
            BatchFrame6.pack(side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.X)

            # ---------------------------------
            BatchStatus = tkinter.Label(BatchFrame1, textvariable=BatchStatusVar, relief=tkinter.GROOVE)
            BatchStatus.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
            ToolTip(BatchStatus, 'Displays batch status')

            AbortCheck = tkinter.Checkbutton(BatchFrame1, text='Abort', variable=self.AbortVar)
            AbortCheck.pack(side=tkinter.LEFT)
            ToolTip(AbortCheck, 'Abort batch operations')

            # ---------------------------------
            # Block select controls
            StartRowButton = tkinter.Button(BatchFrame2, text='Start row:', command=GetLineNumberStart)
            StartRowButton.pack(side=tkinter.LEFT)
            ToolTip(StartRowButton, 'Fetch the first line to perform the batch action on')
            StartRowEntry = tkinter.Entry(BatchFrame2, width=6)
            StartRowEntry.pack(side=tkinter.LEFT)
            StartRowEntry.bind('<Return>', lambda x: SelectBlockRows())
            # StartRowEntry.bind('<Leave>', lambda x: SelectBlockRows())
            ToolTip(StartRowEntry, 'Enter the first line to perform the batch action on')

            StopRowButton = tkinter.Button(BatchFrame2, text='Stop row:', command=GetLineNumberStop)
            StopRowButton.pack(side=tkinter.LEFT)
            ToolTip(StopRowButton, 'Fetch the last line to perform the batch action on')
            StopRowEntry = tkinter.Entry(BatchFrame2, width=6)
            StopRowEntry.pack(side=tkinter.LEFT)
            StopRowEntry.bind('<Return>', lambda x: SelectBlockRows())
            # StopRowEntry.bind('<Leave>', lambda x: SelectBlockRows())
            ToolTip(StopRowEntry, 'Enter the last line to perform the batch action on')

            # BatchRefreshButton = tkinter.Button(BatchFrame2, text='Select', command=SelectBlockRows, width=7)
            # BatchRefreshButton.pack(side=tkinter.LEFT)
            # ToolTip(BatchRefreshButton,'Get currently selected line information and total line count')

            # The follow will test that the selected data is valid
            BatchTestButton = tkinter.Button(BatchFrame2, text='Test', command=TestTheData, width=7)
            BatchTestButton.pack(side=tkinter.RIGHT)
            ToolTip(BatchTestButton, 'Lists displaylist to command line')

            # ---------------------------------
            # Search BatchFrame3
            tkinter.Checkbutton(BatchFrame3, text='Left', variable=LeftSearchVar).pack(side=tkinter.LEFT)
            tkinter.Checkbutton(BatchFrame3, text='Right', variable=RightSearchVar).pack(side=tkinter.LEFT)
            tkinter.Checkbutton(BatchFrame3, text='Status', variable=StatusSearchVar).pack(side=tkinter.LEFT)
            tkinter.Checkbutton(BatchFrame3, text='More', variable=MoreSearchVar).pack(side=tkinter.LEFT)
            tkinter.Checkbutton(BatchFrame3, text='Case', variable=CaseSearchVar).pack(side=tkinter.LEFT)

            SearchButtonBatch = tkinter.Button(BatchFrame3, text='Search', width=6, command=lambda: SearchData('batch', 'search'))
            SearchButtonBatch.pack(side=tkinter.LEFT)
            ResetSearchButton = tkinter.Button(BatchFrame3, text='Reset', width=6, command=ResetSearchData)
            ResetSearchButton.pack(side=tkinter.LEFT)
            ToolTip(SearchButtonBatch, 'Enter a Search string to find certain entries')
            SearchEntryBatch = tkinter.Entry(BatchFrame3)
            SearchEntryBatch.bind('<Return>', lambda x: SearchData('batch', 'search'))
            SearchEntryBatch.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
            ToolTip(SearchEntryBatch, 'Enter a Search string to find certain entries')
            SearchEntryBatch.delete(0, tkinter.END)

            # This frame is for add/remove/clear/show buttons
            AddRowsButton = tkinter.Button(BatchFrame4, text='Add row(s)', command=AddSelectedToList)
            AddRowsButton.pack(side=tkinter.LEFT)
            ToolTip(AddRowsButton, 'Add all selected rows to display list')

            RemoveRowButton = tkinter.Button(BatchFrame4, text='Remove row', command=RemoveARow)
            RemoveRowButton.pack(side=tkinter.LEFT)
            ToolTip(RemoveRowButton, 'Remove the selected row from display list')

            ClearAllRowsButton = tkinter.Button(BatchFrame4, text='Clear all rows', command=ClearSelectedList)
            ClearAllRowsButton.pack(side=tkinter.LEFT)
            ToolTip(ClearAllRowsButton, 'Remove all rows from display list')

            ShowRowsButton = tkinter.Button(BatchFrame4, text='Show rows', command=ShowSelectedList)
            ShowRowsButton.pack(side=tkinter.LEFT)
            ToolTip(ShowRowsButton, 'Show all selected rows')

            # ---------------------------------
            # Action buttons BatchFrame5
            DeleteLeftButton = tkinter.Button(BatchFrame5a, text='Delete left', state=tkinter.NORMAL, width=20, command=lambda: BatchDeleteOrTrash('left'))
            DeleteLeftButton.pack(anchor='w')
            ToolTip(DeleteLeftButton, 'Batch delete left')

            DeleteRightButton = tkinter.Button(BatchFrame5a, text='Delete right', state=tkinter.NORMAL, width=20, command=lambda: BatchDeleteOrTrash('right'))
            DeleteRightButton.pack(anchor='w')
            ToolTip(DeleteRightButton, 'Batch delete right')

            DeleteAutoButton = tkinter.Button(BatchFrame5a, text='Delete auto', state=tkinter.NORMAL, width=20, command=lambda: BatchDeleteOrTrash('auto'))
            DeleteAutoButton.pack(anchor='w')
            ToolTip(DeleteAutoButton, 'Batch delete auto')
            # ---------------------------------
            CopyLeftButton = tkinter.Button(BatchFrame5b, text='Copy left to right', state=tkinter.NORMAL, width=20, command=lambda: BatchCopy('left'))
            CopyLeftButton.pack(anchor='w')
            ToolTip(CopyLeftButton, 'Batch copy left')

            CopyRightButton = tkinter.Button(BatchFrame5b, text='Copy right to left', state=tkinter.NORMAL, width=20, command=lambda: BatchCopy('right'))
            CopyRightButton.pack(anchor='w')
            ToolTip(CopyRightButton, 'Batch copy Right')

            CopyAutoButton = tkinter.Button(BatchFrame5b, text='Copy auto', state=tkinter.NORMAL, width=20, command=lambda: BatchCopy('auto'))
            CopyAutoButton.pack(anchor='w')
            ToolTip(CopyAutoButton, 'Batch copy auto')
            # ---------------------------------
            RenameLeftButton = tkinter.Button(BatchFrame5c, text='Rename left', state=tkinter.NORMAL, width=20, command=BatchRenameLeft)
            RenameLeftButton.pack(anchor='w')
            ToolTip(RenameLeftButton, 'Batch rename left')

            RenameRightButton = tkinter.Button(BatchFrame5c, text='Rename right', state=tkinter.NORMAL, width=20, command=BatchRenameRight)
            RenameRightButton.pack(anchor='w')
            ToolTip(RenameRightButton, 'Batch rename right')
            # -------------------
            BatchSelectedLine = tkinter.Button(BatchFrame6,
                                               textvariable=BatchNumberItemsVar,
                                               command=SelectBlockRows,
                                               relief=tkinter.GROOVE)
            BatchSelectedLine.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.BOTH)
            ToolTip(BatchSelectedLine, 'Number of lines in data display')

            BatchTopLevelVar.withdraw()

            def BatchXButton():
                line_info('Batch X button detected')
                BatchTopLevelVar.withdraw()
            BatchTopLevelVar.protocol('WM_DELETE_WINDOW', BatchXButton)

# ------------------------------
# Any entry, scale or other widgets go here
    class Options:
        def ShowOptionsForm(self):
            # Deiconify the TopLevelVar and put it in the center of the main window
            OptionsTopLevelVar.deiconify()
            Main.update()
            OptionsTopLevelSizeX = 350
            OptionsTopLevelSizeY = 175
            MainGeo = Main.geometry().split('+')
            # MainPosition = MainGeo[0].split('x')
            x = int(MainGeo[1]) + (OptionsTopLevelSizeX / 2)
            y = int(MainGeo[2]) + (OptionsTopLevelSizeY / 2)

            OptionsTopLevelVar.geometry("%dx%d+%d+%d" % (OptionsTopLevelSizeX, OptionsTopLevelSizeY, x, y))
            OptionsTopLevelVar.resizable(1, 0)
            OptionsTopLevelVar.wm_transient(Main)

            line_info('ShowOptionsForm')

        def BuildOptionsForm(self):
            line_info('BuildOptionsForm')
            OptionsTopLevelVar = tkinter.Toplevel()
            OptionsTopLevelVar.title('Options')
            OptionsTopLevelVar.withdraw()

            def OptionsXButton():
                line_info('Options X button detected')
                OptionsTopLevelVar.withdraw()
            OptionsTopLevelVar.protocol('WM_DELETE_WINDOW', OptionsXButton)

            FileTimeTriggerScale = tkinter.Scale(OptionsTopLevelVar,
                                                 from_=0,
                                                 to=5000,
                                                 variable=FileTimeTriggerScaleVar,
                                                 orient=tkinter.HORIZONTAL,
                                                 tickinterval=1000,
                                                 label='File time difference trigger (seconds)',
                                                 length=200)
            FileTimeTriggerScale.pack(fill='x')

            TriggerNumberOfFilesScale = tkinter.Scale(OptionsTopLevelVar,
                                                      from_=0,
                                                      to=500,
                                                      variable=TriggerNumberOfFilesVar,
                                                      orient=tkinter.HORIZONTAL,
                                                      tickinterval=100,
                                                      label='Trigger number of files',
                                                      length=200)
            TriggerNumberOfFilesScale.pack(fill='x')

# ------------------------------
    def ShowEditFile(FileName=None):
        if FileName is None:
            FileName = tkinter.filedialog.askopenfilename(defaultextension='.*',
                                                          initialdir=os.path.dirname(os.path.realpath(StartUpDirectoryVar.get())),
                                                          filetypes=[('All files', '*.*')],
                                                          title='Show/Edit a file',
                                                          parent=OptionsTopLevelVar)

        line_info(' '.join(['Show/Edit file: >>', FileName, '<<']))
        FileName = os.path.normpath(FileName)
        try:
            StartFile(SystemEditorVar.get(), FileName)
        except IOError:
            tkinter.messagebox.showerror('Show/Edit file error',
                                         ' '.join(['Requested file does not exist:', FileName]))
            return

# ------------------------------
    def ClearLog():
        os.system(['clear', 'cls'][os.name == 'nt'])

# ------------------------------
    def ViewLog():
        ShowEditFile(FileName=LogFileNameVar.get())
# ------------------------------

# Some debug stuff
    def About():
        line_info('About ' + main.StartUpDirectoryVar.get())
        tkinter.messagebox.showinfo('About',
                                    os.linesep.join([main.StartUpDirectoryVar.get(),
                                                     Main.geometry(),
                                                     ''.join([str(Main.winfo_screenwidth()),
                                                              'x',
                                                              str(Main.winfo_screenheight())]),
                                                     ' '.join(['Python version:',
                                                               platform.python_version()]),
                                                     ' '.join(['PyBackupTk version:',
                                                               ProgramVersionNumber.get()]),
                                                     platform.platform()]))

# ------------------------------

# The help file
    def Help():
        line_info(' '.join(['Help', main.StartUpDirectoryVar.get()]))

        try:
            f = open(HelpFileVar.get(), 'r')
        except IOError:
            tkinter.messagebox.showerror('Help file error',
                                         os.linesep.join(['Requested file does not exist.>>',
                                                          HelpFileVar.get() + '<<']))

            return
        data = f.read()
        f.close()

        MyMessageBox(Title='PyDiff help',
                     TextMessage=data,
                     Buttons=['OK', 'Cancel', 'Abort', 'Who cares???'],
                     LabelText=['This is a test label',
                                'Can you get an initiator zoned?',
                                '222'],
                     fgColor='pink',
                     bgColor='black',
                     Center=Main,
                     Geometry='500x300+1300+20')

# ------------------------------
# Swap the left and right entry boxes (other menu)
    def SwapLeftAndRight():
        line_info('SwapLeftAndRight')
        temp1 = LeftPathEntry. get()
        temp2 = RightPathEntry. get()
        LeftPathEntry.delete(0, tkinter.END)
        LeftPathEntry.insert(0, temp2)
        RightPathEntry.delete(0, tkinter.END)
        RightPathEntry.insert(0, temp1)
# ------------------------------
# This where the program starts up
    # default_font = tkFont.nametofont("TkFixedFont")
    # default_font.configure(size=9)
    Main.option_add('*Font', 'courier 10')

    FileRenameTopLevelVar = tkinter.Toplevel()
    FileRenameTopLevelVar.title('File rename')
    FileRenameTopLevelVar.withdraw()

    ControlFrame1 = tkinter.Frame(Main, relief=tkinter.SUNKEN, bd=1)
    ControlFrame1.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

    ControlFrame2 = tkinter.Frame(Main, relief=tkinter.SUNKEN, bd=1)
    ControlFrame2.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

    ControlFrame3 = tkinter.Frame(Main, relief=tkinter.SUNKEN, bd=1)
    ControlFrame3.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

    ControlFrame4 = tkinter.Frame(Main, relief=tkinter.SUNKEN, bd=1)
    ControlFrame4.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)

    DataFrame = tkinter.Frame(Main, relief=tkinter.GROOVE, bd=5)
    DataFrame.pack(side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)
    # mlb = MultiListbox(tk, (('Subject', 40), ('Sender', 20), ('Date', 10)))
    # DataBox = MultiListbox(DataFrame, (('Left', 45),
    # xxx = MultiListbox.MultiListbox
    DataBox = MultiListbox(DataFrame, (('Left', 45),
                                       ('Right', 45),
                                       ('Status', 3),
                                       ('More', 40)))

    ToolTip(DataBox, text='This is where the data is displayed')
    DataBox.pack(expand=tkinter.TRUE, fill=tkinter.BOTH)

    menubar = tkinter.Menu(Main)
    Main['menu'] = menubar
    DirectoriesSelectMenu = tkinter.Menu(menubar)
    ProjectsMenu = tkinter.Menu(menubar)
    OptionsMenu = tkinter.Menu(menubar)
    OtherMenu = tkinter.Menu(menubar)
    HelpMenu = tkinter.Menu(menubar)

    menubar.add_cascade(menu=DirectoriesSelectMenu, label='Directories')
    DirectoriesSelectMenu.add_command(label='Select both directories', command=lambda: FetchDirectories('Both'))
    DirectoriesSelectMenu.add_command(label='Select left directory', command=lambda: FetchDirectories('Left'))
    DirectoriesSelectMenu.add_command(label='Select right directory', command=lambda: FetchDirectories('Right'))

    # DirectoriesSelectMenu.add_command(label='History', command=HistoryInstance.HistoryGoto)

    menubar.add_cascade(menu=ProjectsMenu, label='Projects')
    ProjectsMenu.add_command(label='Load', command=ProjectLoad)
    ProjectsMenu.add_command(label='Save', command=ProjectSave)
    ProjectsMenu.add_command(label='Edit', command=ProjectEdit)

    menubar.add_cascade(menu=OptionsMenu, label='Options')
    OptionsMenu.add_checkbutton(label='Auto refresh', variable=AutoRefreshCheckVar)
    OptionsMenu.add_checkbutton(label='Confirm copy', variable=ConfirmCopyCheckVar)
    OptionsMenu.add_checkbutton(label='Confirm delete', variable=ConfirmDeleteCheckVar)
    OptionsMenu.add_checkbutton(label='Confirm rename', variable=ConfirmRenameCheckVar)
    OptionsMenu.add_checkbutton(label='Recycle', variable=RecycleCheckVar)
    OptionsMenu.add_separator()
    OptionsMenu.add_checkbutton(label='Auto checksum', variable=CheckSumAutoVar)

    OptionsMenu.add_radiobutton(label='CRC32', variable=CheckSumTypeVar, value=1)
    OptionsMenu.add_radiobutton(label='MD5', variable=CheckSumTypeVar, value=2)
    OptionsMenu.add_radiobutton(label='SHA1', variable=CheckSumTypeVar, value=3)

    OptionsMenu.add_separator()
    OptionsMenu.add_checkbutton(label='Show both', variable=ShowBothCheckVar)
    OptionsMenu.add_checkbutton(label='Show diff', variable=ShowDiffCheckVar)
    OptionsMenu.add_checkbutton(label='Show left', variable=ShowLeftCheckVar)
    OptionsMenu.add_checkbutton(label='Show right', variable=ShowRightCheckVar)
    OptionsMenu.add_checkbutton(label='Show directories', variable=ShowDirectoriesCheckVar)

    OptionsMenu.add_separator()
    OptionsInstance = Options()
    OptionsMenu.add_command(label='Other settings', command=OptionsInstance.ShowOptionsForm)

    menubar.add_cascade(menu=OtherMenu, label='Other')
    OtherMenu.add_command(label='Swap left and right', command=SwapLeftAndRight)
    OtherMenu.add_command(label='Show disk space', command=DiskSpace)
    OtherMenu.add_command(label='Show/Edit file', command=ShowEditFile)
    OtherMenu.add_command(label='View log', command=ViewLog)
    OtherMenu.add_command(label='Clear log', command=ClearLog)
    OtherMenu.add_command(label='Clear all', command=ClearAll)

    menubar.add_cascade(menu=HelpMenu, label='Help')
    HelpMenu.add_command(label='About', command=About)
    HelpMenu.add_command(label='Help', command=Help)
    HelpMenu.add_command(label='Quit', command=Quit)

    FileInfoInstance = FileInfo()
    FileInfoButton = tkinter.Button(ControlFrame2, text='File info', command=FileInfoInstance.ShowFileInfo)
    FileInfoButton.pack(side=tkinter.LEFT)
    ToolTip(FileInfoButton, text='Show file info form')

    BatchInstance = Batch()
    BatchButton = tkinter.Button(ControlFrame2, text='Batch', command=BatchInstance.ShowBatchForm)
    BatchButton.pack(side=tkinter.LEFT)
    ToolTip(BatchButton, text='Show batch form')

    Statuslabel = tkinter.Label(ControlFrame2, textvariable=StatusVar, relief=tkinter.GROOVE)
    Statuslabel.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
    StatusVar.set('Status: Program started')
    ToolTip(Statuslabel, text='Show the status')

    ShowLineNumber = tkinter.Label(ControlFrame2, textvariable=ShowLineNumberVar, relief=tkinter.GROOVE)
    ShowLineNumber.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
    ToolTip(ShowLineNumber, text=os.linesep.join(['Show line numbers',
                                                 'All values are zero based']))

    def BothX():
        if AutoRefreshCheckVar.get():
            FetchData()
        line_info('BothVar: ' + str(ShowBothCheckVar.get()))
        ShowBoth = tkinter.Checkbutton(ControlFrame1, text='Both', variable=ShowBothCheckVar, command=BothX)
        ShowBoth.pack(side=tkinter.LEFT)
        ToolTip(ShowBoth, 'Show items that exist in both left and right directories and are the same')
        ShowBothCheckVar.set(tkinter.TRUE)

    def DiffX():
        if AutoRefreshCheckVar.get():
            FetchData()
        line_info('DiffVar: ' + str(ShowDiffCheckVar.get()))
        ShowDiff = tkinter.Checkbutton(ControlFrame1, text='Diff', variable=ShowDiffCheckVar, command=DiffX)
        ShowDiff.pack(side=tkinter.LEFT)
        ToolTip(ShowDiff, 'Show items that exist in both left and right directories but are different')
        ShowDiffCheckVar.set(tkinter.TRUE)

    def LeftX():
        if AutoRefreshCheckVar.get():
            FetchData()
        line_info('LeftVar: ' + str(ShowLeftCheckVar.get()))
        ShowLeft = tkinter.Checkbutton(ControlFrame1, text='Left', variable=ShowLeftCheckVar, command=LeftX)
        ShowLeft.pack(side=tkinter.LEFT)
        ToolTip(ShowLeft, 'Show items that exist in the left directory only')
        ShowLeftCheckVar.set(tkinter.FALSE)

    def RightX():
        if AutoRefreshCheckVar.get():
            FetchData()
        line_info('RightVar: ' + str(ShowRightCheckVar.get()))
        ShowRight = tkinter.Checkbutton(ControlFrame1, text='Right', variable=ShowRightCheckVar, command=RightX)
        ShowRight.pack(side=tkinter.LEFT)
        ToolTip(ShowRight, 'Show items that exist in the right directory only')
        ShowRightCheckVar.set(tkinter.FALSE)

    ProjectFrame = tkinter.Frame(ControlFrame1, relief=tkinter.SUNKEN, bd=2)
    ProjectFrame.pack(side=tkinter.TOP, expand=tkinter.FALSE, fill=tkinter.X)
    ProjectLabel = tkinter.Label(ProjectFrame, text='Project', width=8)
    ProjectLabel.pack(side=tkinter.LEFT)
    ToolTip(ProjectLabel, 'Enter or show the current project file name')
    ProjectEntry = tkinter.Entry(ProjectFrame)
    ProjectEntry.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
    ToolTip(ProjectEntry, 'Enter or show the current project file name')
    ProjectEntry.delete(0, tkinter.END)
    ProjectEntry.insert(0, '****************')

# ---------
    FilterFrame = tkinter.Frame(ControlFrame1, relief=tkinter.SUNKEN, bd=2)
    FilterFrame.pack(side=tkinter.LEFT, fill=tkinter.X)
    FetchDataButton = tkinter.Button(FilterFrame, text='Fetch data', width=12, command=FetchData)
    FetchDataButton.pack(side=tkinter.LEFT)
    ToolTip(FetchDataButton, 'Fetch data')
    FilterEntry = tkinter.Entry(FilterFrame, width=8)
    FilterEntry.pack(side=tkinter.LEFT)
    ToolTip(FilterEntry, 'Enter a filter string to display only certain entries')
    FilterEntry.delete(0, tkinter.END)

    tkinter.Checkbutton(FilterFrame, text='Both', variable=ShowBothCheckVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(FilterFrame, text='Diff', variable=ShowDiffCheckVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(FilterFrame, text='Left', variable=ShowLeftCheckVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(FilterFrame, text='Right', variable=ShowRightCheckVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(FilterFrame, text='Dir', variable=ShowDirectoriesCheckVar).pack(side=tkinter.LEFT)
# ---------
    SearchFrame = tkinter.Frame(ControlFrame1, relief=tkinter.SUNKEN, bd=2)
    SearchFrame.pack(side=tkinter.LEFT, fill=tkinter.X)
    SearchButtonMain = tkinter.Button(SearchFrame, text='Search', width=6, command=lambda: SearchData('main', 'search'))
    SearchButtonMain.pack(side=tkinter.LEFT)
    ToolTip(SearchButtonMain, 'Enter a string to search for certain entries')
    SelectButtonMain = tkinter.Button(SearchFrame, text='Select', width=6, command=lambda: SearchData('main', 'select'))
    SelectButtonMain.pack(side=tkinter.LEFT)
    ToolTip(SelectButtonMain, 'Enter a string to select certain entries')
    ResetSearchButton = tkinter.Button(SearchFrame, text='Reset', width=6, command=ResetSearchData)
    ResetSearchButton.pack(side=tkinter.LEFT)
    SearchEntryMain = tkinter.Entry(SearchFrame, width=8)
    SearchEntryMain.pack(side=tkinter.LEFT)
    ToolTip(SearchEntryMain, 'Enter a Search string to find certain entries')
    SearchEntryMain.delete(0, tkinter.END)

    tkinter.Checkbutton(SearchFrame, text='Left', variable=LeftSearchVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(SearchFrame, text='Right', variable=RightSearchVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(SearchFrame, text='Status', variable=StatusSearchVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(SearchFrame, text='More', variable=MoreSearchVar).pack(side=tkinter.LEFT)
    tkinter.Checkbutton(SearchFrame, text='Case', variable=CaseSearchVar).pack(side=tkinter.LEFT)
# ---------

    Leftdirectorybutton = tkinter.Button(ControlFrame3, width=20, text='Left directory path', command=lambda: FetchDirectories('Left'))
    Leftdirectorybutton.pack(side=tkinter.LEFT)
    ToolTip(Leftdirectorybutton, 'Enter or display left directory path')
    LeftPathEntry = tkinter.Entry(ControlFrame3)
    LeftPathEntry.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
    ToolTip(LeftPathEntry, 'Enter or display left directory path')
    LeftPathEntry.delete(0, tkinter.END)

    Rightdirectorybutton = tkinter.Button(ControlFrame4, width=20, text='Right directory path', command=lambda: FetchDirectories('Right'))
    Rightdirectorybutton.pack(side=tkinter.LEFT)
    RightPathEntry = tkinter.Entry(ControlFrame4)
    RightPathEntry.pack(side=tkinter.LEFT, expand=tkinter.TRUE, fill=tkinter.X)
    ToolTip(RightPathEntry, 'Enter or display the right directory path')
    RightPathEntry.delete(0, tkinter.END)
    ToolTip(Rightdirectorybutton, 'Enter or display the right directory path')

    Main.title('PyDiffTk')
    Main.minsize(920, 300)
    Main.resizable(True, True)
    Main.wm_iconname('PyDiffTk')

    AutoRefreshCheckVar.set(1)
    CheckSumTypeVar.set(1)

    RecycleCheckVar.set(1)
    ConfirmCopyCheckVar.set(1)
    ConfirmDeleteCheckVar.set(1)
    ConfirmRenameCheckVar.set(1)

    OptionsInstance.BuildOptionsForm()
    BatchInstance.BuildBatchForm()
    FileInfoInstance.BuildFileInfoForm()

    LeftPathEntry.delete(0, tkinter.END)
    RightPathEntry.delete(0, tkinter.END)

    ParseCommandLine()
    SetDefaults()  # Initialize the variables
    StartUpStuff()

    line_info('System editor: ' + SystemEditorVar.get())
    line_info('System differ: ' + SystemDifferVar.get())
    line_info('System renamer: ' + SystemRenamerVar.get())

    Main.bind('<F1>', lambda e: Help())
    Main.bind('<F2>', lambda e: About())
    Main.bind('<F3>', lambda e: ClearAll())
    Main.bind('<F4>', lambda e: ShowRow())
    Main.bind('<F5>', lambda e: FetchData())
    Main.bind('<F7>', ShowSelectedList)
    Main.bind('<F8>', AddSelectedToList)
    Main.bind('<F9>', ClearSelectedList)
    Main.bind('<F12>', lambda e: FileInfoInstance.ShowFileInfo())
    Main.bind('<Control-q>', lambda e: Quit())
    Main.bind('<Control-Q>', lambda e: Quit())
    Main.bind('<ButtonRelease-1>', lambda e: Update())
    Main.bind('<ButtonRelease-2>', lambda e: BatchInstance.ShowBatchForm())  # Middle button
    Main.bind('<ButtonRelease-3>', lambda e: FileInfoInstance.ShowFileInfo())  # Right button
    # Main.bind('<Configure>', lambda e: ShowResize(Main))
    # This prints out the window geometry on resize event

    Main.mainloop()
