from sqlalchemy import create_engine
engine=create_engine('sqlite:///app.db', echo=True)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata=MetaData()

users_table=Table('users',metadata,
                  Column('id',Integer,primary_key=True),
                  Column('name',String),
                  Column('login',String,unique=True),
                  Column('password',String))

messages_table=Table('messages',metadata,
                     Column('id',Integer,primary_key=True),
                     Column('text',String),
                     Column('previd',Integer),
                     Column('author',Integer,ForeignKey('users.id')))

chat_table=Table('chats',metadata,
                 Column('id',Integer,primary_key=True),
                 Column('last',Integer,ForeignKey('messages.id'),unique=True))

metadata.create_all(engine)

class Message(object):
    def __init__(self,author,text,previd):
        #self.id=Column(Integer, primary_key=True)
        self.author=author
        self.text=text#Column(String)
        self.previd=previd#Column(Integer,ForeignKey("messages.id"))
    def __repr__(self):
        return "<Message(%s, %s, %s)>" % (self.text, self.previd, self.author)

class User(object):
    def __init__(self,name,login,password):
        self.name=name
        self.login=login
        self.password=password
    def __repr__(self):
        return "<User(%s, %s, %s)>" % (self.name, self.login, self.password)

class Chat:
    def __init__(self):
        self.last=None
    def __repr__(self):
        return "<Chat(%s)>" % (self.last)
    def setlast(self, idlastneed):
        self.last=idlastneed
    def getlast(self):
        return self.last

from sqlalchemy.orm import mapper, sessionmaker
mapper(User,users_table)
mapper(Message,messages_table)
mapper(Chat,chat_table)

def registerNewUser(login,password):
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    med=User("",login,password)
    session.add(med)
    session.commit()
    session.close()

def userExists(loginn):
    return not getUser(loginn)==None
    
def getUser(loginn):
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    session.close()
    return session.query(User).filter_by(login=loginn).first()

def getUserPassword(loginn):
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    session.close()
    return session.query(User).filter_by(login=loginn).first().password

def getallUser():
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    session.close()
    return session.query(User).all()

def writeMessageToChat(username,previd,text):
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    mes=Message(username,text,previd)
    session.add(mes)
    session.commit()
    session.close()

def writeMessageToChatOld(username,chatid,text):
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    #session.close()
    #ch=session.query(Chat).filter_by(id=chatid)
    ch=session.query(Chat).all()[0]
    #print(ch)
    lastid=ch.getlast()
    """mes=Message(username,text,lastid)
    session.add(mes)
    session.commit()"""
    writeMessage(username,lastid,text)
    mes=session.query(Message).filter_by().first()
    ch.setlast(mes.id)
    
    #print(mes.id)
    #print(ch.last)
    session.add(ch)
    #session.query(Chat).filter_by(id=chatid).delete()
    session.commit()
    session.close()

def createChat():
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    ch=Chat();
    session.add(ch)
    session.commit()
    session.close()

def getChat(idchat):
    engine=create_engine('sqlite:///app.db', echo=True)
    metadata=MetaData()
    from sqlalchemy.orm import mapper, sessionmaker
    
    Session=sessionmaker()
    Session.configure(bind=engine)
    session=Session()
    #session.close()
    #ch=session.query(Chat).filter_by(id=chatid)
    ch=session.query(Message).filter_by(previd=idchat).all()
    #print(ch)
    ret=[]
    for cht in ch:
        #if(cht.previd==idchat):
            ret.append(cht)
    session.close()
    return ret
    

def checkOnLogin(username,password):
    if(not userExists(username)):
        return False
    if(getUserPassword(username)==password):
        return True
    return False

#createChat()
"""writeMessageToChat("medved","1","Hello  world!")
writeMessageToChat("medvedev","1","Hi!")
writeMessageToChat("Alex","1","How are you guys?")
writeMessageToChat("GoodMan","1","Hello!")
writeMessageToChat("Somebody","1","Fine!")
writeMessageToChat("medved","1","Great!")
writeMessageToChat("Somebody","1","Bye!")"""
#print(getChat(3))

############################################
#                                          #
#  writeMessageToChat(login,chat id, text) #
#  getChat(chat id)                        #
#  registerNewUser(login, password)        #
#  getUser                                 #
#  userExists                              #
#  getUserPassword                         #
#                                          #
############################################
