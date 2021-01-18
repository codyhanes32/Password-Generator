import tkinter as tk
from tkmacosx import Button
import random
from cryptography.fernet import Fernet
import getpass
from os import path

HEIGHT = 450
WIDTH = 800

root = tk.Tk()
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

class App:
    numEntries=0

    def __init__(self):
        self.frame = tk.Frame(root, bg="black")
        self.frame.place(relwidth=1, relheight=1)
        self.addInfo()

    def addInfo(self):
        self.entries=[]
        self.label = tk.Label(self.frame, text="Submit at least 2 words and 1 number", font=('times', 15), fg='red', bg='black')
        self.label.place(relx=.03, rely=.1)
        self.entry = tk.Entry(self.frame, borderwidth=1, highlightbackground='red')
        self.entry.place(relx=.09,rely=.2, relheight=.08, relwidth=.2)
        self.button = Button(self.frame, text="Enter", bg='red', fg='white', command=lambda:self.get_entries(self.entries,self.entry.get()))
        self.button.place(relx=.15, rely=.3, relheight=.065, relwidth=.08)
        self.example = tk.Label(self.frame, text="Examples", font=('times',13), fg='white', bg='black')
        self.example.place(relx=.15, rely=.4)
        self.words = tk.Label(self.frame, text="(sports team, color, favorite number, college,",
                              font=('times',13), fg='red', bg='black')
        self.words.place(relx=.05, rely=.45)
        self.words2 = tk.Label(self.frame, text="           year born, movie, occupation)",
                              font=('times', 13), fg='red', bg='black')
        self.words2.place(relx=.05, rely=.49)
        self.getPassLabel = tk.Label(self.frame, text="OR",font=('times',27), bg='black', fg='white')
        self.getPassLabel.place(relx=.16, rely =.61)
        self.passwordButton = Button(self.frame, text="Decrypt Password",
                                     font=('times', 20), command=self.decryptPass, bg='green', fg='white')
        self.passwordButton.place(relx=.05, rely=.79, relheight=.12, relwidth = .3)

    def decryptPass(self):
        self.enxryptLabel = tk.Label(self.frame, text="Enter encrypted text", font=('times',15), bg='black', fg='red')
        self.enxryptLabel.place(relx=.58, rely=.79)
        self.encryptEntry = tk.Entry(self.frame)
        self.encryptEntry.place(relx=.38, rely=.85, relheight=.04, relwidth=.6)
        self.submitButton = Button(self.frame, text="Enter", font=('times', 13),
                                   command=lambda: self.getEncrypt(self.encryptEntry.get()))
        self.submitButton.place(relx=.64, rely=.91, relheight=.04, relwidth=.06)

    def getEncrypt(self, encryption):
        try:
            key = self.load_key()
            f = Fernet(key)
            editedPass = encryption[1:]
            encryptedPass = editedPass.encode('utf-8')
            encrypted_message = f.decrypt(encryptedPass)
            self.enxryptLabel.destroy()
            self.encryptEntry.destroy()
            self.submitButton.destroy()
            self.passwordLabel = tk.Label(self.frame, text="Password:", font=('times', 30), bg='black', fg='white')
            self.passwordLabel.place(relx=.57, rely=.75)
            self.decryptedPass = tk.Label(self.frame, text=encrypted_message, font=('times',25), bg='black', fg='green')
            self.decryptedPass.place(relx=.55, rely=.84)
        except:
            self.errorLabel = tk.Label(self.frame, text="Error, not found", font=('times',15), bg='black', fg='red')
            self.errorLabel.place(relx=.75, rely=.92)


    def get_entries(self, entries, category):
        self.entries.append(category)
        self.entry.delete(0,tk.END)
        self.numEntries+=1
        if self.numEntries==3:
            self.passButton = Button(self.frame, text="Generate Password", bg='green', borderwidth=0,
                               relief='raised', fg='black', font=('times', 25), command=self.generatePassword)
            self.passButton.place(relx=.45, rely=.14, relheight=.17, relwidth=.4)

    def generatePassword(self):
        self.pw=""
        try:
            while self.entries:
                self.lenList= len(self.entries)-1
                rand = random.randint(0,self.lenList)
                self.pw += self.entries[rand]
                self.entries.pop(rand)
            self.pword = list(self.pw)
            self.password=[]
            for i in self.pword:
                j = i.replace(' ', '')
                self.password.append(j)

            changes=2
            prev=0

            self.changeLetter(self.password)
            self.capitalize(self.password)
            self.doubleNumber(self.password)

            genPass=""
            for i in self.password:
                genPass+=i
            self.nameLabel = tk.Label(self.frame, text="Password:", font=('helvetica', 23), bg='black', fg='white')
            self.nameLabel.place(relx=.42, rely=.34)
            self.passLabel = tk.Label(self.frame, text=genPass, font=('helvetica', 25), bg='black', fg='red')
            self.passLabel.place(relx=.58, rely=.34)
            self.saveButton = tk.Button(self.frame, text="Save password", command=lambda: self.savePass(self.password))
            self.saveButton.place(relx=.47, rely=.46)
            self.deleteButton = tk.Button(self.frame, text="delete password",
                                           command=lambda: self.deletePass(self.passLabel, self.saveButton, self.deleteButton))
            self.deleteButton.place(relx=.66, rely=.46)
        except:
            self.exceptLabel = tk.Label(self.frame, text="Error: Enter required fields to generate new password",
                                        bg='black', font=('times', 13), fg='red')
            self.exceptLabel.place(relx=.42, rely=.55)
            var = tk.IntVar()
            self.R1 = tk.Radiobutton(root, text="", variable=var, value=1, bg='black',
                             command=lambda:sel(self.exceptLabel, self.R1))
            self.R1.place(relx=.76, rely=.55, relwidth=.04, relheight=.04)

            def sel(exceptLabel,R1):
                self.exceptLabel.destroy()
                self.R1.destroy()

    def deletePass(self, passLabel, saveButton, deleteButton):
        self.passLabel.destroy()
        self.saveButton.destroy()
        self.deleteButton.destroy()

    def savePass(self, password):
        self.applicationLabel = tk.Label(self.frame, text="What application will this password be used for?", bg='black',
                                    fg='white', font=('times',13))
        self.applicationLabel.place(relx=.3, rely=.56)
        self.applicationEntry = tk.Entry(self.frame)
        self.applicationEntry.place(relx=.634, rely=.56, relheight=.05)
        self.applicationButton = Button(self.frame, text="Submit", borderwidth=0, bg='gray',
                                   command=lambda:self.storePass(self.password))
        self.applicationButton.place(relx=.88,rely=.56, relwidth=.065)

    def storePass(self, password):
        appEntry = self.applicationEntry.get()
        str=""
        for i in self.password:
            str+=i
        key = self.load_key()
        message = str.encode()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        username = getpass.getuser()
        try:
            file = open(f'/Users/{username}/Desktop/passwords.txt','x')
        except:
            file = open(f'/Users/{username}/Desktop/passwords.txt','a')
            file.write(f'App - {appEntry}    Pass - {encrypted}')
        finally:
            self.successLabel = tk.Label(self.frame, text="Successfuflly saved!", bg='black', fg='green', font=('helvetica',20))
            self.successLabel.place(relx=.5, rely=.64)



    def load_key(self):
        if not path.exists("secret.key"):
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
        return open("secret.key", "rb").read()

    def changeLetter(self, password):
        self.letters= ["a","s","o"]
        rand = random.randint(0,2)
        self.letter=self.letters[rand]

        tries=5
        change=False
        while tries > 0:
            i=0
            for let in self.password:
                if self.letter == let:
                    if let == "s":
                        self.password[i] = "$"
                        change=True
                        break
                    elif let == "a":
                        self.password[i] = "@"
                        change=True
                        break
                    elif let == "o":
                        self.password[i] = "*"
                        change=True
                        break
                i+=1
            if change:
                break
            rand = random.randint(0,2)
            self.letter = self.letters[rand]
            tries-=1

    def doubleNumber(self, password):
        for i in range(0,len(self.password)):
            if password[i].isnumeric():
                self.password.append(self.password[i])
                if not self.password[i+1].isnumeric():
                    break

    def capitalize(self,password):
        nums=3
        while nums != 0:
            rand = random.randint(0, len(self.password) - 1)
            if not self.password[rand].isnumeric():
                self.password[rand] = self.password[rand].upper()
            nums-=1


def main():
    application = App()
    root.mainloop()

if __name__ == '__main__':
    main()
