#-*-coding: utf-8 -*-
from PyQt4 import QtCore, QtGui,QtNetwork

class GetAndSendWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(FtpWindow, self).__init__(parent)

        self.resize(400, 300)

        self.TotalSendBytes = 0
        self.TotalSaveBytes = 0
        self.bytesReceived = 0
        self.bytesWritten = 0
        self.fileToSave = None
        self.fileToSend = None
        self.PayloadSize = 65536

        self.tcpServer = QtNetwork.QTcpServer()
        self.tcpClient = QtNetwork.QTcpSocket()

        self.clientProgressBar = QtGui.QProgressBar()
        self.clientStatusLabel = QtGui.QLabel(u"客户端准备")
        self.serverProgressBar = QtGui.QProgressBar()
        self.serverStatusLabel = QtGui.QLabel(u"服务器端准备")

        self.startButton = QtGui.QPushButton(u"开始")
        self.fileButton = QtGui.QPushButton(u"文件")
        self.ipLineEdit = QtGui.QLineEdit()
        self.portSpinbox = QtGui.QSpinBox()
        self.portSpinbox.setMaximum(65535)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.addWidget(self.ipLineEdit)
        self.horizontalLayout.addWidget(self.portSpinbox)
        self.horizontalLayout.addWidget(self.startButton)
        self.horizontalLayout.addWidget(self.fileButton)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.headerItem().setText(0, u'文件名')
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.treeWidget.headerItem().setText(1, u'大小(B)')
        self.treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.treeWidget.headerItem().setText(2, u'修改日期')
        self.treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.treeWidget.headerItem().setText(3, u'传输状态')
        self.treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

        def selectFile():
            names = QtGui.QFileDialog.getOpenFileNames()
            self.treeWidget.clear()
            for name in names:
                info = QtCore.QFileInfo(name)
                self.treeWidget.addTopLevelItem(QtGui.QTreeWidgetItem([info.absoluteFilePath(),
                                                                       str(info.size()),
                                                                       info.lastModified().toString(),
                                                                       u'等待']))

        self.startButton.clicked.connect(self.start)
        self.fileButton.clicked.connect(selectFile)
        self.tcpServer.newConnection.connect(self.acceptConnection)
        self.tcpClient.connected.connect(self.startTransfer)
        self.tcpClient.bytesWritten.connect(self.updateClientProgress)
        self.tcpClient.error.connect(self.displayClientError)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.horizontalLayout)
        mainLayout.addWidget(self.treeWidget)
        mainLayout.addWidget(self.clientProgressBar)
        mainLayout.addWidget(self.clientStatusLabel)
        mainLayout.addWidget(self.serverProgressBar)
        mainLayout.addWidget(self.serverStatusLabel)
        self.setLayout(mainLayout)

        self.tcpServer.listen()
        while not self.tcpServer.isListening() and not self.tcpServer.listen():
            ret = QtGui.QMessageBox.critical(self, u"网络",
                                             u"无法进行监听: %s." % self.tcpServer.errorString(),
                                             QtGui.QMessageBox.Retry | QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Cancel:
                return
        self.serverStatusLabel.setText(u"监听")
        self.tcpServer.setMaxPendingConnections(1)
        self.ipLineEdit.setText(self.tcpServer.serverAddress().toString())
        self.portSpinbox.setValue(self.tcpServer.serverPort())
        self.setWindowTitle(self.ipLineEdit.text() + ':' + self.portSpinbox.text())

    def start(self):
        if not self.treeWidget.topLevelItemCount():
            QtGui.QMessageBox.critical(self, u"网络", u"没有指定任何文件进行发送.")
            return

        if self.tcpClient.isOpen():
            self.tcpClient.close()

        self.startButton.setEnabled(False)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.clientStatusLabel.setText(u"正在连接")
        self.tcpClient.connectToHost(self.ipLineEdit.text(), self.portSpinbox.value())

    def acceptConnection(self):
        self.tcpServerConnection = self.tcpServer.nextPendingConnection()
        self.tcpServerConnection.readyRead.connect(self.updateServerProgress)
        self.tcpServerConnection.error.connect(self.displayServerError)

        self.bytesReceived = 0
        self.TotalSaveBytes = 0
        self.fileToSave = None

        self.serverStatusLabel.setText(u"服务器准备接收文件...")
        #self.tcpServer.close()

    def startTransfer(self):
        self.treeWidgetIndex = 0
        self.sendFile(self.treeWidget.topLevelItem(self.treeWidgetIndex).text(0))
        self.clientStatusLabel.setText(u"客户端建立连接")

    def sendFile(self, filename):
        self.fileToSend = QtCore.QFile(filename)
        if not self.fileToSend.open(QtCore.QIODevice.ReadOnly):
            self.clientStatusLabel.setText(u"客户端错误: " + self.fileToSend.errorString())
            print self.fileToSend.fileName()
            return

        self.bytesWritten = 0
        self.TotalSendBytes = 0

        head = QtCore.QByteArray()
        stream = QtCore.QDataStream(head, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_0)
        stream.writeUInt32(self.fileToSend.size())
        print 'C: fileToSend = ' + str(self.fileToSend.size())
        info = QtCore.QFileInfo(self.fileToSend.fileName())
        stream.writeQString(info.fileName())
        print 'C: fileName = ' + info.fileName()

        self.TotalSendBytes = self.fileToSend.size() + head.size()
        print 'C: TotalSendBytes = '+str(self.TotalSendBytes)
        self.tcpClient.write(head)

    def getNewFile(self):
        self.bytesReceived = 0
        self.TotalSaveBytes = 0
        self.fileToSave = 0

        stream = QtCore.QDataStream(self.tcpServerConnection)
        stream.setVersion(QtCore.QDataStream.Qt_4_0)

        if self.tcpServerConnection.bytesAvailable() < 32:
            return

        filesize = stream.readUInt32()
        print 'S: Begin getting new file'
        print 'S: ' + str(filesize)
        self.bytesReceived = 4 # 32bit = 4Byte

        filename = stream.readQString()
        print 'S: ' + filename
        # The string length in bytes (quint32) followed by the data in UTF-16
        self.bytesReceived += 4 + 2 * filename.length()

        # For now we have already received the whole head block
        self.TotalSaveBytes = self.bytesReceived + filesize
        print 'S: TotalSaveBytes = ' + str(self.TotalSaveBytes)
        print 'S: ' + str(self.bytesReceived)
        self.fileToSave = QtCore.QFile(filename)
        if not self.fileToSave.open(QtCore.QIODevice.WriteOnly):
            self.serverStatusLabel.setText(u"无法保存文件:%s" + self.fileToSave.errorString())
            return

    def updateServerProgress(self):
        if self.fileToSave is None or not self.fileToSave.isOpen():
            self.getNewFile()
            return

        if self.tcpServerConnection.bytesAvailable() + self.bytesReceived <= self.TotalSaveBytes:
            self.bytesReceived += self.tcpServerConnection.bytesAvailable()
            self.fileToSave.write(self.tcpServerConnection.readAll())

            self.serverProgressBar.setMaximum(self.TotalSendBytes)
            self.serverProgressBar.setValue(self.bytesReceived)
            self.serverStatusLabel.setText("Received %dKB" % (self.bytesReceived / 1024))

            if self.bytesReceived == self.TotalSendBytes:
                print 'S: Done!'
                self.fileToSave.close()

        else:
            print 'S: New file!'
            print 'S: TotalSaveByte = '+str(self.TotalSaveBytes), 'bytesAvailable = '+str(self.tcpServerConnection.bytesAvailable())
            self.fileToSave.write(self.tcpServerConnection.read(self.TotalSaveBytes - self.bytesReceived))
            self.fileToSave.close()
            self.getNewFile()

        print 'S: bytesReceived = ' + str(self.bytesReceived)

    def updateClientProgress(self, numBytes):
        self.bytesWritten += numBytes
        print 'C: numBytes = ' + str(numBytes)

        if self.bytesWritten == self.TotalSendBytes:
            print 'C: Done!'
            self.treeWidget.topLevelItem(self.treeWidgetIndex).setText(3, u'完成')
            self.treeWidgetIndex += 1
            if self.treeWidgetIndex < self.treeWidget.topLevelItemCount():
                self.sendFile(self.treeWidget.topLevelItem(self.treeWidgetIndex).text(0))
            else:
                self.startButton.setEnabled(True)
                QtGui.QApplication.restoreOverrideCursor()
        else:
            self.tcpClient.write(self.fileToSend.read(self.PayloadSize))

        self.clientProgressBar.setMaximum(self.TotalSendBytes)
        self.clientProgressBar.setValue(self.bytesWritten)
        self.clientStatusLabel.setText("Sent %dKB" % (self.bytesWritten / 1024))

    def displayClientError(self, socketError):
        if socketError == QtNetwork.QTcpSocket.RemoteHostClosedError:
            QtGui.QApplication.restoreOverrideCursor()
            return

        QtGui.QMessageBox.information(self, u"网络故障",
                                      u"客户端网络错误: %s." % self.tcpClient.errorString())

        self.tcpClient.close()
        if self.fileToSend is not None:
            self.fileToSend.close()
        self.clientProgressBar.reset()
        self.clientStatusLabel.setText(u"客户端就绪.")
        self.startButton.setEnabled(True)
        QtGui.QApplication.restoreOverrideCursor()


    def displayServerError(self, socketError):
        if socketError == QtNetwork.QTcpSocket.RemoteHostClosedError:
            self.tcpServerConnection.close()
            return

        QtGui.QMessageBox.information(self, u"网络故障",
                                      u"服务端网络错误: %s." % self.tcpServerConnection.errorString())

        self.tcpServer.close()
        self.fileToSave.close()
        self.serverProgressBar.reset()
        self.serverStatusLabel.setText(u"本地服务端就绪.")

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    Win = GetAndSendWindow()
    Win.show()
    sys.exit(Win.exec_())
