from tkinter import *

root = Tk()
root.title("CarBazaar")
root.iconbitmap("images/CarBazaar_logo.png")
root.configure(bg="white")
root.geometry("400x400")

Label1=Label(root,text='                                                         CarBazaar',fg='red',bg='white').grid()
button_1=Button(root,text ="Post Car Listing",bg="red",fg="white",width=18).grid(row=1,column=0,pady=5,padx=5)
button_2=Button(root,text="Schedule Car Check",bg="red",fg="white",width=18).grid(row=2,column=0,pady=5,padx=5)
button_3=Button(root,text="Car Search",bg="red",fg="white",width=18).grid(row=3,column=0,pady=5,padx=5)
button_4=Button(root,text="Find Nearby Dealerships",bg="red",fg="white",width=18).grid(row=4,column=0,pady=5,padx=5)
button_5=Button(root,text ="Buy Car",bg="red",fg="white",width=18).grid(row=5,column=0,pady=5,padx=5)
button_6=Button(root,text="Purchase Insurance Plan",bg="red",fg="white",width=18).grid(row=6,column=0,pady=5,padx=5)
button_7=Button(root,text="My Purchases",bg="red",fg="white",width=18).grid(row=7,column=0,pady=5,padx=5)
button_8=Button(root,text="My Test Drives",bg="red",fg="white",width=18).grid(row=8,column=0,pady=5,padx=5)
button_9=Button(root,text="My Listings",bg="red",fg="white",width=18).grid(row=9,column=0,pady=5,padx=5)
button_10=Button(root,text="Wishlist",bg="red",fg="white",width=18).grid(row=10,column=0,pady=5,padx=5)
button_11=Button(root,text="Post Spare Part Listing",bg="red",fg="white",width=18).grid(row=1,column=1,pady=5,padx=5)
button_12=Button(root,text ="Schedule Test Drive",bg="red",fg="white",width=18).grid(row=2,column=1,pady=5,padx=5)
button_13=Button(root,text="Spare Part Search",bg="red",fg="white",width=18).grid(row=3,column=1,pady=5,padx=5)
button_14=Button(root,text="Comprare Cars",bg="red",fg="white",width=18).grid(row=4,column=1,pady=5,padx=5)
button_15=Button(root,text="Car Exchange",bg="red",fg="white",width=18).grid(row=5,column=1,pady=5,padx=5)
button_16=Button(root,text ="Car Transportation",bg="red",fg="white",width=18).grid(row=6,column=1,pady=5,padx=5)
button_17=Button(root,text="My Car Checks",bg="red",fg="white",width=18).grid(row=7,column=1,pady=5,padx=5)
button_18=Button(root,text="My Car Transoportations",bg="red",fg="white",width=18).grid(row=8,column=1,pady=5,padx=5)
button_19=Button(root,text="My Messages",bg="red",fg="white",width=18).grid(row=9,column=1,pady=5,padx=5)
button_20=Button(root,text="Contact Us",bg="red",fg="white",width=18).grid(row=10,column=1,pady=5,padx=5)


root.mainloop()