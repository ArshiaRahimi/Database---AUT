# cli.py
import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(host="localhost", user="root", passwd="Cenation021", database="library")


def printChoicesForUsers():
    print("[1] SEE PERSONAL AND SYSTEMATIC INFO")
    print("[2] SEARCH FOR A BOOK")
    print("[3] BORROW A BOOK")
    print("[4] RETURN A BOOK")
    print("[5] INCREASE CASH")


def printChoicesForSTAFF():
    print("[1] ADD A BOOK")
    print("[2] ADD TO INVENTORY")
    print("[3] UPDATE INVENTORY")
    print("[4] USER SEARCH")
    print("[5] LIST OF SUCCESSFUL ATTEMPTS")
    print("[6] HISTORY OF A BOOK")
    print("[7] SEE USERS INFO")
    print("[8] SEE USERS HISTORY")
    print("[9] CHECK MAILBOX")


def printChoicesForBOSS():
    print("[1] ADD A BOOK")
    print("[2] ADD TO INVENTORY")
    print("[3] UPDATE INVENTORY")
    print("[4] USER SEARCH")
    print("[5] LIST OF SUCCESSFUL ATTEMPTS")
    print("[6] HISTORY OF A BOOK")
    print("[7] SEE USER'S INFO")
    print("[8] SEE USER'S HISTORY")
    print("[9] CHECK MAILBOX")
    print("[10] DELETE AN ACCOUNT")


def bookInsertion():
    print("#### BOOK INSERTION ####")
    book_id = input("Enter bookId: ")
    title = input("Enter title: ")
    category = input("Enter category: ")
    author = input("Enter author: ")
    edition = input("Enter book edition: ")
    price = input("Enter book price: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('insertIntoBook', (book_id, title, category, author, edition, price))
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(x[0][0])
    mydb.commit()


def inventoryInsertion():
    print("#### INVENTORY INSERTION ####")
    book_id = input("Enter bookId: ")
    date = input("Enter return date limit: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('insertIntoInventory', (book_id, date))
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(x[0][0])
    mydb.commit()


def updateInventory():
    print("#### UPDATING INVENTORY ####")
    book_id = input("Enter bookId: ")
    num = input("Enter number of books: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('updateInventory', (book_id, num))
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(x[0][0])
    mydb.commit()


def checkPassword(passwd):
    counter = 0
    haveNumber = False
    haveChar = False
    for i in passwd:
        counter += 1
        if i.isdigit():
            haveNumber = True
        if i.isalpha():
            haveChar = True
    if counter < 8 or haveChar is False or haveNumber is False:
        return False
    else:
        return True


def checkUserName(user):
    if len(user) < 6:
        return False
    else:
        return True


def checkField(user_name):
    cursor2 = mydb.cursor()
    cursor2.callproc('getField', (user_name, ))
    for result in cursor2.stored_results():
        x = result.fetchall()
    return x[0][0]

#print(checkField('yo_ganeh'))


def printInfo(user_name):
    cursor3 = mydb.cursor()
    cursor3.callproc('InfoRetrieve', (user_name, ))
    for result in cursor3.stored_results():
        x = result.fetchall()
    print("ID: " + str(x[0][0]))
    print("Username: " + str(x[0][1]))
    print("Password: " + str(x[0][2]))
    print("Created Date: " + str(x[0][3]))
    print("Balance: " + str(x[0][4]))
    print("Name: " + str(x[0][5]))
    print("Family Name: " + str(x[0][6]))
    print("type: " + str(x[0][7]))
    print(" ")


def printInbox():
    cursor3 = mydb.cursor()
    cursor3.callproc('showInbox')
    for result in cursor3.stored_results():
        x = result.fetchall()
    for i in range(len(x)):
        print("inbox id: " + str(x[i][0])+ " message: " + str(x[i][1]))


def userSearch():
    cursor5 = mydb.cursor()
    option = input("Enter [1] if you want to search by name or Enter [2] to search by family name: ")
    if option == '1':
        # search by name
        query = input("Enter name: ")
        cursor5.callproc('userSearch1', (query, ))
        for result in cursor5.stored_results():
            x = result.fetchall()
        neededPages = int(len(x)/5) + 1
        pages = [i+1 for i in range(neededPages)]
        exit = True
        while exit is not False and len(x) != 0:
            choice = input("Choose between Pages: " + str(pages) + " Or enter q to quit: ")
            if choice == 'q':
                exit = False
                continue
            print("page:" + str(choice))
            print("   id |   name |   family |   type")
            for i in range((int(choice)-1)*5, (int(choice)-1)*5 + 5):
                if i in range(len(x)):
                    print(x[i])

    elif option == '2':
        # search by family name
        query = input("Enter Family name: ")
        cursor5.callproc('userSearch2', (query, ))
        for result in cursor5.stored_results():
            x = result.fetchall()
        neededPages = int(len(x) / 5) + 1
        pages = [i + 1 for i in range(neededPages)]
        exit = True
        while exit is not False and len(x) != 0:
            choice = input("Choose between Pages: " + str(pages) + " Or enter q to quit: ")
            if choice == 'q':
                exit = False
                continue
            print("page:" + str(choice))
            print("   id |   name |   family |   type")
            for i in range((int(choice) - 1) * 5, (int(choice) - 1) * 5 + 5):
                if i in range(len(x)):
                    print(x[i])
    else:
        print("You entered the wrong Option!")



def listSuccessfulHistory():
    cursor6 = mydb.cursor()
    cursor6.callproc('successfulResults')
    for result in cursor6.stored_results():
        x = result.fetchall()
    neededPages = int(len(x) / 5) + 1
    pages = [i + 1 for i in range(neededPages)]
    exit = True
    while exit is not False and len(x) != 0:
        choice = input("Choose between Pages: " + str(pages) + " Or enter q to quit: ")
        if choice == 'q':
            exit = False
            continue
        print("page:" + str(choice))
        print('id | hid | bid | result | start date | returned date')
        for i in range((int(choice) - 1) * 5, (int(choice) - 1) * 5 + 5):
            if i in range(len(x)):
                print(x[i])


def updateCash(uname):
    cursor2 = mydb.cursor()
    money = input("Enter amount to add to cash: ")
    cursor2.callproc('updateUserCash', (uname, money))
    for result in cursor2.stored_results():
        x = result.fetchall()
    mydb.commit()
    print(x[0][0])


def borrow(user_name):
    bookId = input("Enter book id to borrow: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('borrowBook', (user_name, bookId))
    for result in cursor3.stored_results():
        x = result.fetchall()
    mydb.commit()


def returnBook(user_name):
    bookId = input("Enter book id to return: ")
    date = input("Enter returned date")
    cursor3 = mydb.cursor()
    cursor3.callproc('returnBook', (user_name, bookId, date))
    for result in cursor3.stored_results():
        x = result.fetchall()
    mydb.commit()


def successResults():
    cursor3 = mydb.cursor()
    cursor3.callproc('successfulResults')
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(tabulate(x, headers=['id', 'history_id', 'book_id', 'result', 'start date', 'returned date'], tablefmt='psql'))


def bookHistory():
    bookId = input("Enter book id to view it's history: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('bookHistory', (bookId, ))
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(tabulate(x, headers=['id', 'history_id', 'book_id', 'result', 'start date', 'returned date'], tablefmt='psql'))

def seeHistory():
    cursor3 = mydb.cursor()
    cursor3.callproc('seeHistory')
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(tabulate(x, headers=['id', 'history_id', 'book_id', 'result', 'start date', 'returned date'], tablefmt='psql'))


def seeUsers():
    cursor3 = mydb.cursor()
    cursor3.callproc('seeUsers')
    for result in cursor3.stored_results():
        x = result.fetchall()
    print(tabulate(x, headers=['id', 'user_name', 'password', 'type', 'phone', 'address'], tablefmt='psql'))


def deleteAccount():
    usr = input("Enter user name to delete: ")
    cursor3 = mydb.cursor()
    cursor3.callproc('deleteAccount', (usr, ))
    for result in cursor3.stored_results():
        x = result.fetchall()
    mydb.commit()


def bookSearch():
    print("### BOOK SEARCH ###")
    options = input("How many parameters do you want to include in your search? ")
    cursor3 = mydb.cursor()
    if options == '4':
        param1 = input("Enter param 1: ")
        param2 = input("Enter param 2: ")
        param3 = input("Enter param 3: ")
        param4 = input("Enter param 4: ")
        cursor3.callproc('bookSearch4', (param1, param2, param3, param4))
        for result in cursor3.stored_results():
            x = result.fetchall()
        print(tabulate(x, headers=['book_id', 'title', 'category', 'author', 'edition', 'price'], tablefmt='psql'))
    elif options == '3':
        param1 = input("Enter param 1: ")
        param2 = input("Enter param 2: ")
        param3 = input("Enter param 3: ")
        cursor3.callproc('bookSearch3', (param1, param2, param3))
        for result in cursor3.stored_results():
            x = result.fetchall()
        print(tabulate(x, headers=['book_id', 'title', 'category', 'author', 'edition', 'price'], tablefmt='psql'))
    elif options == '2':
        param1 = input("Enter param 1: ")
        param2 = input("Enter param 2: ")
        cursor3.callproc('bookSearch2', (param1, param2))
        for result in cursor3.stored_results():
            x = result.fetchall()
        print(tabulate(x, headers=['book_id', 'title', 'category', 'author', 'edition', 'price'], tablefmt='psql'))
    elif options == '1':
        param1 = input("Enter param 1: ")
        cursor3.callproc('bookSearch1', (param1, ))
        for result in cursor3.stored_results():
            x = result.fetchall()
        print(tabulate(x, headers=['book_id', 'title', 'category', 'author', 'edition', 'price'], tablefmt='psql'))
    else:
        print("you can only use up to 4 parameters! ")


if __name__ == "__main__":
    connected = True
    while connected:
        a = input("Press 1 for login and 2 for signUp: ")
        if a == "1":
            print("Please Enter your Login Info")
            user = input("Username: ")
            pswd = input("Password: ")
            cursor = mydb.cursor()
            check = cursor.callproc('CheckUserExists', (user, pswd))
            for result in cursor.stored_results():
                x = result.fetchall()
            if x[0][0] == 1:
                # user exists
                field = checkField(user)
                if field == 'student' or field == 'prof' or field == 'normal':
                    choice = True
                    while choice:
                        printChoicesForUsers()
                        user_input = input("Enter your choice or 'q' to quit: ")
                        print(" ")
                        if user_input == '1':
                            inside = True
                            while inside:
                                printInfo(user)
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '2':
                            inside = True
                            while inside:
                                bookSearch()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '3':
                            inside = True
                            while inside:
                                borrow(user)
                                print(" ")
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '4':
                            inside = True
                            while inside:
                                returnBook(user)
                                print(" ")
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '5':
                            inside = True
                            while inside:
                                cash = input("Enter amount: ")
                                updateCash(user)
                                print(" ")
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == 'q':
                            choice = False
                if field == 'boss':
                    choice = True
                    while choice:
                        printChoicesForBOSS()
                        user_input = input("Enter your choice or 'q' to quit: ")
                        if user_input == '1':
                            inside = True
                            while inside:
                                bookInsertion()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '2':
                            inside = True
                            while inside:
                                inventoryInsertion()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '3':
                            inside = True
                            while inside:
                                updateInventory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '4':
                            inside = True
                            while inside:
                                userSearch()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '5':
                            inside = True
                            while inside:
                                successResults()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '6':
                            inside = True
                            while inside:
                                bookHistory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '7':
                            inside = True
                            while inside:
                                seeUsers()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '8':
                            inside = True
                            while inside:
                                seeHistory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '9':
                            inside = True
                            while inside:
                                printInbox()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '10':
                            inside = True
                            while inside:
                                deleteAccount()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == 'q':
                            choice = False
                if field == 'reception':
                    choice = True
                    while choice:
                        printChoicesForSTAFF()
                        user_input = input("Enter your choice or 'q' to quit: ")
                        if user_input == '1':
                            inside = True
                            while inside:
                                bookInsertion()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '2':
                            inside = True
                            while inside:
                                inventoryInsertion()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '3':
                            inside = True
                            while inside:
                                updateInventory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '4':
                            inside = True
                            while inside:
                                userSearch()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '5':
                            inside = True
                            while inside:
                                successResults()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '6':
                            inside = True
                            while inside:
                                bookHistory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '7':
                            inside = True
                            while inside:
                                seeUsers()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '8':
                            inside = True
                            while inside:
                                seeHistory()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == '9':
                            inside = True
                            while inside:
                                printInbox()
                                quit1 = input("press 'q' to quit ")
                                if quit1 == 'q':
                                    print(" ")
                                    inside = False
                        if user_input == 'q':
                            choice = False

            else:
                print("Wrong username of password")
        if a == "2":
            mycursor = mydb.cursor()
            checkUser = False
            checkPass = False
            id = input("Enter your id: ")
            name = input("Enter your name: ")
            family_name = input("Enter your family name: ")
            type = input("Enter your type: ")
            while checkUser is not True:
                user_name = input("Enter your userName: ")
                checkUser = checkUserName(user_name)
                if checkUser is False:
                    print("Username should be minimum 6 characters")
            while checkPass is not True:
                password = input("Enter your password: ")
                checkPass = checkPassword(password)
                if checkPass is False:
                    print("Password is weak!")
            balance = input("Enter your balance: ")
            address = input("Enter your address: ")
            phone = input("Enter your phone: ")
            argsPersonal = (id, name, family_name, type)
            argsSystematic = (id, user_name, password, int(balance))
            argsPhone = (id, phone)
            argsAddress = (id, address)
            personal = mycursor.callproc('insertIntoPersonal', argsPersonal)
            systematic = mycursor.callproc('insertIntoSystematic', argsSystematic)
            phone = mycursor.callproc('insertIntoPhone', argsPhone)
            address = mycursor.callproc('insertIntoAddress', argsAddress)
            mydb.commit()
            print("Congrats! You just SignedUp ")

