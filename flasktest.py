import testalchemy as api
from flask_socketio import SocketIO, send
################################################################

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio=SocketIO(app)
#print(api.getChat(3))
@app.route('/')
def main_page():
   if "login" in session:
      linf=session["login"]
   else:
      linf=None
   return render_template("index.html", title="Welcome to NetChat", logininfo=linf)

@app.route('/user/<iduser>')
def viewuser(iduser):
   return render_template("viewuser.html", userid=iduser, exists=users.userExists(iduser), title=iduser, logininfo=session["login"])

@app.route('/about')
def about():
   return render_template("about.html", title="About NetChat")

@app.route('/login')
def loginform():
   return render_template("login.html")
   return ('''<form action="log_in" method="POST">
           login:<input type="text" name="login"><br>
           password:<input type="password" name="password">
           <input type="submit" title="login">
           </form>''')

@app.route('/log_in', methods=['POST'])
def formtest():
   if "login" in session:
      linf=session["login"]
   else:
      linf=None
   if(api.checkOnLogin(request.form["login"],request.form["password"])):
      session["login"]=request.form["login"]
      return render_template("log_in.html",out="Welcome " + request.form["login"])

   else:
      return render_template("log_in.html",out="Wrong login or password",logininfo=linf)

@app.route('/logout')
def logout():
   session.pop("login",None)
   return "You successfully logged out"

@app.route('/chat/<idchat>', methods=['GET','POST'])
def showchat(idchat):
   if "login" in session:
      linf=session["login"]
   else:
      linf=None
   leng=(len(api.getChat(int(idchat))))
   out=[]
   try:
      if(request.form.get("message","")==""):
         out.append([["not"],[" inputted "]])
      else:
         api.writeMessageToChat(session['login'],idchat,request.form.get("message"))
         #out.append([["you printed "],[request.form.get("message","")+"<br>"]])
         #request.form["message"]=None
         
   except:
      out.append([["not"],[" inputted "]])
   for i in range(leng):
      out.append([api.getChat(int(idchat))[i].author,api.getChat(int(idchat))[i].text])
   return render_template("chat.html",chatbody=out,logininfo=linf)

@app.route('/messages')
def rett():
   if "login" in session:
      return render_template("chatWithSockets.html",CurrentUser=session["login"], chatid=False)
   return "You should login to use chats"

@app.route('/messages/<chid>')
def rett2(chid):
   if "login" in session:
      return render_template("chatWithSockets.html",CurrentUser=session["login"], chatid=chid)
   return "You should login to use chats"

@app.route('/registration')
def reg():
   return render_template("registration.html")
@app.route('/registr_ation', methods=['POST'])
def formtest1():
   if "login" in session:
      linf=session["login"]
   else:
      linf=None
   print(request.form["password"])
   if (request.form["password"] == request.form["password_repeat"]):
      api.registerNewUser(request.form["login"], request.form["password"])
      session["login"]=request.form["login"]
      return render_template("registr_ation.html", out="Welcome " + request.form["login"])
   else:
      return render_template("registr_ation.html", out="Oh, your password and your repeat of password aren't equals. Try again.")

@socketio.on('message')
def handleMessage(message):
    if message[0]==1:
       print("connected")
    if message[0]==2:  
       print(message)
    send(message, broadcast=True)
@socketio.on('message')
def handleMessage(message):
    if message[0]==1:
       print("connected")
    if message[0]==2:  
       print(message)
    send(message, broadcast=True)
@app.route("/stylesheet.css")
def style():
   return render_template("stylesheet.css")

if __name__ == '__main__':
   socketio.run(app)
