"""Flask App Project."""

from flask import Flask, jsonify, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twilSend import sendMess
import time

cred = credentials.Certificate('path/to/serviceAccnt.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://DATABASE.firebaseio.com'
})
#Authenticate firebase

numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#Create numList
def onlyNumbs(inString):
    returnStr = ""
    #function to extract only numerical characters from input string
    for x in inString:
        #Loop through input string
        if x in numList:
            #If it's in the number list
            returnStr += x
            #Add to main string
    return returnStr
# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/objRef')
ref2 = db.reference('/numberRef')
ref3 = db.reference('/sentRef')
#Define firebase refs we'll be using
app = Flask(__name__)
#initialize app

class storeClass:
    def __init__(self):
        self.x = ""

globs = storeClass()

chList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
#Define character list
@app.route('/')
def index():
    mnsr = ref.get()
    #Get brain data from objRef
    print(mnsr)
    #Redirect to login page
    return redirect(url_for('logs'))

@app.route('/<numbString>/brain')
def brain(numbString):
    #Get number string from http request
    print(numbString)
    strNum = ""
    #Create empty string for characters
    h = 0
    while h < len(numbString):
        #Loop through input string
        if numbString[h] in chList:
            #If current index is alphabetical character between a and j
            bv = 0
            while bv < len(chList):
                #Loop through chList
                if numbString[h].lower() == chList[bv]:
                    #Find exact index at which current character can be found(number represented by character)
                    strNum += str(bv)
                    #Add number to main string
                bv += 1
        else:
            if numbString[h] == "x":
                #If current character is x(represents decimal)
                strNum += "."
                #Add decimal to main string
            elif numbString[h] == "-":
                #If current character is negative sign(represents itself)
                strNum += "-"
                #Add negative to main string
        h += 1
    mainVar = float(strNum)
    #Convert main string to float
    ref.set(mainVar)
    #Push brain data to objRef
    revs = ref.get()
    #Pull from objRef
    return str(revs)


@app.route('/graphTest')
def graphTest():
    #Route for graph page
    return render_template("graphTest.html", vari=globs.x)

@app.route('/gets')
def gets():
    #URL to fetch brain data(didn't work through firebase web)
    floats = float(ref.get())
    #Pull from objRef
    print(floats)
    if floats > 1.2:
        #If amplitude is greater than 1.2
        numba = ref2.get()
        #Pull from teacher number ref
        msg = "Your students are getting unengaged, your lecture is boring and forgettable"
        #Create message
        sendMess(msg, numba)
        #Call to sendMess function to send SMS notification to teacher
    return str(ref.get())
    #Return alpha wave amplitude as string

@app.route('/logs', methods=['GET', 'POST'])
def logs():
    #Login page
    if request.method == 'POST':
        #If login form is submitted
        print(request.form['fn'])
        print(request.form['ln'])
        numVar = str(request.form['numb'])
        #Get phone number from form
        oneStr = "+1"
        oneStr += onlyNumbs(numVar)
        #Create string and filter out non-numerical characters the user may have accidentally inputted
        ref2.set(oneStr)
        #Push phone number string to numberRef
        print(ref2.get())
        #Print phone number
        return redirect(url_for('graphTest'))
        #Redirect to graph page
    return render_template("logs.html")

if __name__ == '__main__':
    app.run()
