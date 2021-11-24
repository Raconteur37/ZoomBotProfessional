import sqlite3
conn = sqlite3.connect('ZoomBotProfessionalDB.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS classes (
        name text,
        class text,
        time text,
        timeofday text,
        link text)""")

class colors:
    SUCCESS = '\033[92m'
    WARNING = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Class:

    def __init__(self,name,time,timeofday,link):
        self.name = name
        self.time = time
        self.timeofday = timeofday
        self.link = link

    def getName(self):
        return self.name
    
    def getTime(self):
        return self.time

    def getTimeOfDay(self):
        return self.timeofday

    def getLink(self):
        return self.link

def getInstanceFromDb(a:str,index):
    a = str(a)
    a = a.replace("[","")
    a = a.replace("]","")
    a = a.replace("(","")
    a = a.replace(")","")
    a = a.replace("'","")
    temp = a.split(",")
    a = temp[index]
    a = a.replace(" ","")
    return(a)

personName = str.lower((input(f"{colors.BOLD}What is your name?{colors.END} EX (John M): ")))
c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
check = c.fetchone()
if check is None:
    c.execute("INSERT INTO classes VALUES (:name, :class, :time, :timeofday, :link)", {'name': personName, 'class': "", 'time': "", 'timeofday': "", 'link': ""})
    print(f"{colors.BOLD}{colors.YELLOW}Welcome new person!{colors.END}")
    conn.commit()
temp = personName.split(" ")
print(f"{colors.BOLD}Welcome {colors.YELLOW}{temp[0]}.{colors.END}")
run = True
while (run):
    print(f"{colors.CYAN}Choose some options: {colors.END}\n 1. List all classes to access \n 2. Add a class \n 3. Edit a class \n 4. Remove a class \n 5. {colors.WARNING}{colors.BOLD}Exit{colors.END}")
    option = int(input("Choose an option: "))

    if (option == 1):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if len(check) > 1:
            print(f"Here is a list of your classes: ")
            print(f"")
            z = 1
            while (z < len(check)):
                print(f"-={colors.BOLD}{colors.UNDERLINE} {z}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} {colors.END}=-")
                z = z + 1
            print(f"")
        else:
            print("You have no classes!")

    if(option == 2):
        adding = True
        className = input("Input class name: EX (Pre cal): ")
        classTime = input("Input class time: EX (10:30): ")
        classTimeOfDay = input("Input class time of day: EX (AM or PM): ")
        classLink = input("Input class link: EX (blahblah.com): ")
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if check is not None:
            for x in check:
                if (getInstanceFromDb(x,1).lower() == className.lower()):
                    adding = False
        if (adding):
            c.execute("INSERT INTO classes VALUES (:name, :class, :time, :timeofday, :link)", {'name': personName, 'class': className, 'time': classTime, 'timeofday': classTimeOfDay, 'link': classLink})   
            conn.commit()
            print(f"Added {className} class")
        else:
            print("Cannot add duplicate classes!")

    if (option == 3):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if len(check) > 1:
            print("Here are your classes: ")
            z = 1
            while (z < len(check)):
                print(f"{colors.UNDERLINE}{z}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} with a link of {getInstanceFromDb(check[z],4)}{colors.END}")
                z = z + 1
            edit = input("What class would you like to edit? (The exact name that's displayed): ")
            edit = edit.replace(" ","")
            editType = input("What do you want to edit? EX (name, time, time of day, or link): ")
            if (str.lower(editType) == "name"):
                editName = input(f"What do you want the new name for {edit} to be? ")
                with conn:
                    c.execute(
                    'UPDATE classes SET class = ? WHERE class= ?', 
                    (editName, edit,))
                print(f"Updated {edit} to now be called {editName}")
            if (str.lower(editType) == "time"):
                editTime = input(f"What do you want the new time for {edit} to be? EX (10:30): ")
                with conn:
                    c.execute(
                    'UPDATE classes SET time = ? WHERE class= ?', 
                    (editTime, edit,))
                print(f"Updated {edit}'s time to {editTime}")
            if (str.lower(editType) == "time of day"):
                editTimeOfDay = input(f"What do you want the new time of day for {edit} to be? EX (AM or PM): ")
                with conn:
                    c.execute(
                    'UPDATE classes SET timeofday = ? WHERE class= ?', 
                    (editTimeOfDay, edit,))
                print(f"Updated {edit}'s time of day to {editTimeOfDay}")
            if (str.lower(editType) == "link"):
                editLink = input(f"What do you want the new link for {edit} to be? EX (zoom.com): ")
                with conn:
                    c.execute(
                    'UPDATE classes SET link = ? WHERE class= ?', 
                    (editLink, edit,))
                print(f"{colors.BOLD}{colors.SUCCESS}Updated {edit}'s link to {editLink}{colors.END}")
            else:
                print(f"{colors.WARNING}{colors.BOLD}That's not a valid argument!{colors.END}")
        else:
            
            print(f"{colors.WARNING}{colors.BOLD}You dont have any classes! {colors.END}")

    if (option == 5):
        print()
        

    if(option == 6):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if check is not None:
            for x in check:
                print(x)
                print(getInstanceFromDb(x,1))

    if (option == 5):
        run = False
        print("You have exited")

