# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import PyQt5
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from skpy import Skype
import threading
import datetime

todayDate = datetime.date.today().strftime("%Y-%m-%d")

class skypeUploader(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(skypeUploader, self).__init__()
        loadUi("skypeuploader.ui", self)
        self.show()
        self.setWindowTitle("Skype Uploader")
        self.setWindowIcon(QIcon("cat.ico"))
        
        self.lePassword.setEchoMode(QLineEdit.Password)
        
        self.pbSelectFile.clicked.connect(self.chooseFile)
        
        self.pbUpload.clicked.connect(self.handleUploadThread)
        
    # 加入現成避免程序阻塞
    def handleUploadThread(self):
        uploadThread = threading.Thread(target = self.upload)
        uploadThread.start()
        
    def chooseFile(self):
        # open choose file dialog
        fileDialog = QFileDialog();
        selectedFile, _= fileDialog.getOpenFileName(self, "選擇文件", "", "All Files (*)")       
        if selectedFile:
            self.lbFileChosen.setText(selectedFile)
    # 根據群組名稱取得群組 ID
    def getChatId(self):
        account = self.leAccount.text()
        password = self.lePassword.text()
        targetChatName = self.leChatName.text()
        if not targetChatName:
            return;
        print(account, password, targetChatName)
        try:
            sk = Skype(account, password)
        except Exception as err:
            print("發生錯誤:", str(err))
            self.lbStatus.setText("登陸失敗: %s" %err)
            return;
            
        chats = sk.chats.recent()
        while len(chats) > 0:
            for chat in chats.values():
                groupName = getattr(chat, "topic", "no attr")
                if groupName == targetChatName:
                    groupID = getattr(chat, "id")
                    print(groupID)
                    return groupID
            chats = sk.chats.recent()
            
    def setUiMode(self, status):
        if status == "executing":    
            self.leAccount.setEnabled(False)
            self.lePassword.setEnabled(False)
            self.leChatName.setEnabled(False)
            self.pbSelectFile.setEnabled(False)
            self.pbUpload.setEnabled(False)
        else:
            self.leAccount.setEnabled(True)
            self.lePassword.setEnabled(True)
            self.leChatName.setEnabled(True)
            self.pbSelectFile.setEnabled(True)
            self.pbUpload.setEnabled(True)
                    
        
    def upload(self):
        self.lbStatus.clear()
        self.setUiMode('executing');
        self.lbStatus.setText("目前進度: 正在取得群組 ID...")
        groupID = self.getChatId()
        self.lbStatus.setText("取得 ID: %s" %groupID)
        if groupID:
            account = self.leAccount.text()
            password = self.lePassword.text()
            filename = self.lbFileChosen.text()
         
            try:      
                if filename:
                    sk = Skype(account, password)
                    channel = sk.chats.chat(groupID)
                    channel.sendMsg(todayDate)
                    
                    self.lbStatus.setText("目前進度: 正在上傳檔案...")
                    channel.sendFile(open(filename, 'rb'), filename.split('/')[-1])
                    self.setUiMode('finish');
                    self.lbStatus.setText("上傳成功 !")
                else:
                    self.lbStatus.setText("錯誤: 未選擇上傳檔案")
                    self.setUiMode("show");
                    return;
                    
            except Exception as err:
                print("Error:", err)
                self.lbStatus.setText(err)
                return;
        else:
            self.setUiMode("show");
            self.lbStatus.setText("錯誤: 未找到群組")
            return;
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = skypeUploader()
    sys.exit(app.exec_())
        
    