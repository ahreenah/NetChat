import pickle
import SQLAlchemy

class Message:
    id=0
    text=""
    fromwho=""
    def __init__(self,idd,textt,fromwhoo):
        self.id=idd
        self.text=textt
        self.fromwho=fromwhoo
        #print(text)
    def get(self):
        return self.text

class Chat:
    idneed=0
    users=[]
    messages=[]
    def __init__(self):
        self.users=[]
    def addUser (self, uname):
        if( not uname in self.users ):
            self.users.append(uname)
    def save(self):
        f=open("test.pickle","wb")
        pickle.dump([self.idneed,self.users,self.messages],f)
        f.close()
    def post(self,fromwho,what):
        if(fromwho in self.users):
            global idneed
            #print(self.idneed)
            self.messages.append(Message(self.idneed,what,fromwho))
            self.idneed=self.idneed+1
        else:
            raise Exception("No such user")
    def load(self):
        tmp=pickle.load(open("test.pickle","rb"))

        #print(tmp[0])
        self.idneed=tmp[0]
        self.users=tmp[1]
        self.messages=tmp[2]
    def get(self,num):
        return(self.messages[-num:])
    

ch = Chat()

ch.load()
a=[1,2,3]
#pickle.dump(a,open("test2.pickle","wb"))
#b=pickle.load(open("test2.pickle","rb"))
#print(b)
print(ch.get(3))
ch.save()
