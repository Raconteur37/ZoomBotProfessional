import sqlite3
conn = sqlite3.connect('ZoomBotProfessionalDB.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS classes (
        name text,
        class text,
        time text,
        timeofday text,
        link text)""")

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

personName = str.lower((input("What is your name? EX (John M): ")))
c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
check = c.fetchone()
if check is None:
    c.execute("INSERT INTO classes VALUES (:name, :class, :time, :timeofday, :link)", {'name': personName, 'class': "", 'time': "", 'timeofday': "", 'link': ""})
    print("Welcome new person!")
    conn.commit()
print(f"Welcome {personName}!")
run = True
while (run):
    print("Choose some options: \n 1. List all classes to access \n 2. Add a class to access \n 3. Edit a class \n 4. Exit")
    option = int(input("Choose an option: "))

    if (option == 1):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if len(check) > 1:
            print("Here is a list of your classes: ")
            z = 1
            while (z < len(check)):
                print(f"-= {z}. {getInstanceFromDb(check[z],1)} at {getInstanceFromDb(check[z],2)} {getInstanceFromDb(check[z],3)} =-")
                z = z + 1
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

    if(option == 5):
        c.execute('SELECT * FROM classes WHERE name IN (SELECT name FROM classes WHERE name = ?)', (personName,))
        check = c.fetchall()
        if check is not None:
            for x in check:
                print(x)
                print(getInstanceFromDb(x,1))

    if (option == 4):
        run = False
        print("You have exited")

