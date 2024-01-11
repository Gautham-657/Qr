#  Gautham D  04/22


# modules
from logging import exception
from tkinter import messagebox
from turtle import fillcolor
from email.message import EmailMessage
import smtplib
from click import command
import qrcode
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkmacosx import Button
try:
    from google.cloud import storage
    import google.cloud.storage
    import json
    import os
    import sys
except exception as e:
    print("Missing libriaries are {}".format(e))

# Gcloud auth
PATH = os.path.join(os.getcwd(),"high-codex-348005-db158670ea13.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH

storage_client = storage.Client.from_service_account_json(PATH)
print(storage_client)

# Bucket
bucket = storage_client.get_bucket("ram-vakil")
    

# tkinter creation
root = Tk()
root.title("QR CODE GENERATOR")
root.configure(background='grey')


text = Entry(root,width=50,text="URL or Text")
text.grid(row=0,column=0,pady=5)

image1 =PhotoImage(file="new.png")
display = Label(root,image=image1) 
display.grid(row=2,column=0,pady=5)

# Generates a QR code
def makeQr(event):
    global image1
    img = qrcode.make(event)
    img.save("new.png")
    image1 =PhotoImage(file="new.png")
    display.configure(image=image1)
    linkText.delete('1.0',END)
    linkText.insert(INSERT,event)
    # root.update()

# Generate Button
generate = Button(root,text="Generate QR code",command=lambda:makeQr(text.get()),highlightbackground='#808080')
generate.grid(row=1,column=0)

# Append to Json

def write_json(data,fileName = "linksStorage.json"):
    with open (fileName,'w') as f:
        json.dump(data,f,indent=4)

# Open file
def open_file(): 
    file = askopenfile(mode ='r') 
    if file is not None: 
        print(file.name)
        makeQr(file)
        blob = bucket.blob(file.name)
        with open(file.name,'rb') as f:
            try:
                blob.upload_from_file(f)
                fileNew = "https://storage.googleapis.com/{}/{}".format("ram-vakil",file.name)

                makeQr(fileNew)
                displayLink(fileNew)
                print("Completed!")

                if text.get() != "":
                    with open ("linksStorage.json") as json_files:
                        data1 = json.load(json_files)
                        temp = data1["paths"]
                        y = {"key":str(text.get()),"link":fileNew}
                        temp.append(y)
                        text.delete(0,END)
                    write_json(data1)
            except exception as e:
                print(e)
        # print(content) 



# Link display
linkText = Text(root,width=50,height=3,wrap=WORD)
linkText.grid(row=4,column=0,pady=5)

def displayLink(llink):
    linkText.delete('1.0',END)
    linkText.insert(INSERT,llink)
    

btn = Button(root, text ='Select File',highlightbackground='#808080' ,command = lambda:open_file()) 
btn.grid(row=3,column=0,pady=5,sticky='ns')


# def findSearch():
#     findButton = Button(searchWindow,text="Find",command=lambda:searchResult())
#     findButton.grid(row=1,column=0)
    
m=0
def searchResult():
    try:
        global m
        f = open("linksStorage.json")
        data1 = json.load(f)
        for i in data1['paths']:
            for keys in i:
                if keys == 'key' and text.get() == i[keys]:
                    m = 1
                    continue

                if m==1:
                    makeQr(i[keys])
                    m=0
                    break
    except:
        messagebox.showinfo(title='Invalid Key', message='Invalid Key')

search1 = Button(root,text="Search",highlightbackground='#808080',command = lambda:searchResult())
search1.grid(row=3,column=0,pady=5,sticky='e')


# Email



email = "ramdatabase81@gmail.com"
passw = "$ram$data"



def sendEmail2():
    lst = text.get()
    lst1 = lst.split(',')
    # try:
    linkEmail = ""
    global m
    f = open("linksStorage.json")
    data1 = json.load(f)
    for i in data1['paths']:
        for keys in i:
            if keys == 'key' and textEmail.get() == i[keys]:
                m = 1
                continue
            if m==1:
                linkEmail = i[keys]
                m=0
                break
    print(linkEmail)

    for em in lst1:
        print(em)
        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("ramdatabase81@gmail.com","$ram$data")
        server.sendmail("ramdatabase81@gmail.com",em,str(linkEmail))
        print("Sent")


textEmail = Entry(root,width=50)
textEmail.grid(row=6,column=0,pady=5)
def sendMail():
    newWi = Tk()
    sendButton = Button(newWi,text="Send",highlightbackground='#808080',command=sendEmail2)
    sendButton.grid(row=1,column=0)
    newWi.mainloop()

email = Button(root,text="Email",highlightbackground='#808080',command=sendEmail2)
email.grid(row=3,column=0,pady=5,sticky='w')


root.mainloop()