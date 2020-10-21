from configparser import ConfigParser
import mysql.connector




header = 40

def createMenu(title,*args):
    print("#"*40)
    centerText(title)
    print("#"*40)
    print()
    if len(args) >1:
        for option in args:
            centerText(f"-{option}-")
    print()
    print("#"*40)
def displayRecord(*args):
    global header
    print("#"*header)
    print("\n")
    for text in args:
        print(text)
    print("\n")
    print("#"*header)
def centerText(text):
    global header
    value = int((header - len(text))/2)
    print(" "*value,text," "*value)  
class sql:
    def checkForMySQLConnection():
        config = ConfigParser()
        config.read("config.ini")
        config_variables = config["MySQL"]
        print("|CHECKING CONNECTION WITH MySQL DATABASE|")
        try:
            mydb = mysql.connector.connect(
                host=config_variables['host'],
                user=config_variables['user'],
                password=config_variables['password'],
                port=config_variables['port'],
                database=config_variables['database']
                    
            )
            cursor = mydb.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS  `itemstable` (`partnumber` VARCHAR(255),`name` VARCHAR(255),`description` VARCHAR(255),`location` VARCHAR(255),`quantity` INT(255),PRIMARY KEY (`partnumber`));')  
            main.menu()
        except mysql.connector.Error:
            print("Could'nt connect to database, your details could be wrong.")
            sql.changeConfigValues()
          
    def changeConfigValues():
        createMenu("Enter MySQL detials")
        while True:
            host = input("Host: ")
            user = input("User: ")
            password = input("Password: ")
            port = input("Port: ")
            database = input("Database: ")

            if host == None or user == None or password == None or port == None or database == None:
                print("You have to enter EVERY detail to connect to your database.")
                option = input("Press enter, or enter 'close' to close this program").lower()
                if option == "close":
                    exit()
            else:
                
                break

        print("Details has been changed, Thank you.")
        config = ConfigParser()
        config.read("config.ini")
        config["MySQL"] = {'host': host,'user': user,'password': password,"port": port,'database': database}
        with open('config.ini','a+') as conf:
            config.write(conf)
    
    def searchForRecord(value,searchtype):
        global header
        config = ConfigParser()
        config.read("config.ini")
        config_variables = config["MySQL"]
        mydb = mysql.connector.connect(
            host=config_variables['host'],
            user=config_variables['user'],
            password=config_variables['password'],
            port=config_variables['port'],
            database=config_variables['database']
                        
        )
        try:
            cursor = mydb.cursor()
            sql = f"SELECT * FROM itemstable WHERE {searchtype}='{value}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            displayRecord(f"Part number: {result[0]}",f"Name: {result[1]}",f"Description: {result[2]}",f"Quantity: {result[3]}",f"Location: {result[4]}")
        except:
            print("Can't find matching item.")
    def changeItem():
        global header

        
        partnumber = input("Enter part number: ")
        config = ConfigParser()
        config.read("config.ini")
        config_variables = config["MySQL"]
        mydb = mysql.connector.connect(
            host=config_variables['host'],
            user=config_variables['user'],
            password=config_variables['password'],
            port=config_variables['port'],
            database=config_variables['database']
                        
        )
        try:
            cursor = mydb.cursor()
            sql = f"SELECT * FROM itemstable WHERE partnumber='{partnumber}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            partnumber = result[0]
        except:
            print("Can't find matching item.")
            main.menu()
        
        print("#"*header,"\n")
        createMenu(f"Change item - {partnumber}","Change name","Change description","Change location","Change quantity")
        option = input("--> ").lower()

        if "change name" in option:
            while True:
                new_name = input("Enter new name: ")

                if new_name == None:
                    print("You have to enter the name.")
                else:
                    break
            sql = f"UPDATE itemstable SET name=%s WHERE partnumber=%s"
            values = (new_name,partnumber)
            cursor.execute(sql,values)
            mydb.commit()
            print("Name has been updated.")

        elif "change description" in option:
            while True:
                new_desc = input("Enter new descripton: ")
                if new_desc == None:
                    print("You have to enter the description.")
                else:
                    break
            sql = f"UPDATE itemstable SET description=%s WHERE partnumber=%s"
            values = (new_desc,partnumber)
            cursor.execute(sql,values)
            mydb.commit()
            print("Description has been updated.")

        elif "change location" in option:
            while True:
                new_location = input("Enter new location: ")

                if new_location == None:
                    print("You have to enter the location.")
                else:
                    break
            sql = f"UPDATE itemstable SET location=%s WHERE partnumber=%s"
            values = (new_location,partnumber)
            cursor.execute(sql,values)
            mydb.commit()
            print("Location has been updated.")
        elif "change quantity" in option:
            while True:
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    

                    if new_quantity == None:
                        print("You have to enter the quantity.")
                    else:
                        break
                except:
                    print("Value has to be a integer")
            sql = f"UPDATE itemstable SET quantity=%s WHERE partnumber=%s"
            values = (new_quantity,partnumber)
            cursor.execute(sql,values)
            mydb.commit()
            print("Quantity has been updated.")

        main.menu()

        
            
    def createItem():
        global header
        print("#"*header,"\n")
        n_partnumber = input("Enter partnumber: ")
        n_name = input("Enter name of item: ")
        n_desc = input("Enter description: ")
        n_location = input("Enter location: ")
        while True:
            try:
                n_quantity = int(input("Quantity: "))
                break
            except:
                print("You need to enter valid quantity.")


        if n_partnumber == None or n_name == None or n_desc == None or n_quantity == None:
            print("You can't leave any blanks")
            createItem()

        print("\nItem created.\nPart number: ",n_partnumber,"\nName: ",n_name,"\nDescription: ",n_desc,"\nQuantity: ",n_quantity)

        config = ConfigParser()
        config.read("config.ini")
        config_variables = config["MySQL"]
        mydb = mysql.connector.connect(
            host=config_variables['host'],
            user=config_variables['user'],
            password=config_variables['password'],
            port=config_variables['port'],
            database=config_variables['database']
                        
        )

        cursor = mydb.cursor()
        sql = f"INSERT INTO itemstable(partnumber,name,description,quantity,location) VALUES(%s,%s,%s,%s,%s)"
        values = (n_partnumber,n_name,n_desc,n_quantity,n_location)
        cursor.execute(sql,values)
        mydb.commit()

        main.menu()
        
                    
        
        



class main:
    def menu():
        createMenu("WMS","Find item","Create item","Change item","quit")
        option = input("--> ").lower()
        if "find item" in option:
            print("\nYou want to find item by name or part number?")
            action = input("-->")
            if "part number" in action:
                partnumber = input("Enter part number: ")
                sql.searchForRecord(partnumber,"partnumber")
                enter = input("Press enter to continue")
                main.menu()
            elif "name" in action:
                name = input("Enter name of item: ")
                sql.searchForRecord(name,"name")
                enter = input("Press enter to continue")
                main.menu()
            else:
                print("Invalid option...")
                main.menu()
        if "create item" in option:
            sql.createItem()
        if "change item" in option:
            sql.changeItem()
            
    def checkForConfig():
        config = ConfigParser()
        config.read("config.ini")
        if config.has_section("MySQL") == False:
            config["MySQL"] = {'host': "",'user': "",'password': "","port": 3306,'database': ""}
            with open('config.ini','a+') as conf:
                config.write(conf)
        




if __name__ == "__main__":
    main.menu()
