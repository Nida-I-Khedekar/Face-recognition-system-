from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from time import  strftime
from datetime import datetime
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x766+0+0")
        self.root.title("face Recognition system")


        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",30,"bold"),bg="white",fg="green")
        title_lbl.place(x=0,y=0,width=1366,height=45)

#============ 1st Image==============
        img_top=Image.open(r"college_images\face_detector1.jpg")
        img_top=img_top.resize((650,660),Image.Resampling.LANCZOS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=650,height=660)

#============ 2nd Image==============
        img_bottom=Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
        img_bottom=img_bottom.resize((950,660),Image.Resampling.LANCZOS)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=600,y=55,width=950,height=660)

        # button
        b1_1=Button(f_lbl,text="FACE RECOGNITION",cursor="hand2",command=self.face_recog,font=("times new roman",13,"bold"),bg="darkgreen",fg="white")
        b1_1.place(x=365,y=580,width=200,height=40)
        
        
        #================attendance====================
    def mark_attendance(self,i,r,n,d):
        with open("nida1.csv","r+",newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list) ):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")
                
                


    #================ Face Recognition ===================

    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord=[]

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost",username="root",password="admin23",database="face_recognizer")
                my_cursor=conn.cursor()

                my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
                n = my_cursor.fetchone()
                if n:
                    n = n[0]  
                    n = str(n)  
                    result = '+' + n

                my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
                r = my_cursor.fetchone()
                if n:
                    r = r[0]  
                    r = str(r) 
                    result = '+' + r

                my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
                d = my_cursor.fetchone()
                if d:
                    d = d[0]  
                    d = str(d)  
                    result = '+' + n
                
                my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
                i = my_cursor.fetchone()
                if i:
                    i = i[0]  
                    i = str(i)   
                    result = '+' + n
                

                if confidence>77:
                    cv2.putText(img,f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                coord=[x,y,w,h]

            return coord
        
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img

        faceCascade=cv2.CascadeClassifier("C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap=cv2.VideoCapture(0)

        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to Face Recognition",img)

            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()        