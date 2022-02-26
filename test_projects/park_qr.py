from asyncio.windows_events import NULL
from time import sleep
import cv2
import pyzbar.pyzbar as pyzbar
from face_recognition.api import face_locations
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv

def Parking(name):
    with open('parking.csv','r+') as f:
         myDataList = f.readlines()
         nameList = []
         for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
         if name not in nameList:
            now = datetime.now()
            dString = now.strftime('%H:%M:%S')
            #f.writelines(f'\n{name},{dString}')
            f.writelines(f'{name},{dString}')

def EndParking(name):
    lines = list()
    with open('parking.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if row != []:
                lines.append(row)
            print(row)
            if name in row:
                lines.remove(row)


    with open('parking.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)




cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
buffer = 0
mode = ['park','no park']
passkey = 'park'
while True:
    
    if(passkey == mode[0]):
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        # for obj in decodedObjects:
        #     print("Data", obj.data)
        #     cv2.putText(frame, "Parking Taken", (50, 200), font, 2,(0, 0, 255), 3)
        #     cv2.putText(frame, str(obj.data), (50, 100), font, 2,(0, 0, 255), 3)
        # cv2.imshow('Frame',frame)
        for obj in decodedObjects:
            print("Type:", obj.type)
            print("Data: ", obj.data, "\n")
            string = str(obj.data)
            test= string.strip("\\n'")
            #path = "C:\\Users\\hpadmin\\Desktop\\New folder\\"+str(obj.data)
            #path = "C:\\Users\\hpadmin\\Desktop\\New folder\\b'1BG19CS014'"
            path = "C:\\Users\\hpadmin\\Desktop\\New folder\\"+test+"'"

            for file in os.listdir(path):
                if file.endswith(".txt"):
                    file_path = f"{path}\{file}"
            current_file = open(file_path, "r")
            #print(current_file.read())
            ticket = current_file.read()
            print(ticket)
            print("Match Found!")
            Parking(ticket)
            passkey = mode[1]
            if obj.data != NULL:
                for obj in decodedObjects:
                    print("Data", obj.data)
                    cv2.putText(frame, "Parking Taken", (50, 200), font, 2,(0, 0, 255), 3)
                    cv2.putText(frame, str(obj.data), (50, 100), font, 2,(0, 0, 255), 3)
                buffer = 10000
        
        if buffer:
            while buffer>0:        
                cv2.imshow('Frame',frame)
                buffer-=1
            continue
        
        cv2.imshow('Frame',frame)
      
        
            
            

    if(passkey == mode[1]):
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        # for obj in decodedObjects:
        #     print("Data", obj.data)
        #     cv2.putText(frame, "Bill Generated", (50, 200), font, 2,(0, 0, 255), 3)
        #     cv2.putText(frame, str(obj.data), (50, 100), font, 2,(0, 0, 255), 3)
        for obj in decodedObjects:
            print("Type:", obj.type)
            print("Data: ", obj.data, "\n")
            string = str(obj.data)
            test= string.strip("\\n'")
            #path = "C:\\Users\\hpadmin\\Desktop\\New folder\\"+str(obj.data)
            #path = "C:\\Users\\hpadmin\\Desktop\\New folder\\b'1BG19CS014'"
            path = "C:\\Users\\hpadmin\\Desktop\\New folder\\"+test+"'"

            for file in os.listdir(path):
                if file.endswith(".txt"):
                    file_path = f"{path}\{file}"
            current_file = open(file_path, "r")
            #print(current_file.read())
            ticket = current_file.read()
            print(ticket)
            print("Bill generated! Pay up please!")
            EndParking(ticket)
            passkey=mode[0]
            if obj.data != NULL:
                for obj in decodedObjects:
                    print("Data", obj.data)
                    cv2.putText(frame, "Bill Generated", (50, 200), font, 2,(0, 0, 255), 3)
                    cv2.putText(frame, str(obj.data), (50, 100), font, 2,(0, 0, 255), 3)
                buffer=10000
                
        if buffer:
            while buffer>0:        
                cv2.imshow('Frame',frame)
                buffer-=1
            continue
        
        cv2.imshow('Frame',frame) 

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows() 