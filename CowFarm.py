from tkinter import ttk
from tkinter.font import Font
import tkinter as tk
from tkinter.messagebox import *
from random import randint,choice

window=tk.Tk()
# Introduction to the game.

showinfo(title="Introduction", message="Dairy Farm Game!\n\nYour goal is to earn money by selling milk\n\
    This paragraph will inform you about milk production in this game.\n\
    Milk production depends upon age of the cow, the young the cow the profitable it will be.\n\
    Milk of a cow will decrease over time, it will be increased if your cow gives birth to a calf.\n\
    You can mate a cow with a bull.\n\
    There are much chances that your cow will die after 8 years.")

# change these if you are unsatisfied with the economy.
money=1000000 # Starting money
milkPrice=50
grassPriceRainy=300
grassPriceSunny=400
rainyMonths=(4,5,6,7,8) # Months in which rains
rainProbability=1/3
cowsInMarket=6 # Amount of cows on sale in the market
# milk of a cow changes with age.
# key is age. value is milk
ageMilkRelation={1:10,2:11,3:randint(11,13) ,4:randint(12,15) ,5:12 ,6:randint(10,11), 7:randint(9,10)}
# change these if you don't follow English months.
monthNames=('January','February','March','April','May','June','July','August','September','October','November','December')
# change these if you don't follow the solar calendar.
monthDays=(31,28,31,30,31,30,31,31,30,31,30,31)
# Cow price calculation algorithm
def CalculatePrice(age,milk,meat,ispregnant=False,prgDate=(0,0)):
    agePriceRelation = {7:35000, 1:70000, 6:54000, 2:65000, 3:60000, 4:57000, 5:50000}
    #meatMilkRelation={10:15,9:14,8:13,7:12,6:11,5:10,4:9,3:8,2:7,1:6}
    price=agePriceRelation[age] + milk*1000 + meat*2000
    if ispregnant:
        price+=10000
    
    return price

month=0
year=0
profit=0
milk=0 
cowInfo=[] #Stores information of bought cows.
# List of dictionaries, each dictionary is one cow's info.
# Dictionary structure is described below
# cowLastCalf : Tuple showing the date of birth of cow's youngest calf.
# cowMilk : int
# cowAge : list [year, month]
# IsPregnant : boolean
# prgDate : Tuple (year, month)
bullsInfo=[] #Stores information of bought bulls.
calves=[] #Stores information of born calves.

window.title('Dairy Farm')
window.geometry('800x400')

def getGrassPrice(weather):
    return grassPriceSunny if weather == "sunny" else grassPriceRainy
    
def getSlaughterPrice(meat):
    return meat*9000

# Doesn't work
def getFoodRequirement(meat):
    meatFoodRelation={10:600,9:550,8:500,7:450,6:400,5:350,4:300,3:250,2:250,1:250}
####
s=ttk.Style()
s.configure('my.TButton', font=('Helvetica', 12)) #for buttons
sL=ttk.Style()
sL.configure('my.TLabel', font=('Helvetica', 12)) #for label
label=ttk.Label(window, style='my.TLabel')
label.pack(side='top', anchor = 'center')
buttonsFrame2=ttk.Frame(window)
buttonsFrame2.pack(side='top')

def MonthlyCycle(): #Main game window
    global month, year, money, calves, cowInfo, bullsInfo, profit, milk

    weather='sunny'
    if month in rainyMonths: #monsoon
        weather='rainy' if randint(1,3) == 2 else 'sunny'

    if month==12: #Year ends 'after' 12th month but counting starts from 0
        year+=1
        month=0
    label['text']=("Money : "+str(money)+
        "\nProfit : "+str(profit)+
        "\nCows : "+str(len(cowInfo))+
        "\nBulls : "+str(len(bullsInfo))+
        "\nCalves : "+str(len(calves))+
        "\nTotal Milk: "+str(milk)+
        "\n            Year: "+str(year)+" Month: "+monthNames[month]+
        "\nMonthly Weather Conditions: "+weather)

    for i in buttonsFrame2.pack_slaves(): #destroy buttons created from previous interactions
        i.destroy()
    
    milk=0
    grass=getGrassPrice(weather)*monthDays[month]*( len(cowInfo)+len(bullsInfo) )
    for calf in calves:
        # calf gets mature after 16 months
        if year*12+month > calf['Birthday'][0]*12+16:
            if calf['Gender']=='Male': 
                bullsInfo.append({'bullAge': [1,4],
                    'bullMeat':5})
                continue
                
            cowInfo.append({'cowLastCalf':(0,0),'cowMilk':0,'cowAge':[1,4],'cowMeat':5})
            cow=len(cowInfo)-1
            if bulls>0: #breed this immediately
                cowInfo[cow]['IsPregnant']=True
                cowInfo[cow]['prgDate']=(year,month)
            else:
                cowInfo[cow]['IsPregnant']=False
                cowInfo[cow]['prgDate']=(-1,-1)
            calves.remove(calf)
        # calf drinks milk until 3 months
        if year*12+month > calf['Birthday'][0]*12+3: milk-=1
        # else it eats grass
        else: grass+=100*monthDays[month]

    for cow in cowInfo:
        if cow == {}: continue
        
        cow['cowAge'][1]+=1
        if cow['cowAge'][1]==13:
            cow['cowAge'][0]+=1
            cow['cowAge'][1]=0

        if cow['cowAge'][0] >= 8 and randint(0,3)!=1:
            showinfo(message = 'Unfortunately, one of your cows has died')
            cowInfo.remove(cow)
            
        if cow['IsPregnant']:
            # Get no: of month in which the cow got pregnant by using `year*12+months`.
            # +9: after 9 months a calf will be born
            if cow['prgDate'][0]*12+cow['prgDate'][1]+9 <= year*12+month:
                cow['IsPregnant']=False
                cow['cowMilk']=ageMilkRelation[cow['cowAge'][0]]
                Gender=choice(['female','male'])
                calves.append({'Birthday':(year,month), 'Gender':Gender})
                showinfo(message=f'A {Gender} calf is born!')
        
        milk += cow['cowMilk']
        if month+(year*12)-(cow['cowLastCalf'][1]-cow['cowLastCalf'][0]*12) >= 7 or \
           ( month+(year*12)-(cow['cowLastCalf'][1]-cow['cowLastCalf'][0]*12) >= 5 and cow['IsPregnant']):
            if cow['cowMilk'] > 0:
                cow['cowMilk']-=2 if randint(1,3) == 3 else 1
                    
            if not cow['cowMilk']:
                if not len(bullsInfo):
                    showerror(message = "You don't have a bull, your cows can't get pregnant. One of your cow has lost milk")
                else:
                    cow['IsPregnant']=True
                    cow['prgDate']=(year,month)
    for bull in bullsInfo:
        if bull=={}:
            continue
            
        bull['bullAge'][1]+=1
        if bull['bullAge'][1]==13:
            bull['bullAge'][0]+=1
            bull['bullAge'][1]=0

        if bull['bullAge'][0] >= 8 and randint(0,3)!=1:
            showinfo(message = 'Unfortunately, one of your bulls has died')
            bullsInfo.remove(bull)
    profit=(milk*50*monthDays[month])-grass #Total profit = Income-Maintanence
    money+=profit 
    month+=1
MonthlyCycle()
def GoToMarket():
    marketInfo=[]
    num=0 #number of animal being viewed
    buttons = buttonsFrame2.pack_slaves()
    for i in buttons:
        i.destroy()
    global money
    for i in range(cowsInMarket):
        age=randint(1,7)
        meat=randint(1,10)
        gender=choice(['female','male'])
        if gender=='female':
            price=CalculatePrice(age,ageMilkRelation[age],meat)
            marketInfo.append({'Age':age , 'Milk':ageMilkRelation[age]+meat , 'Price':price, 'Pregnancy':False, 'Meat':meat, 'Gender':'female'})
        else:
            price=CalculatePrice(age,0,meat)
            marketInfo.append({'Age':age , 'Price':price, 'Meat':meat, 'Gender':'male'})
    
    spacing=30
    buttons=[]
    def BuyCow():
        global money
        nonlocal num
        if money >= marketInfo[num]['Price']:
            money-=marketInfo[num]['Price']
            if marketInfo[num]['Gender']=='female':
                cowInfo.append({'cowLastCalf':(0,0),
                        'cowMilk':marketInfo[num]['Milk'],
                        'cowAge':[marketInfo[num]['Age'],0],
                        'IsPregnant':marketInfo[num]['Pregnancy'],
                        'prgDate':(-1,-1),
                        'cowMeat':marketInfo[num]['Meat']})
            else:
                bullsInfo.append({'bullAge':[marketInfo[num]['Age'],0],
                        'bullMeat':marketInfo[num]['Meat']})
            marketInfo.remove(marketInfo[num])
            showinfo(message='You have successfully bought the animal')
            if not marketInfo:
                Exit()
                return
            num=num-1 if num else 0
            InsideMarket()
        #else:
            
    def InsideMarket():
        Text=''
        for keys,values in marketInfo[num].items():
            Text+=keys+str(values).rjust(spacing-len(str(keys)))+'\n'
        label.configure(text=Text)
    def Decreasenum():
        nonlocal num
        num=num-1 if num else len(marketInfo)-1
        InsideMarket()
    def Increasenum():
        nonlocal num
        num=num+1 if not num==len(marketInfo)-1 else 0
        InsideMarket()
    def Exit():
        for i in buttons: 
            i.destroy()
        label.destroy
        MonthlyCycle()
    if buttons==[]:
        buttons.append(ttk.Button(buttonsFrame2, text='Prev',
            command = Decreasenum))
        buttons.append(ttk.Button(buttonsFrame2, text='Next',
            command = Increasenum))
        buttons.append(ttk.Button(buttonsFrame2, text='Buy', command = BuyCow))
        buttons.append(ttk.Button(buttonsFrame2, text='Exit', command = Exit))
        for i in buttons:
            i.pack(side='right', anchor='center')
            i['style']='my.TButton'
    InsideMarket()

def ShowAnimals():
    i=0
    iterating_list=cowInfo+bullsInfo+calves
    if iterating_list==[]:
        showerror(message="You don't have a cow or bull. Buy one from market.")
        return
    for j in buttonsFrame2.pack_slaves():
        j.destroy()
    spacing=30
    buttons=[]
    change_strings={'cowLastCalf':'Last calf born on',
        'cowMilk':'Milk',
        'cowAge':'Age',
        'IsPregnant':'IsPregnant',
        'prgDate':'Pregnant Date',
        'cowMeat':'Meat',
        'bullAge':'Age',
        'bullMeat':'Meat'}
    def ShowAnimal():
        Text=''
        nonlocal i
        for keys,values in iterating_list[i].items():
            #correct the name from dictionary
            Text+=change_strings[keys]+str(values).rjust(spacing-len(change_strings[keys]))+'\n'
        label['text']=Text
    def Increasenum():
        nonlocal i
        i=i+1 if not i==len(iterating_list)-1 else 0
        ShowAnimal()
    def Decreasenum():
        nonlocal i
        i=i-1 if not i==0 else len(iterating_list)-1
        ShowAnimal()
    def Exit():
        for j in buttons:
            j.destroy()
        MonthlyCycle()
    def Slay():
        global money
        nonlocal i
        try: #to avoid key error
            price=getSlaughterPrice(iterating_list[i]['cowMeat'])
        except KeyError:
            price=getSlaughterPrice(iterating_list[i]['bullMeat'])
        if askyesno(title='Confirm', message='The butcher offers you '+str(price)):
            money+=price
            try:
                cowInfo.remove(iterating_list[i])
            except ValueError:
                bullsInfo.remove(iterating_list[i])
            iterating_list.remove(iterating_list[i])
            if i==0:
                Exit()
                return
            i-=1
        ShowAnimal()
    def Mate():
        nonlocal i
        if bullsInfo == []:
            showerror(message = "You don't have a bull buy one from market.")
        elif not i < len(cowInfo): # if the current list is not cowInfo
            showerror(message = "You can't mate a bull or calf with a bull.")
        elif cowInfo[i]['IsPregnant']:
            showinfo(message = 'This cow is already pregnant.')
        else:
            if askyesno(title='Confirm', message='Do you want to breed this cow? It will start to lose milk\
                after 5th month instead of 7th.'):
                iterating_list[i]['IsPregnant']=True
                iterating_list[i]['prgDate']=(year,month)
                cowInfo[i]['IsPregnant']=True
                cowInfo[i]['prgDate']=(year,month)
                showinfo(message='This cow is now pregnant.')
        ShowAnimal()
    def Sell():
        global money
        nonlocal i
        try: #to avoid key error
            price=CalculatePrice(iterating_list[i]['cowAge'][0],iterating_list[i]['cowMilk'],
                        iterating_list[i]['cowMeat'],iterating_list[i]['IsPregnant'],iterating_list[i]['prgDate'])
        except KeyError:
            price=CalculatePrice(iterating_list[i]['bullAge'][0],0,iterating_list[i]['bullMeat'])
            
        action=askyesno(title='Sell the animal', message='You have got offer of '
            +str(price)+'. Do you want to sell it?')
        if action:
            money+=price
            try:
                cowInfo.remove(iterating_list[i])
            except ValueError:
                bullsInfo.remove(iterating_list[i])
            iterating_list.remove(iterating_list[i])
            if i == 0:
                Exit()
                return
            i-=1
        ShowAnimal()
    if buttons == []:
        buttons.append(ttk.Button(buttonsFrame2, text='Prev', command = Decreasenum))
        buttons.append(ttk.Button(buttonsFrame2, text='Next', command = Increasenum))
        buttons.append(ttk.Button(buttonsFrame2, text='Slaughter/Slay', command = Slay))
        buttons.append(ttk.Button(buttonsFrame2, text='Exit', command = Exit))
        buttons.append(ttk.Button(buttonsFrame2, text='Sell', command = Sell))
        buttons.append(ttk.Button(buttonsFrame2, text='Mate', command = Mate))
        for j in buttons:
            j.pack(side='right', anchor='center')
            j['style']='my.TButton'
    ShowAnimal()

buttonsFrame = ttk.Frame(window)
buttonsFrame.pack(side='left',anchor='n',before=label)

ttk.Button(buttonsFrame, text="Go to the market", command = GoToMarket, style = 'my.TButton'
    ).pack(side='top', anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame, text="Show animals", command = ShowAnimals, style = 'my.TButton'
    ).pack(side='top', anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame, text="Next Month", command = MonthlyCycle, style = 'my.TButton'
    ).pack(side='top', anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame,text="Quit", command = window.destroy, style = 'my.TButton'
    ).pack(side='top', anchor='w', pady=10, padx=20)

window.mainloop()
