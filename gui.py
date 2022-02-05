import sys
import argparse

from qtpy import QtCore, QtGui, QtWidgets
import qtpy.compat as qtcompat

from config import Config, Ui_ConfigDialog
from tree import ResultsTreeWidget

LINE_PROFILER_DOC_URL = "https://github.com/pyutils/line_profiler#id2"

from utils import translate as _


class UI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.config = Config()

        QtWidgets.QMainWindow.__init__(self)
        self.setup_ui()

    def setup_ui(self):
        # Main window
        self.setObjectName("self")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralLayout.setContentsMargins(0, 6, 0, 0)
        self.centralLayout.setObjectName("centralLayout")
        self.setCentralWidget(self.centralwidget)

        # Results tab
        self.resultsTab = QtWidgets.QWidget()
        self.resultsTab.setObjectName("resultsTab")
        self.resultsTabLayout = QtWidgets.QVBoxLayout(self.resultsTab)
        self.resultsTabLayout.setContentsMargins(0, 0, 0, 0)
        self.resultsTabLayout.setObjectName("resultsTabLayout")
        self.resultsTreeWidget = ResultsTreeWidget(self.resultsTab)
        self.resultsTreeWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.resultsTreeWidget.setObjectName("resultsTreeWidget")
        self.resultsTabLayout.addWidget(self.resultsTreeWidget)

        # Output tab
        self.outputTab = QtWidgets.QWidget()
        self.outputTab.setObjectName("outputTab")
        self.outputTabLayout = QtWidgets.QVBoxLayout(self.outputTab)
        self.outputTabLayout.setContentsMargins(0, 0, 0, 0)
        self.outputTabLayout.setObjectName("outputTabLayout")
        self.outputWidget = QtWidgets.QPlainTextEdit(self.outputTab)
        self.outputWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.outputWidget.setTabChangesFocus(True)
        self.outputWidget.setUndoRedoEnabled(False)
        self.outputWidget.setReadOnly(True)
        self.outputWidget.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByKeyboard
            | QtCore.Qt.LinksAccessibleByMouse
            | QtCore.Qt.TextBrowserInteraction
            | QtCore.Qt.TextSelectableByKeyboard
            | QtCore.Qt.TextSelectableByMouse
        )
        self.outputWidget.setCenterOnScroll(True)
        self.outputWidget.setObjectName("outputWidget")
        self.outputTabLayout.addWidget(self.outputWidget)

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.addTab(self.resultsTab, "")
        self.tabWidget.addTab(self.outputTab, "")
        self.tabWidget.setCurrentIndex(0)
        self.centralLayout.addWidget(self.tabWidget)

        # Actions
        self.actionCollapse_all = QtWidgets.QAction(self)
        self.actionCollapse_all.setObjectName("actionCollapse_all")
        self.actionCollapse_all.triggered.connect(self.resultsTreeWidget.collapseAll)
        self.actionExpand_all = QtWidgets.QAction(self)
        self.actionExpand_all.setObjectName("actionExpand_all")
        self.actionExpand_all.triggered.connect(self.resultsTreeWidget.expandAll)
        self.actionRun = QtWidgets.QAction(self)
        self.actionRun.setObjectName("actionRun")
        self.actionAbort = QtWidgets.QAction(self)
        self.actionAbort.setObjectName("actionAbort")
        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(QtWidgets.QApplication.instance().quit)
        self.actionConfigure = QtWidgets.QAction(self)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionLine_profiler_documentation = QtWidgets.QAction(self)
        self.actionLine_profiler_documentation.setObjectName(
            "actionLine_profiler_documentation"
        )
        self.actionLine_profiler_documentation.triggered.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl(LINE_PROFILER_DOC_URL))
        )
        self.actionAbout_Qt = QtWidgets.QAction(self)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionAbout_Qt.triggered.connect(QtWidgets.QApplication.aboutQt)

        # Menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        # Profiling menu
        self.menuProfiling = QtWidgets.QMenu(self.menubar)
        self.menuProfiling.setObjectName("menuProfiling")
        self.menuProfiling.addAction(self.actionConfigure)
        self.menuProfiling.addSeparator()
        self.menuProfiling.addAction(self.actionRun)
        self.menuProfiling.addAction(self.actionAbort)
        self.menuProfiling.addSeparator()
        self.menuProfiling.addAction(self.actionQuit)
        self.menubar.addAction(self.menuProfiling.menuAction())

        # Display Menu
        self.menuDisplay = QtWidgets.QMenu(self.menubar)
        self.menuDisplay.setObjectName("menuDisplay")
        self.menuDisplay.addAction(self.actionCollapse_all)
        self.menuDisplay.addAction(self.actionExpand_all)
        self.menubar.addAction(self.menuDisplay.menuAction())

        # Help Menu
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.addAction(self.actionLine_profiler_documentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuHelp.menuAction())

        # Toolbar
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addAction(self.actionConfigure)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionAbort)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCollapse_all)
        self.toolBar.addAction(self.actionExpand_all)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # Finalization
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        self.update_window_title()
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.resultsTab), _("Profiling results"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.outputTab), _("Script Output"),
        )
        self.menuDisplay.setTitle(_("&Display"))
        self.menuProfiling.setTitle(_("&Profiling"))
        self.menuHelp.setTitle(_("&Help"))
        self.toolBar.setWindowTitle(_("toolBar"))
        self.actionCollapse_all.setText(_("&Collapse all"))
        self.actionExpand_all.setText(_("&Expand all"))
        self.actionRun.setText(_("&Run"))
        self.actionRun.setShortcut(_("F5"))
        self.actionAbort.setText(_("&Abort"))
        self.actionAbort.setShortcut(_("F6"))
        self.actionQuit.setText(_("&Quit"))
        self.actionQuit.setShortcut(_("Ctrl+Q"))
        self.actionConfigure.setText(_("&Configuration..."))
        self.actionConfigure.setToolTip(_("Configuration"))
        self.actionConfigure.setShortcut(_("Ctrl+O"))
        self.actionLine_profiler_documentation.setText(
            _("&Line profiler documentation...")
        )
        self.actionLine_profiler_documentation.setShortcut(_("F1"))
        self.actionAbout_Qt.setText(_("&About Qt..."))

    def update_window_title(self):
        title = _("Line Profiler GUI")
        if self.config.script:
            title += f" - {self.config.script}"
        self.setWindowTitle(title)

    def configure(self):
        Ui_ConfigDialog(self, self.config).exec()
        self.update_window_title()

    @QtCore.Slot()
    def on_actionConfigure_triggered(self):
        self.configure()

    @QtCore.Slot()
    def on_actionRun_triggered(self):
        ...

    @QtCore.Slot()
    def on_actionAbort_triggered(self):
        ...

    def set_running_state(self, state=True):
        self.start_button.setEnabled(not state)
        self.stop_button.setEnabled(state)


def main():
    # Manage arguments by hand : args will be passed to the python script
    args = sys.argv[1:]
    if args:
        if args[0] in ("-h", "--help"):
            print("Help !!!")
            return
        script = args[0]
        script_args = " ".join(args[1:])
    else:
        script = None
        script_args = ""

    # Create application
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QIcon(_WINDOW_ICON))

    # Create main window
    win = UI_MainWindow()
    if script:
        win.config.build_simple_config(script, script_args)
        win.update_window_title()
    else:
        win.configure()
    win.show()

    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
