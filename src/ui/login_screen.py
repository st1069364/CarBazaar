
from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("CarBazaar")
root.iconbitmap("images/CarBazaar_logo.png")
root.configure(bg="white")
root.geometry("450x600")


my_img = ImageTk.PhotoImage(Image.open("images/CarBazaar_logo.png") )
my_lab2 = Label(image=my_img,bg='white')
my_lab2.place(x=250,y=100,anchor=CENTER)

frame = LabelFrame(root,padx=10,pady=50,bg="white")
frame.place(x=100,y=200)
e1=Entry(frame,width=20,bg="white")
e1.insert(0,"example@email.com")
e2=Entry(frame,width=20,bg="white")
e2.insert(0,"*********")
button_1= Button(frame,text="Sign In",width=20,bg="red",fg="white").grid(row=6,column=0,pady=5)
button_2= Button(frame,text="Google",bg="gray",fg="white",width=10).grid(row=10,column=0)
button_3= Button(frame,text="Facebook",bg="Blue",fg="white",width=10).grid(row=10,column=1)
e1.grid(row=3,column=0,pady=4)
e2.grid(row=5,column=0,pady=4)
label_1=Label(frame,text="Sign in",fg="red",bg="white",anchor="nw").grid(row=0,column=0)
label_2=Label(frame,text="Hi there! Welcome to CarBazaar",fg="gray",bg="white").grid(row=1,column=0)
label_3=Label(frame,text="Email",fg="red",bg="white").grid(row=2,column=0,pady=4)
label_4=Label(frame,text="password",fg="red",bg="white").grid(row=4,column=0,pady=4)
label_5=Label(frame,text="sing in using",fg='red',bg='white').grid(row=8,column=0,padx=5,pady=4 )
label_6=Label(frame,text="Forgot Password?",fg="red",bg="white").grid(row=12,column=0)
label_7=Label(frame,text="Sign up",fg="red",bg="white").grid(row=12,column=1)


root.mainloop()
