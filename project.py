from pathlib import Path
import os

def create_folder():
    name=input("Enter Folder name:-")
    p = Path(name)
    if p.exists():
        print("Folder alredy exist  try again")
        create_folder()
    else:
        p.mkdir()
        print("New folder created successfully!")





def read_folder():
    p = Path("")
    items = list(p.rglob("*"))
    return items

    # for i in range(len(items)):
    #     print(f"{i+1}:{items[i]}")





def update_folder():
    items=read_folder()
    for i in items:
            i = str(i)
            for j in i :
                if j == ".":
                    break
            else:
                print(i)
    name = input("Which folder you want to update:-")
    old_p = Path(name)

    if old_p.exists():
        new_name = input("Enter Your new name:-")
        new_p = Path(new_name)
        old_p.rename(new_p)
        print("Updated successfully")

    else:
        print("name not exist try again")
        update_folder()





def delete_folder():
    name=input("Enter Folder name:-")
    p = Path(name)
    if not p.exists():
        print("Folder doesn't exist  try again")
        delete_folder()
    else:
        p.rmdir()
        print("Folder deleted successfully!")




def create_file():
    name = input("Tell Your file name with extension:-")
    p = Path(name)
    if p.exists() and p.is_file():
        print("File name Already exist please try again")
        create_file()
    else:
        with open(p,"w") as fs:
            data = input("What do yo want to write:-")
            fs.write(data)
            print("File Created successfully")

    



def read_file():
    items = read_folder()
    for i in items:
        p = Path(i)
        if p.is_file():
            print(i)

    name = input("Which file you want to read:-")
    p = Path(name)
    if p.exists() and p.is_file():
        with open (p,"r") as fs:
            data = fs.read()
            print("\n\n\n\nyour file content is\n\n\n\n")
            print(data)
    else:
        print("no such file exist please try again")
        read_file()





def updating_file():
    items = read_folder()
    for i in items:
        p = Path(i)
        if p.is_file():
            print(i)

    name = input("Tell your file name:-")
    p = Path(name)
    if p.exists() and p.is_file():
        print("Choose one option")
        print("Press 1 to change the name")
        print("Press 2 to overwrite the file content")
        print("Press 3 to append new content")

        res = int(input("Tell your response:-"))

        if res == 1:
            new_name = input("Tell new name with extension")
            new_p = Path(new_name)
            p.rename(new_p)
            print("File name change successfully")

        elif res == 2:
            with open(p,"w") as fs:
                data = input("What do you want to overwrite:-")
                fs.write(data)
                print("overwritten successfully")

        elif res == 3:
            with open(p,"a") as fs:
                data = input("What do you want to overwrite:-")
                fs.write(data)
                print("Appended successfully")



def delete_file():
    item = read_folder()
    for i in items:
        p = Path(i)
        if p.is_file():
            print(i)

    name = input("Tell your file name with extension:-")
    p = Path(name)
    if p.exists() and p.is_file():
        os.remove(p)
    else:
        print("no such file exxists please try again")
        delete_file()    


print("Press 1 - for creating a folder")
print("Press 2 - for reading  a folder")
print("Press 3 - for updating a folder")
print("Press 4 - for deleting a folder")


print("Press 5 - for creating a file")
print("Press 6 - for reading  a file")
print("Press 7 - for updating a file")
print("Press 8 - for deleting a file")


res = int(input("Tell your response:-"))

if res == 1:
    create_folder()



if res == 2:
    items = read_folder()
    for i in range(len(items)):
        print(f"{i+1}:{items[i]}")



if res == 3:
    update_folder()



if res == 4:
    delete_folder()



if res == 5:
    create_file()



if res == 6:
    read_file()


if res == 7:
    updating_file()


if res == 8:
    delete_file()