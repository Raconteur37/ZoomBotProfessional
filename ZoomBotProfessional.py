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

def sortClasses(a:list):
    del a[0]
    for x in range(len(a)):
        for z in range(len(a) - 1):
            temp = a[z]
            #tempClass = getInstanceFromDb(temp, 1) #Class name
            tempTime = getInstanceFromDb(temp,2) # Class time
            tempTime = tempTime.split(":")
            tempTimeHour = tempTime[0]
            tempTimeMinute = tempTime[1]
            finalTime = float(tempTimeMinute) * .01
            finalTime = finalTime + float(tempTimeHour)
            tempTimeofDay = getInstanceFromDb(temp,3) # Class time of day
            if str.lower(tempTimeofDay) == "pm":
                if (int(tempTimeHour) != 12):
                    finalTime = float(finalTime) + 12.0
            temp2 = a[z + 1]
            #tempClass2 = getInstanceFromDb(temp2, 1) #Class name
            tempTime2 = getInstanceFromDb(temp2,2) # Class time
            tempTime2 = tempTime2.split(":")
            tempTimeHour2 = tempTime2[0]
            tempTimeMinute2 = tempTime2[1]
            finalTime2 = float(tempTimeMinute2) * .01
            finalTime2 = finalTime2 + float(tempTimeHour2)
            tempTimeofDay2 = getInstanceFromDb(temp2,3) # Class time of day
            if str.lower(tempTimeofDay2) == "pm":
                if(int(tempTimeHour2) != 12):
                    finalTime2 = float(finalTime2) + 12.0        
            if (float(finalTime) > float(finalTime2)):
                a[z], a[z+1] = a[z+1], a[z]
    return a


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

def cleanDbTable(a:str):
    a = str(a)
    a = a.replace("[","")
    a = a.replace("]","")
    a = a.replace("(","")
    a = a.replace(")","")
    a = a.replace(",","")
    a = a.replace("'","")
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
    print(f"{colors.CYAN}{colors.BOLD}Choose some options: {colors.END}{colors.BOLD}\n 1. List all classes to access \n 2. Add a class \n 3. Edit a class \n 4. Remove a class \n 5. Remove a user \n 6. {colors.WARNING}{colors.BOLD}Exit{colors.END}")
    option = int(input("Choose an option: "))

    if (option == 1):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        check = sortClasses(check)
        if len(check) > 1:
            print(f"Here is a list of your classes: ")
            print(f"")
            disNum = 1
            z = 0
            while (z < len(check)):
                print(f"-={colors.BOLD}{colors.UNDERLINE} {disNum}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} {colors.END}=-")
                z = z + 1
                disNum = disNum + 1
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
            check = sortClasses(check)
            if len(check) > 1:
                go = True
                print(f"Here is a list of your classes: ")
                print(f"")
                disNum = 1
                z = 0
                while (z < len(check)):
                    print(f"-={colors.BOLD}{colors.UNDERLINE} {disNum}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} with a link of {getInstanceFromDb(check[z],4)}{colors.END}=-")
                    z = z + 1
                    disNum = disNum + 1
                print(f"")
            else:
                print(f"{colors.WARNING}You have no classes!{colors.END}")
                go = False
            if(go):
                edit = input("What class would you like to edit? EX (1 or 3): ")
                edit = int(edit) - 1
                theClass = check[edit]
                className = getInstanceFromDb(theClass,1)
                classTime = getInstanceFromDb(theClass,2)
                classTimeOfDay = getInstanceFromDb(theClass,3)
                classLink = getInstanceFromDb(theClass,4)
                editType = input(f"What do you want to edit about {className}? EX (name, time, time of day, or link): ")
                if (str.lower(editType) == "name"):
                    editName = input(f"What do you want the new name for {className} to be? ")
                    with conn:
                        c.execute(
                        'UPDATE classes SET class = ? WHERE class= ?', 
                        (editName, className,))
                    print(f"Updated {className} to now be called {editName}")
                if (str.lower(editType) == "time"):
                    editTime = input(f"What do you want the new time for {className} to be? Current({classTime}): ")
                    with conn:
                        c.execute(
                        'UPDATE classes SET time = ? WHERE class= ?', 
                        (editTime, className,))
                    print(f"Updated {className}'s time to {editTime}")
                if (str.lower(editType) == "time of day"):
                    editTimeOfDay = input(f"What do you want the new time of day for {className} to be? Current({classTimeOfDay}): ")
                    with conn:
                        c.execute(
                        'UPDATE classes SET timeofday = ? WHERE class= ?', 
                        (editTimeOfDay, className,))
                    print(f"Updated {className}'s time of day to {editTimeOfDay}")
                if (str.lower(editType) == "link"):
                    editLink = input(f"What do you want the new link for {className} to be? EX (zoom.com): ")
                    with conn:
                        c.execute(
                        'UPDATE classes SET link = ? WHERE class= ?', 
                        (editLink, className,))
                    print(f"{colors.BOLD}{colors.SUCCESS}Updated {className}'s link to {editLink}{colors.END}")
            else:
                print(f"{colors.WARNING}{colors.BOLD}There was an error!{colors.END}")        

    if (option == 4):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        check = sortClasses(check)
        if len(check) > 1:
            print(f"Here is a list of your classes: ")
            print(f"")
            disNum = 1
            z = 0
            while (z < len(check)):
                print(f"-={colors.BOLD}{colors.UNDERLINE} {disNum}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} {colors.END}=-")
                z = z + 1
                disNum = disNum + 1
            print(f"")
            option = input(f"What class do you want to remove? EX (1 or 3): ")
            option = int(option) - 1
            theClass = check[option]
            className = getInstanceFromDb(theClass,1)
            with conn:
                c.execute('DELETE FROM classes WHERE class = ?',(className,))
            print(f"{colors.BOLD}{colors.SUCCESS}Removed {className}{colors.END}")
        else:
            print(f"{colors.WARNING}You have no classes!{colors.END}")

    if(option == 5):
        c.execute('SELECT name FROM classes') 
        check = c.fetchall()
        check = list(dict.fromkeys(check))
        print(f"Here is a list of your classes: ")
        print(f"")
        disNum = 1
        for x in check:
            print(f"-={colors.BOLD}{colors.UNDERLINE} {disNum}. {cleanDbTable(x)} {colors.END}=-")
            disNum = disNum + 1
        print(f"")
        option = input(f"What user do you want to remove? EX (1 or 3): ")
        option = int(option) - 1
        remove = check[option]
        remove = cleanDbTable(remove)
        with conn:
            c.execute('DELETE FROM classes WHERE name = ?',(remove,))
        print(f"{colors.BOLD}{colors.SUCCESS}Removed {remove}{colors.END}")
            


    if (option == 6):
        run = False
        print("You have exited")

