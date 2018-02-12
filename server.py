import socket
import sys
import os
import glob
import time
import random
import threading
import requests
import grab

def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def clear():
    with open(bat_dir, 'w'): pass
    files = glob.glob(code_dir+'*')
    for f in files:
        os.remove(f)    
    files = glob.glob(compiled_dir+'*')
    for f in files:
        os.remove(f)  

def ascomp(bat_dir):
    os.system(bat_dir)
    os.system("exit") 
    time.sleep(2)

def changewifi(wifiname):
    os.system('netsh wlan connect name='+'"'+str(wifiname)+'"')
    os.system("exit") 
    time.sleep(7)

def send2flash(a_compiled):
    t = threading.Thread(target=changewifi, args=("SanDisk Connect F08152",))
    t.daemon = True
    t.start()
    t.join() 
    del4flash()  
    for i in range(len(a_compiled)):
        print(a_compiled[i])
        with open(a_compiled[i], "rb") as fh:
            mydata = fh.read()
            cs=a_compiled[i]
            b = os.path.getsize(a_compiled[i])
            b=str(b) 
            print(b)
            r = requests.put('http://172.25.63.1/myconnect/'+cs[cs.rfind("//")+1:],
                                     data=mydata,                         
                               headers={'Content-Type':'',"X-AirStash-Date":"2018-01-22 11:52:14+0-300","lastModified":1516525420053,"lastModifiedDate":'',"name":cs[cs.rfind("//")+1:],"size":int(b),"type":"", "webkitRelativePath":""},
                               params={'file': a_compiled[i]}
                               )  
            print(cs[cs.rfind("//")+2:])
        time.sleep(3)
    print("Sending to flash completed") 
    t = threading.Thread(target=changewifi, args=(wifi_phone_server,))
    t.daemon = True
    t.start()
    t.join()  

def del4flash():
    g = grab.Grab()
    g.go('http://172.25.63.1/myconnect/')
    text = g.css_text('body')
    text=text.split()
    already=0
    for i in range(len(text)):
        if text[i]=='Size' or already==1:
            if already==0:
                already=1
                continue
            else:
                r = requests.delete('http://172.25.63.1/myconnect/'+text[i]) 
    
bat_dir = 'C://server//maketp.bat'
code_dir = 'C://server//uploaded_files//'
compiled_dir = 'C://server//compiled_files//'
wifi_phone_server = "228"
wifi_flash = "SanDisk Connect F08152"

#accepting connections 
t = threading.Thread(target=changewifi, args=(wifi_phone_server,))
t.daemon = True
t.start()
t.join() 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 62888
s.bind(("192.168.43.243",port))
s.listen(10)
file_index,a_compiled=0,[]   
print("Server started!")
clear()
while True:    
    connection_ended = 0
    file_index+=1
    currentconnect, address = s.accept()
    print("Success connect by: "+str(address))     
    #accepting code
    code_name = "needchange"+str(file_index)+".ls"
    f = open(code_dir+code_name,'wb') 
    currentPartOfFile = 1
    while(currentPartOfFile):
        currentPartOfFile = currentconnect.recv(1024)
        if currentPartOfFile==b"Sent": #sending compiled files
            f.close()       
            #compiling code
            t = threading.Thread(target=ascomp, args=(bat_dir,))
            t.daemon = True
            t.start()
            t.join()          
            #send to flash
            send2flash(a_compiled)
            a_compiled=[]
            #clear all before next picture
            connection_ended = 1
            break
        while (currentPartOfFile):
            f.write(currentPartOfFile)
            currentPartOfFile = currentconnect.recv(1024)
    f.close()
    if(not connection_ended==1):
        #get name of prog
        with open(code_dir+code_name) as f:
            try:
                content = [x.strip("\n") for x in f.readlines()]  
            except:
                print(code_name)
            for i in range(len(content)):
                if content[i].count('/PROG')==1:
                    print(content[i])
                    content[i] = content[i].split()
                    nameOfProg = content[i][len(content[i])-1]
                    break
            print("Activity number: " + str(file_index))
        #change name of file to name from prog
        os.rename(code_dir + code_name, code_dir + nameOfProg + '.ls')
        code_name = nameOfProg + '.ls'
        compiled_name = code_name[:len(code_name)-3] + '.tp'
        #creating bat file
        if os.stat(bat_dir).st_size == 0:
            with open(bat_dir, 'a') as bat_file:
                bat_file.write('call setrobot.exe')
        #append to bat file
        with open(bat_dir, 'a') as bat_file:
            bat_file.write('\ncall maketp.exe ' + code_dir.replace("//","/") + code_name + ' '+ compiled_dir.replace("//","/") + compiled_name)
        a_compiled.append(compiled_dir+compiled_name)
        currentconnect.close()
    else:
        currentconnect.close()
s.close()