from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
import random
import time
import datetime
import re
from main import Face_Recognition_System


def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()
    
    
class Login_Window:   
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x766+0+0")
        self.root.title("Login")
        
        self.bg=ImageTk.PhotoImage(file=r"college_images\best13.jpg")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)
        
        frame=Frame(self.root,bg="black")
        frame.place(x=513,y=170,width=340,height=450)
        
        img1=Image.open(r"college_images\LoginIconAppl.png")
        img1=img1.resize((100,100),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="black",borderwidth=0)
        lblimg1.place(x=633,y=175,width=100,height=100)
        
        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=97,y=100)
        
        # Label
        username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username.place(x=60,y=155)
        
        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)
        
        password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password.place(x=60,y=225)
        
        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=40,y=250,width=270)
        self.show_pass = False

        self.btn_eye = Button(frame,text="👁",font=("times new roman",10),bd=0,bg="white",cursor="hand2",command=lambda: (
        self.txtpass.config(show="" if not self.show_pass else "*"),
        setattr(self, "show_pass", not self.show_pass)))
        self.btn_eye.place(x=280, y=250)  # near password box
        
        
        
        #=====================Icon Image=============
        img2=Image.open(r"college_images\LoginIconAppl.png")
        img2=img2.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg1=Label(image=self.photoimage2,bg="black",borderwidth=0)
        lblimg1.place(x=550,y=323,width=25,height=25)
        
        img3=Image.open(r"college_images\lock-512.png")
        img3=img3.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg1=Label(image=self.photoimage3,bg="black",borderwidth=0)
        lblimg1.place(x=550,y=395,width=25,height=25)
        
        
        #===========Login Btn==================
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=90,y=300,width=160)
        
        #===========Register Btn==================
        registerbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160)
        
        #===========Forget Btn==================
        loginbtn=Button(frame,text="Forget Password",command=self.forget_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        loginbtn.place(x=10,y=370,width=160)
        
    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)
        
    def login(self):
        if self.txtuser.get=="" or self.txtpass.get()=="":
            messagebox.showerror("error","All fields Required")
        elif self.txtuser.get()=="kapu" and self.txtpass.get()=="ashu":
            messagebox.showinfo("Success","Login Successfully")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="admin23",database="mydata")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                                                                                    self.txtuser.get(),
                                                                                    self.txtpass.get()
                                                                            ))
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username & Password")
            else:
                open_main=messagebox.askyesno("YesNo","Access Only Admin")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Face_Recognition_System(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
            
#=============== Reset Pass ==================
    def reset_pass(self):
        if self.combo_security_Q.get()=="Select":
            messagebox.showerror("Error","Select Security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please enter the Answer",parent=self.root2)
        elif self.txt_newpass.get()=="":
            messagebox.showerror("Error","Please enter the New Password",parent=self.root3)
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="admin23",database="mydata")
            my_cursor=conn.cursor()
            qury=("select * from register where email=%s and securityQ=%s and securityA=%s")
            vlaue=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get(),)
            my_cursor.execute(qury,vlaue)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please Enter Correct Answer",parent=self.root2)
            else:
    # 🔐 password check
                if self.txt_newpass.get() == "" or self.txt_newpass1.get() == "":
                    messagebox.showerror("Error", "Please enter password in both fields", parent=self.root3)

                elif self.txt_newpass.get() != self.txt_newpass1.get():
                    messagebox.showerror("Error", "New Password and Confirm Password do not match", parent=self.root3)
                else:
                    query=("Update register set password=%s where email=%s")
                    value=(self.txt_newpass.get(),self.txtuser.get())
                    my_cursor.execute(query,value)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Info","Your Password has been reset, Please Login with new Password",parent=self.root2)
                    self.root2.destroy()
                    self.root3.destroy()  
#============ Forget Pass =======================
    def forget_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please Enter the Email Address to reset Password")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="admin23",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            #print(row)
            
            if row==None:
                messagebox.showerror("My Error","Please enter the Valid Username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+500+150")
                
                l=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)
                
                security_Q=Label(self.root2,text="Select Security Question",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_Q.place(x=50,y=80)
                
                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("Select","Your Birth Place","Your Girlfriend Name","Your Pet Name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)

                security_A=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_A.place(x=50,y=150)
                
                self.txt_security=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_security.place(x=50,y=180,width=250)
                
                btn=Button(self.root2,text="Change Password",command=self.change_password_window,font=("times new roman",15,"bold"),fg="white",bg="green")
                btn.place(x=140,y=290)
                
    #========New Pass Window============
    def change_password_window(self):
    # --- security question & answer checks ---
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error", "Select Security Question", parent=self.root2)
            return
        elif self.txt_security.get() == "":
            messagebox.showerror("Error", "Please enter the Answer", parent=self.root2)
            return
        else:
     # Verify the security question and answer from database
            conn = mysql.connector.connect(host="localhost", username="root", password="admin23", database="mydata")
            my_cursor = conn.cursor()
            query = "SELECT * FROM register WHERE email=%s AND securityQ=%s AND securityA=%s"
            value = (self.txtuser.get(), self.combo_security_Q.get(), self.txt_security.get())
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            conn.close()

        if row is None:
            messagebox.showerror("Error", "Incorrect Security Question or Answer", parent=self.root2)
            return

# --- only if above checks pass ---
        self.root3 = Toplevel(self.root)
        self.root3.title("Confirm Password")
        self.root3.geometry("340x450+500+150")
                
        l=Label(self.root3,text="Confirm Password",font=("times new roman",20,"bold"),fg="red",bg="white")
        l.place(x=0,y=10,relwidth=1)
                
        new_password=Label(self.root3,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        new_password.place(x=50,y=80)
                
        self.txt_newpass=ttk.Entry(self.root3,font=("times new roman",15),show="*")
        self.txt_newpass.place(x=50,y=110,width=250)
                
        new_password1=Label(self.root3,text="Confirm New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        new_password1.place(x=50,y=150)
                
        self.txt_newpass1=ttk.Entry(self.root3,font=("times new roman",15),show="*")
        self.txt_newpass1.place(x=50,y=180,width=250)
        self.show_pass = False

        self.btn_eye = Button(self.root3,text="👁",font=("times new roman",10),bd=0,bg="white",cursor="hand2",command=lambda: (
        self.txt_newpass.config(show="" if not self.show_pass else "*"),
        self.txt_newpass1.config(show="" if not self.show_pass else "*"),
        setattr(self, "show_pass", not self.show_pass)))
        self.btn_eye.place(x=270, y=180)
                
        btn=Button(self.root3,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="white",bg="green")
        btn.place(x=140,y=320)
                
    
                
class Register:   
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x766+0+0")
        self.root.title("Register")
        
        #=============== Variables ===================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_SecurityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()
        
        
        #==============bg Image=================
        self.bg=ImageTk.PhotoImage(file=r"college_images\login2.jpg")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)
        
        #==============left Image=================
        self.bg1=ImageTk.PhotoImage(file=r"college_images\thought-good-morning-messages-LoveSove.jpg")
        bg_lbl=Label(self.root,image=self.bg1)
        bg_lbl.place(x=50,y=100,width=470,height=550)
        
        #====================== Name Frame =====================
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)
        
        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        register_lbl.place(x=20,y=20)
        
        #================Label and Entry=======================
        
        # row 1
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)
        
        fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        fname_entry.place(x=50,y=130,width=250)
        
        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=100)
        
        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txt_lname.place(x=370,y=130,width=250)
        
        # row 2
        contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white",fg="black")
        contact.place(x=50,y=170)
        
        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)
        
        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=170)
        
        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)
        
        # row 3
        security_Q=Label(frame,text="Select Security Question",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_Q.place(x=50,y=240)
        
        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_Q["values"]=("Select","Your Birth Place","Your Girlfriend Name","Your Pet Name")
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)

        security_A=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_A.place(x=370,y=240)
        
        self.txt_security=ttk.Entry(frame,textvariable=self.var_SecurityA,font=("times new roman",15))
        self.txt_security.place(x=370,y=270,width=250)
        
        # row 4
        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        pswd.place(x=50,y=310)
        
        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15),show="*")
        self.txt_pswd.place(x=50,y=340,width=250)
        
        confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        confirm_pswd.place(x=370,y=310)
        
        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15),show="*")
        self.txt_confirm_pswd.place(x=370,y=340,width=250)
        self.show_pass = False

        self.btn_eye = Button(frame,text="👁",font=("times new roman",10),bd=0,bg="white",cursor="hand2",command=lambda: (
        self.txt_pswd.config(show="" if not self.show_pass else "*"),
        self.txt_confirm_pswd.config(show="" if not self.show_pass else "*"),
        setattr(self, "show_pass", not self.show_pass)))
        self.btn_eye.place(x=590, y=340)
        
        #================checkButton================
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I agree the Terms & Conditions",font=("times new eoman",12,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)
        
        #===============button========================
        img=Image.open(r"college_images\register-now-button1.jpg")
        img=img.resize((200,50),Image.Resampling.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2")
        b1.place(x=10,y=420,width=200)
        
        img1=Image.open(r"college_images\loginpng.png")
        img1=img1.resize((200,50),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=330,y=420,width=200)
        
        
       #==================== Function declaration ================ 
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="Select":
            messagebox.showerror("Error","All Fields are required")
            return
        # Email validation
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", self.var_email.get()):
            messagebox.showerror("Error","Invalid Email Format")
            return
        # Contact validation
        if not self.var_contact.get().isdigit() or len(self.var_contact.get()) != 10:
            messagebox.showerror("Error","Contact must be exactly 10 digits")
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","Password & Confirm Password must be same")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please Agree to Our Terms & Condition")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="admin23",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User Already Exist, Please try another Email")
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(

                                self.var_fname.get(),
                                self.var_lname.get(),
                                self.var_contact.get(),
                                self.var_email.get(),
                                self.var_securityQ.get(),
                                self.var_SecurityA.get(),
                                self.var_pass.get()
                                
                        ))
            conn.commit()
            conn.close()
        messagebox.showinfo("Success","Register Successfully")
            
    def return_login(self):
        self.root.destroy()
                   
if __name__ == "__main__":
    root=Tk()
    obj=Login_Window(root)
    root.mainloop()