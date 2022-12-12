import pickle
from Database_Object import DatabaseObject


def insert_obj(tree, value):
    last_obj = get_last_obj()
    new_obj = DatabaseObject(int(last_obj.index) + 1, value)
    tree.insert(new_obj)

    with open('data.dat', 'rb') as file:
        file.seek(0)
        data_from_file = pickle.load(file)
    data_from_file.append(new_obj)
    with open('data.dat', 'wb') as file:
        file.seek(0)
        pickle.dump(data_from_file, file)


def edit_obj(tree, index, new_value):
    old_obj = DatabaseObject(index, 'no_val')
    tree.edit(old_obj, new_value)

    with open('data.dat', 'rb') as file:
        file.seek(0)
        data_from_file = pickle.load(file)
    data_from_file[int(old_obj.index)] = DatabaseObject(old_obj.index, new_value)
    with open('data.dat', 'wb') as file:
        file.seek(0)
        pickle.dump(data_from_file, file)


def search_obj(tree, value):
    return tree.search(value)


def delete_obj(tree, index, value):
    tree.delete(tree.root, DatabaseObject(index, value))
    with open('data.dat', 'rb') as file:
        file.seek(0)
        data_from_file = pickle.load(file)
    data_from_file.remove(DatabaseObject(index, value))
    with open('data.dat', 'wb') as file:
        file.seek(0)
        pickle.dump(data_from_file, file)


def get_last_obj():
    with open('data.dat', 'rb') as file:
        file.seek(0)
        data_from_file = pickle.load(file)
    return data_from_file[-1]
