import pickle
from tkinter import messagebox
import Tree_interaction
from tkinter import *
from tkinter import ttk
from B_Tree import BTree


class GUI:
    def __init__(self):
        self.tree = self.__create_tree()
        self.runner()

    def runner(self):
        root = Tk()
        root.title("Lab 3")
        root.geometry("800x500+600+250")

        options_menu = ttk.Notebook()
        options_menu.pack(expand=True, fill=BOTH)

        insert = self.create_option(options_menu, "Insert")
        edit = self.create_option(options_menu, "Edit")
        self.search = self.create_option(options_menu, "Search")
        self.label_search_value = ttk.Label(self.search, font=('Arial', 13))
        self.label_search_value.pack()
        delete = self.create_option(options_menu, "Delete")

        self.configure_insert(insert)
        self.configure_edit(edit)
        self.configure_search()
        self.configure_delete(delete)

        self.display_tree()
        self.tree = self.__create_tree()

        root.mainloop()

    def __create_tree(self):
        data_from_file = self.read_file()

        tree = BTree()
        for piece in data_from_file:
            tree.insert(piece)

        return tree

    def create_option(self, menu, name):
        option = ttk.Frame(menu)
        option.pack(fill=BOTH, expand=True)
        menu.add(option, text=name)
        return option

    def display_tree(self):
        data_from_file = self.read_file()
        table = ttk.Treeview(columns=('id', 'value'), show="headings")
        table.pack(side=LEFT, fill=BOTH)
        col1 = table.heading('id', text='id')
        table.heading('value', text='value')
        for piece in data_from_file:
            table.insert("", END, values=(piece.index, piece.value))
        table.place(x=380, y=25, relwidth=0.5, relheight=0.9)
        scrollbar = ttk.Scrollbar(table, command=table.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=table.yview)
        table.config(yscrollcommand=scrollbar.set)

    def read_file(self):
        with open('data.dat', "rb") as file:
            data_from_file = pickle.load(file)
            file.close()
        return data_from_file

    def configure_insert(self, frame):
        label_enter_value = ttk.Label(frame, text="Enter new value:", font=('Arial', 13))
        label_enter_value.pack()
        label_enter_value.place(x=20, y=26)
        self.insert_enter = ttk.Entry(frame, font=('Arial', 13))
        self.insert_enter.pack()
        self.insert_enter.place(x=160, y=24)
        btn = Button(frame, text="  Insert  ", command=self.insert_value_to_tree, font=('Arial', 13))
        btn.pack()
        btn.place(x=160, y=60)

    def insert_value_to_tree(self):
        inserted_value = self.insert_enter.get()
        Tree_interaction.insert_obj(self.tree, inserted_value)
        self.tree = self.__create_tree()
        self.display_tree()

    def configure_edit(self, frame):
        label_edit_index = ttk.Label(frame, text="Enter index:", font=('Arial', 13))
        label_edit_index.pack()
        label_edit_index.place(x=20, y=26)
        self.edit_index_enter = ttk.Entry(frame, font=('Arial', 13))
        self.edit_index_enter.pack()
        self.edit_index_enter.place(x=160, y=24)
        label_edit_new_value = ttk.Label(frame, text="Enter new value:", font=('Arial', 13))
        label_edit_new_value.pack()
        label_edit_new_value.place(x=20, y=74)
        self.edit_new_value_enter = ttk.Entry(frame, font=('Arial', 13))
        self.edit_new_value_enter.pack()
        self.edit_new_value_enter.place(x=160, y=72)
        btn = Button(frame, text="  Edit  ", command=self.edit_tree_value, font=('Arial', 13))
        btn.pack()
        btn.place(x=160, y=130)

    def edit_tree_value(self):
        index = self.edit_index_enter.get()
        new_value = self.edit_new_value_enter.get()
        if index.isnumeric():
            Tree_interaction.edit_obj(self.tree, index, new_value)
            self.tree = self.__create_tree()
            self.display_tree()
        else:
            messagebox.showwarning(title='Incorrect input', message='The index must be a positive integer.\nTry again.')

    def configure_search(self):
        label_search_value = ttk.Label(self.search, text="Enter the value:", font=('Arial', 13))
        label_search_value.pack()
        label_search_value.place(x=20, y=26)
        self.search_enter = ttk.Entry(self.search, font=('Arial', 13))
        self.search_enter.pack()
        self.search_enter.place(x=160, y=24)
        btn = Button(self.search, text="  Search  ", command=self.search_tree_value, font=('Arial', 13))
        btn.pack()
        btn.place(x=160, y=60)

    def search_tree_value(self):
        search_value = str(self.search_enter.get())
        result = Tree_interaction.search_obj(self.tree, search_value)
        if result is None:
            self.label_search_value.config(text="Value not found.")
            self.label_search_value.place(x=160, y=110)
            print(self.tree.counter)
            self.tree.counter = 0
        else:
            self.label_search_value.config(text=f"Index: {result.index}\nValue: {result.value}")
            self.label_search_value.place(x=160, y=110)
            print(self.tree.counter)
            self.tree.counter = 0

    def configure_delete(self, frame):
        label_delete_index = ttk.Label(frame, text="Enter index:", font=('Arial', 13))
        label_delete_index.pack()
        label_delete_index.place(x=20, y=26)
        self.delete_index_enter = ttk.Entry(frame, font=('Arial', 13))
        self.delete_index_enter.pack()
        self.delete_index_enter.place(x=170, y=24)
        label_edit_value = ttk.Label(frame, text="Enter deleted value:", font=('Arial', 13))
        label_edit_value.pack()
        label_edit_value.place(x=20, y=74)
        self.delete_value_enter = ttk.Entry(frame, font=('Arial', 13))
        self.delete_value_enter.pack()
        self.delete_value_enter.place(x=170, y=72)
        btn = Button(frame, text="  Delete  ", command=self.delete_tree_value, font=('Arial', 13))
        btn.pack()
        btn.place(x=160, y=130)

    def delete_tree_value(self):
        index = self.delete_index_enter.get()
        value = self.delete_value_enter.get()
        if index.isnumeric():
            Tree_interaction.delete_obj(self.tree, index, value)
            self.tree = self.__create_tree()
            self.display_tree()
        else:
            messagebox.showwarning(title='Incorrect input', message='The index must be a positive integer.\nTry again.')