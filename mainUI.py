'''
USER INTERFACE OF PROJECT: LPC ANALYSIS
created: Rajesh R, MS Research Scholar, IIT Mandi
'''
import sys
import os
import soundfile as sf
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

#Make sure the backend .py is included before running
import LPCModule

'''
THIS CLASS IS TO PLOT VARIOUS PLOTS IN THE UI
'''
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

'''
MAIN UI CLASS
'''
class userinterface(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    # This function contains all the codes for layouts, buttons, labels, tabs etc
    def initUI(self):

        self.layout = QHBoxLayout(self)

        lbl1 = QLabel('Input Parameters for Generating Audio', self)
        lbl1.setStyleSheet("border: 1px solid black;")
        lbl1.setAlignment(Qt.AlignCenter)

        self.parametersLayout1 = QHBoxLayout(self)
        self.parametersLayout2 = QHBoxLayout(self)

        self.fText = QLineEdit('0.125')
        fTextlbl = QLabel('frequency')

        self.fsText = QLineEdit('8000')
        fsTextlbl = QLabel('Sampling freq')

        self.tsText = QLineEdit('2')
        tsTextlbl = QLabel('Time period')

        btn1 = QPushButton('Generate an Audio', self)

        lbl2 = QLabel('Load Existing Audio from System', self)
        lbl2.setStyleSheet("border: 1px solid black;")
        lbl2.setAlignment(Qt.AlignCenter)

        btn2 = QPushButton('Choose an Audio file', self)
        btn3 = QPushButton('Play file', self)

        lbl3 = QLabel('Spectrum Analysis', self)
        lbl3.setStyleSheet("border: 1px solid black;")
        lbl3.setAlignment(Qt.AlignCenter)

        lpcbtn = QPushButton('Perform LPC Coding', self)

        lbl4 = QLabel('LPC Compression', self)
        lbl4.setAlignment(Qt.AlignCenter)
        lbl4.setStyleSheet("border: 1px solid black;")

        self.avalframes = QLabel('Available Frames: ', self)

        self.spectrumLayout1 = QHBoxLayout(self)
        self.spectrumLayout2 = QHBoxLayout(self)

        framenolbl = QLabel('Frame', self)
        self.frameno = QLineEdit('15', self)
        orderlbl = QLabel('Order', self)
        self.order = QLineEdit('16', self)

        pltbtn = QPushButton('Plot', self)


        # Buttons layout
        self.buttonsLayout = QVBoxLayout()

        self.buttonsLayout.addWidget(lbl1)

        self.buttonsLayout.addLayout(self.parametersLayout1)
        self.parametersLayout1.addWidget(fTextlbl)
        self.parametersLayout1.addWidget(fsTextlbl)
        self.parametersLayout1.addWidget(tsTextlbl)
        self.buttonsLayout.addLayout(self.parametersLayout2)
        self.parametersLayout2.addWidget(self.fText)
        self.parametersLayout2.addWidget(self.fsText)
        self.parametersLayout2.addWidget(self.tsText)

        self.buttonsLayout.addWidget(btn1)

        self.buttonsLayout.addWidget(lbl2)


        self.buttonsLayout.addWidget(btn2)
        self.buttonsLayout.addWidget(btn3)
        self.buttonsLayout.addWidget(lbl4)
        self.buttonsLayout.addWidget(lpcbtn)
        self.buttonsLayout.addWidget(lbl3)

        self.buttonsLayout.addWidget(self.avalframes)

        self.buttonsLayout.addLayout(self.spectrumLayout1)
        self.spectrumLayout1.addWidget(framenolbl)
        self.spectrumLayout1.addWidget(self.frameno)

        self.buttonsLayout.addLayout(self.spectrumLayout2)
        self.spectrumLayout2.addWidget(orderlbl)
        self.spectrumLayout2.addWidget(self.order)

        self.buttonsLayout.addWidget(pltbtn)



        # Tab Layout
        self.tabsLayout = QHBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Time Analysis")
        self.tabs.addTab(self.tab2, "Frequency Analysis")
        self.tabs.addTab(self.tab3, "Computation Results")
        #self.tabs.addTab(self.tab4, "Steps")

        # first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)

        # second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.setLayout(self.tab2.layout)

        # Third tab
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)

        # fourth tab
        self.tab4.layout = QHBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)

        # Add tabs to widget
        self.tabsLayout.addWidget(self.tabs)
        self.layout.addLayout(self.buttonsLayout)
        self.layout.addLayout(self.tabsLayout)

        self.setLayout(self.layout)


        #self.setGeometry(600, 600, 1024, 720)
        self.setWindowTitle('Linear Predictive Analysis of Speech Signals')

        # Methods for triggered operations
        btn2.clicked.connect(self.open)
        btn3.clicked.connect(self.playaudio)
        lpcbtn.clicked.connect(self.performLPC)
        pltbtn.clicked.connect(self.plotspect)
        btn1.clicked.connect(self.audiogeneration)


        self.show()

    '''
    THIS FUNCTION USED WHEN LOAD BUTTON IS CLICKED
    '''
    def open(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                                'All Files (*.*)')
        if self.path != ('', ''):
            print("File path : " + self.path[0])

        try:
            x, y = LPCModule.timePlot(self.path[0])
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.plot(x, y)
            self.toolbar = NavigationToolbar(sc, self)
            self.tab1.layout.addWidget(sc)
            self.tab1.layout.addWidget(self.toolbar)

            self.no_of_frames = LPCModule.frameno(self.path[0])
            self.avalframes.setText('Available Frames: 0 to '+str(self.no_of_frames-1))
            #self.buttonsLayout.addWidget(avalframes)

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Loading Audio!!!")
            msg.setText("OOPS! \nAN ERROR OCCURED WHILE LOADING AUDIO\nPlease select an Audio (.wav) file to proceed!")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    '''
    THIS FUNCTION USED TO PLAY AUDIO
    '''
    def playaudio(self):
        try:
            print(self.path[0])
            self.player = QMediaPlayer()
            url = QUrl.fromLocalFile(self.path[0])
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Occured!!!")
            msg.setText("How do you expect to play without loading the audio?\nPlease load audio to proceed")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    '''
    THIS FUNCTION USED TO PLAY OUTPUT AUDIO
    '''
    def PlayOutFile(self):
        print(self.rpath)
        self.player = QMediaPlayer()
        url = QUrl.fromLocalFile(self.rpath)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    '''
    THIS FUNCTION PERFORMS LPC ANALYSIS
    '''
    def performLPC(self):
        try:
            reduced_val, self.rpath = LPCModule.shorttimeprocessing(self.path[0])
            s1 = QLabel('Result', self)
            s1.setAlignment(Qt.AlignCenter)
            text = 'Speech compressed by {}%'.format(str(reduced_val))
            s2 = QLabel(text, self)
            s2.setAlignment(Qt.AlignCenter)

            Oplaybtn = QPushButton('Play Resulted Audio', self)

            self.tab3.layout.addWidget(s1)
            self.tab3.layout.addWidget(s2)
            self.tab3.layout.addWidget(Oplaybtn)

            Oplaybtn.clicked.connect(self.PlayOutFile)

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Occured!!!")
            msg.setText("OOPS! AN ERROR OCCURED WHILE PERFORMING TASK\n(1)Please check if audio is loaded\n(2)Maybe resulted in ill-conditioned system")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    '''
    THIS FUNCTION USED TO PLOT THE LPC & FFT SPECTRUM
    '''
    def plotspect(self):
        try:
            print("frame no: ", self.frameno.text())
            print("LPC Order: ", self.order.text())

            x1, y1, x2, y2 = LPCModule.sprectrumvectors(self.path[0], int(self.frameno.text()), int(self.order.text()))
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.plot(x1, y1)
            sc.axes.plot(x2, y2)
            sc.axes.legend(['LPC Envelope', 'DFT Spectrum'])
            self.toolbar = NavigationToolbar(sc, self)
            self.tab2.layout.addWidget(sc)
            self.tab2.layout.addWidget(self.toolbar)

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Occured!!!")
            msg.setText("OOPS! AN ERROR OCCURED WHILE PERFORMING TASK\n(1)Please check if audio is loaded\n(2)Recheck the frame no/order number is in range & int data type")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    '''
    THIS FUNCTION GENERATES AUDIO
    '''
    def audiogeneration(self):
        try:
            print("frequency: ", self.fText.text())
            print("Sampling frequency: ", self.fsText.text())
            print("tsec: ", self.tsText.text())
            f = float(self.fText.text())
            fs = int(self.fsText.text())
            ts = int(self.tsText.text())
            audio = LPCModule.generate_audio(f, fs, ts)
            sf.write('GeneratedAudio.wav', audio, fs)
            path = os.path.join(os.getcwd(), 'GeneratedAudio.wav')
            self.path = [path, '']
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Occured!!!")
            msg.setText("OOPS! AN ERROR OCCURED WHILE GENERATING AUDIO\n(1)Please check f (in float), fs and ts (in int)")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        try:
            x, y = LPCModule.timePlot(self.path[0])
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.plot(x, y)
            self.toolbar = NavigationToolbar(sc, self)
            self.tab1.layout.addWidget(sc)
            self.tab1.layout.addWidget(self.toolbar)

            self.no_of_frames = LPCModule.frameno(self.path[0])
            self.avalframes.setText('Available Frames: 0 to ' + str(self.no_of_frames - 1))
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error Occured!!!")
            msg.setText("OOPS! AN ERROR OCCURED WHILE PERFORMING TASK\nError raisen in time plot and in framing the speech")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()



def main():
    app = QApplication(sys.argv)
    ex = userinterface()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
