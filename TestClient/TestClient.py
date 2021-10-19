from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import requests

class ListView(QWidget):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.setWindowTitle('Asphodel Downloader Test Client')
        self.resize(400, 100)
        self.initUI()

    def append(self):
        """
        채팅을 추가함
        """
        res = requests.get(f"http://112.151.179.200:7474/publicchat/append/{self.appendChatInput.text()}").json()

    def get(self):
        """
        클라에 보관된 해시가 없으면 그냥 보내서 10개 받아오고,
        클라에 해시가 보관되어 있으면 그거 보내서 필요한 부분만 받아옴
        """
        if self.currentLastHashViewer.text() == '':
            res = requests.get("http://112.151.179.200:7474/publicchat/get").json()
            self.addItemList(res)
        else:
            res = requests.get(f"http://112.151.179.200:7474/publicchat/get?hash={self.currentLastHashViewer.text()}").json()
            self.addItemList(res)

    def addItemList(self, res):
        """
        [[해시, 텍스트]] 형식의 리스트를 리스트뷰에 넣어줌
        역순으로 리스트를 전달받으므로, 역순으로 한번 뒤집어줌
        그리고 마지막 해시는 해시 뷰어에 넣어줌
        """
        for n, r in enumerate(reversed(res)):
                self.chatting.addItem(str(r))
                if n + 1== len(res):
                    self.currentLastHashViewer.setText(str(r[0]))
            
    def save(self):
        """
        API에 저장하라고 시킴
        """
        requests.get("http://112.151.179.200:7474/publicchat/save")
 
    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.chatting = QListWidget()

        self.currentLastHashTitle = QLabel('currentLastHash : ')
        self.currentLastHashViewer = QLineEdit()

        self.hashes = QHBoxLayout()
        self.hashes.addWidget(self.currentLastHashTitle)
        self.hashes.addWidget(self.currentLastHashViewer)

        self.getChat = QPushButton('getChat')
        self.getChat.clicked.connect(self.get)

        self.appendChatInput = QLineEdit()
        self.appendChatInput.setPlaceholderText('Input text to send')
        self.appendChat = QPushButton('appendChat')
        self.appendChat.clicked.connect(self.append)

        self.saveBTN = QPushButton('SAVE')
        self.saveBTN.clicked.connect(self.save)
        
        self.mainLayout.addWidget(self.chatting)
        self.mainLayout.addWidget(self.getChat)
        self.mainLayout.addLayout(self.hashes)
        self.mainLayout.addWidget(self.appendChatInput)
        self.mainLayout.addWidget(self.appendChat)
        self.mainLayout.addWidget(self.saveBTN)

        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ListView()
    window.show()
    sys.exit(app.exec())