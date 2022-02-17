
from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

class price():
    def __init__(self,htmllink:str,availableTag:str,availableClass:str,priceTag:str ,priceClassName:str,isChild = False,childTag="",childClass="",oneChildTag="",oneChildClass=""):
        self.htmllink = htmllink
        self.availableTag = availableTag
        self.availableClass = availableClass
        self.priceTag = priceTag
        self.priceClassName = priceClassName
        self.isChild = isChild
        self.childTag = childTag
        self.childClass = childClass
        self.oneChildTag = oneChildTag
        self.oneChildClass = oneChildClass

    def getPrice(self):
        html_text = requests.get(self.htmllink).text
        soup = BeautifulSoup(html_text, 'lxml')
        if not self.isChild:
            isAvailable = soup.find(self.availableTag, class_=self.availableClass).text
        else:
            parentClass = soup.find(self.availableTag,self.availableClass)
            
            children = parentClass.findChildren(self.childTag,class_=self.childClass, recursive=False)
            for child in children:
                if self.oneChildTag != "" and self.oneChildClass =="":
                    isAvailable = child.find(self.oneChildTag).text
                else:
                    isAvailable = child.text
        shopName = self.htmllink
        price = soup.find(self.priceTag,class_=self.priceClassName).text

        return {"availability" :isAvailable,"name" :shopName,"price":price}

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/price")

def getInfo():
    myList = []
    page1 = price("https://grybezpradu.eu/Bor-gra-planszowa-sklep",'span','second','em','main-price')
    myList.append(page1.getPrice())
    page2 = price("https://dragoneye.pl/bor-p-4143.html",'a','noWrap','span','cenaBrutto wartoscBrutto')
    myList.append(page2.getPrice())
    page3 = price("https://www.rebel.pl/gry-planszowe/bor-2007946.html",'span','u--text-900 collapsible-with-caret collapsed','span','price')
    myList.append(page3.getPrice())
    page4 = price("https://mepel.pl/bor",'div','availability','em','main-price',True,'span','label-icon gray','em')
    myList.append(page4.getPrice())
    page5 = price("https://sklep.portalgames.pl/bor",'div','row availability','em','main-price color',True,'span','second','span','second')
    myList.append(page5.getPrice())
    return render_template("home.html",isAvailable=myList)
