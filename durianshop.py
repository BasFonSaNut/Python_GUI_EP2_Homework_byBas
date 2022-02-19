from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from db import Database

db = Database('store.db')


def sold_list():
    #เรียกโครงสร้างข้อมูลใน ๒sqlite ขึ้นมา แล้วเคลียร์ดาต้าที่ค้างอยู่ไปก่อน
    sell_list.delete(0, END)
    for row in db.fetch():
        sell_list.insert(END, row)


def add_item():
    if quantity_text.get() == '' or priceperkilo_text.get() == '' or totalprice_text.get() == '':
        messagebox.showerror('ว่างไม่ได้ครับ', 'ต้องมีค่าหมดทุกข้อมูล')
        return
    db.insert(quantity_text.get(), priceperkilo_text.get(),
              totalprice_text.get())
    sell_list.delete(0, END)
    sell_list.insert(END, (quantity_text.get(), priceperkilo_text.get(),
                            totalprice_text.get()))
    clear_text()
    sold_list()


def select_item(event):
    try:
        global selected_item
        index = sell_list.curselection()[0]
        selected_item = sell_list.get(index)

        quantity_entry.delete(0, END)
        quantity_entry.insert(END, selected_item[1])
        
        priceperkilo_entry.delete(0, END)
        priceperkilo_entry.insert(END, selected_item[2])
        
        totalprice_entry.delete(0, END)
        totalprice_entry.insert(END, selected_item[3])
        
    except IndexError:
        pass

def calculate_item():
    if quantity_text.get() == '' or priceperkilo_text.get() == '':
        messagebox.showerror('ว่างไม่ได้ครับ', 'ขอจำนวนกิโล กับ ราคาต่อกิโล ครับ')
        return
    quantity = quantity_text.get()
    priceperkilo = priceperkilo_text.get()
    totalprice_text.set(float(quantity) * float(priceperkilo))
    
    
def remove_item():
    db.remove(selected_item[0])
    clear_text()
    sold_list()


def update_item():
    db.update(selected_item[0], quantity_text.get(), priceperkilo_text.get(),
              totalprice_text.get())
    sold_list()


def clear_text():
    quantity_entry.delete(0, END)
    priceperkilo_entry.delete(0, END)
    totalprice_entry.delete(0, END)


# สร้าง window object
app = Tk()

# จำนวน
quantity_text = StringVar()
quantity_label = Label(app, text='จำนวน', font=('Angsana New',25,BOLD), pady=20)
quantity_label.grid(row=0, column=0, sticky=W)
quantity_entry = Entry(app, textvariable=quantity_text,font=('Angsana New',20))
quantity_entry.grid(row=0, column=1)

# ราคาต่อหน่วย
priceperkilo_text = StringVar()
priceperkilo_label = Label(app, text='ราคาต่อกิโล', font=('Angsana New',25,BOLD))
priceperkilo_label.grid(row=0, column=2, sticky=W)
priceperkilo_entry = Entry(app, textvariable=priceperkilo_text,font=('Angsana New',20))
priceperkilo_entry.grid(row=0, column=3)

# ราคารวมต่อรายการ
totalprice_text = StringVar()
totalprice_label = Label(app, text='ยอดรวมต่อรายการ', font=('Angsana New',25,BOLD))
totalprice_label.grid(row=1, column=0, sticky=W)
totalprice_entry = Entry(app, textvariable=totalprice_text,font=('Angsana New',20))
totalprice_entry.grid(row=1, column=1)


sell_list = Listbox(app, height=8, width=50, border=0)
sell_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# สร้าง scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# กำหนดว่า scroll นี้ผูกกับ control ไหน
sell_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=sell_list.yview)
# เอา listbox ไปยัดไว้ใน scroll
sell_list.bind('<<ListboxSelect>>', select_item)

# สร้างปุ่ม
calculate_btn = Button(app, text='คำนวณราคา', width=12, command=calculate_item)
calculate_btn.grid(row=2, column=0, pady=20)

add_btn = Button(app, text='เพิ่มรายการ', width=12, command=add_item)
add_btn.grid(row=2, column=1, pady=5)

remove_btn = Button(app, text='ลบรายการ', width=12, command=remove_item)
remove_btn.grid(row=2, column=2)

update_btn = Button(app, text='แก้ไขรายการ', width=12, command=update_item)
update_btn.grid(row=2, column=3)

clear_btn = Button(app, text='ล้างรายการ', width=12, command=clear_text)
clear_btn.grid(row=2, column=4)

app.title('รายการซื้อขายทุเรียน')
app.geometry('800x550')

# เรียกโครงสร้างข้อมูลใน sqlite ขึ้นมา แล้วเคลียร์ดาต้าที่ค้างอยู่ไปก่อน
sold_list()

# Start program
app.mainloop()

