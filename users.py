import sqlite3
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
#cursor.execute("CREATE TABLE users (username text, password text, age text, sex text, name text)")
def registerNewUser(username,password,age,sex,name):
    if(not (userExists(username))):
       cursor.execute("INSERT INTO users VALUES('"+username+"', '"+password+"', '"+age+"', '"+sex+"', '"+name+"')")
       conn.commit()
def getUser(username):
    cursor.execute("SELECT * FROM users WHERE username='"+username+"'")
    return cursor.fetchall()
def userExists(username):
    return(len(getUser(username))>0)
def getUserName(username):
    return (getUser(username)[0][4])
def getUserAge(username):
    return(getUser(username)[0][2])
def getUserGender(username):
    return(getUser(username)[0][3])
def getUserPassword(username):
    return(getUser(username)[0][1])
def checkOnLogin(username,password):
    if(not userExists(username)):
        return False
    if(getUserPassword(username)==password):
        return True
    return False
registerNewUser("medvedeicheg","secret","sada","N","sashok")
print(getUser("medvedeicheg"))
print(userExists("medvedeicheg"))
print(getUserPassword("medvedeicheg"))
print(checkOnLogin("medvedeicheg","secret"))
print(getUserAge("medvedeicheg"))
