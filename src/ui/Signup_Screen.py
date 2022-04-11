from tkinter import *

root = Tk()
root.title("CarBazaar")
root.iconbitmap("images/CarBazaar_logo.png")
root.configure(bg="white")
root.geometry("350x400")

frame = LabelFrame(root,bg='white').grid()
label_1 = Label(frame,text="Sign up",fg='red',bg='white').grid(row=0,column=0,pady=5)
label_2=Label(frame,text="Email",bg='white',fg='red').grid(row=1,column=0,pady=5)
label_3 =Label(frame,text='Password',bg='white',fg='red').grid(row=3,column=0,pady=5)
label_4=Label(frame,text='Have An Account? Sign In',bg='white',fg='gray').grid(row=7,column=0,pady=5)
e1=Entry(frame,width=20,bg='white').grid(row=2,column=0,pady=5)
e2 =Entry(frame,width=20,bg='white').grid(row=4,column=0,pady=10,padx=5)
c = Checkbutton(frame,text="   I agree to the Terms of Services and \n Privacy Policy",bg='white').grid(row=5,column=0,padx=5,pady=5)
button_1=Button(frame,text='Continue',width=20,bg='red',fg='white').grid(row=6,column=0,padx=5,pady=5)

root.mainloop()