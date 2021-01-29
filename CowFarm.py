from datetime import date, timedelta

from tkinter import ttk
from tkinter.font import Font
import tkinter as tk
from tkinter.messagebox import *
from random import randint, choice

testing = False

window=tk.Tk()

# Introduction to the game.
if testing == False:
    showinfo(title="Introduction", message="Dairy Farm Game!\n\n\
        Your goal is to earn money by selling milk\n\
        This paragraph will inform you about milk production in this game.\n\
        Milk production depends upon age of the cow, \
        the young the cow the profitable it will be.\n\
        Milk of a cow will decrease over time, \
        it will be increased if your cow gives birth to a calf.\n\
        You can mate a cow with a bull.\n\
        There are much chances that your cow will die after 8 years.")

# change these if you are unsatisfied with the economy.
money=100000 # Starting money
milkPrice=100
grassPriceRainy=300
grassPriceSunny=400
rainyMonths=(4,5,6,7,8) # Months in which rains
rainProbability=1/3
cowsInMarket=7 # Amount of cows on sale in the market
# milk of a cow changes with age.
# key is age. value is milk
ageMilkRelation={1:10,2:11,3:randint(11,13) ,4:randint(12,15) ,5:12 ,6:randint(10,11), 7:randint(9,10)}
# change these if you don't follow English months.
monthNames=('', 'January','February','March','April','May','June','July','August','September','October','November','December')
# change these if you don't follow the solar calendar.
monthDays=(0,31,28,31,30,31,30,31,31,30,31,30,31)

current_date=date(1900, 1, 1)
profit=0
milk=0 

window.title('Dairy Farm')
window.geometry('800x400')

class Animal():
    def __init__(self,
                birthDay: date,
                gender: str,
                meat: int,
                milk: int=0,
                ispregnant: bool=False, 
                prgDate: date = date(1900, 1, 1)):
        if not gender in ('male', 'female'):
            raise 'gender can only be male or female'
        self.birthDay = birthDay
        self.gender = gender
        self.meat = meat
        self.milk = milk
        self.age = [current_date.year - self.birthDay.year,
                    current_date.month - self.birthDay.month]
        
        if gender == 'female':
            self.ispregnant = ispregnant
            self.prgDate = prgDate
            
    def MonthlyCycle(self):
        if [self.age[0], self.age[1]] < [1,4]:
            #calf drinks milk until 3 months
            if self.age[1] < 4: self.milk-=1
            # else it eats grass
            else: grass+=100*monthDays[month]
        if self.age[0] != 12:
            self.age[1] += 1
        else:
            self.age[0]+=1
            
        if self.age[0] >= 8 and randint(0,3)!=1:
                showinfo(message = 'Unfortunately, one of your '
                    + ('bulls' if self.gender=='male' else 'cows') +
                    'has died')
        if self.gender  == 'female' and self.ispregnant:
            # Get no: of month in which the cow got pregnant by using `year*12+months`.
            # +9: after 9 months a calf will be born
            #if self.prgDate[0]*1+self.prgDate[1]+9 <= year*12+month:
            if current_date > date(self.prgDate.year, 
                                self.prgDate.month+9,
                                self.prgDate.day):
                self.ispregnant=False
                self.milk=ageMilkRelation[self.age[0]][0]+meat
                Gender=choice(['female','male'])
                Animal(current_date, Gender, 5)
                showinfo(message=f'A {Gender} calf is born!')

    def getSalePrice(self):
        price=0
        if self.gender == 'female':
            agePriceRelation = {7:35000, 1:70000, 6:54000, 2:65000, 3:60000, 4:57000, 5:50000}
            #meatMilkRelation={10:15,9:14,8:13,7:12,6:11,5:10,4:9,3:8,2:7,1:6}
            price=agePriceRelation[self.age[0]]+\
                self.milk*1000+\
                self.meat*2000
            if self.ispregnant:
                price+=10000
        else:
            price = self.meat*3000
        
        return price

    def getSlaughterPrice(self):
        return self.meat*9000
    
    def getForShowing(self):
        '''Create a dictionary'''
        animalDict = {'BirthDay': self.birthDay,
                'Age': self.age,
                'Gender': self.gender,
                'Meat': self.meat,
                'Price': self.getSalePrice()}
        if self.gender == 'female':
            animalDict['Milk'] = self.milk
            animalDict['IsPregnant'] = self.ispregnant
            if self.ispregnant:
                animalDict['Pregnant Date'] = str(self.prgDate)
        Text=''
        spacing = 20
        
        for keys,values in animalDict.items():
            Text += keys+str(values).rjust(spacing-len(str(keys)))+'\n'
        return Text
        
def getGrassPrice(weather):
    return grassPriceSunny if weather == "sunny" else grassPriceRainy

# Doesn't work
def getFoodRequirement(meat):
    meatFoodRelation={10:600,9:550,8:500,7:450,6:400,5:350,4:300,3:250,2:250,1:250}
####
s=ttk.Style()
Font=('Helvetica', 12)
s.theme_settings('xpnative',
    settings={'TButton': {'configure': {'font': Font}},
            'TLabel': {'configure': {'font': Font}}})
s.theme_use('xpnative')

label=ttk.Label(window)
label.pack(side='top', anchor = 'center')
buttonsFrame2=ttk.Frame(window)
buttonsFrame2.pack(side='top')

class Farm:
    def __init__(self):
        self.animals=[]
        
    def get_all_animals(self):
        return self.animals
        
    def add_animal(self, animal: Animal):
        self.animals.append(animal)
        
    def delete_animal(self, animal: Animal):
        self.animals.remove(animal)
        
farm=Farm()

def MonthlyCycle(): #Main game window update
    global current_date, money, profit, milk

    weather='sunny'
    if current_date.month in rainyMonths: #monsoon
        weather='rainy' if randint(1,3) == 2 else 'sunny'
    cows, bulls, calves = (0,0,0)
    for i in farm.get_all_animals():
        if current_date < (i.birthDay + timedelta(9*30)):
            calves+=1
            
        if i.gender == 'male':
            bulls+=1
        else:
            cows+=1
    label['text']=("Money : "+str(money)+
        "\nProfit : "+str(profit)+
        "\nCows :  "+str(cows)+
        "\nBulls : "+str(bulls)+
        "\nCalves : "+str(calves)+
        "\nTotal Milk: "+str(milk)+
        "\n            Year: "+str(current_date.year)+
                " Month: "+monthNames[current_date.month]+
        "\nMonthly Weather Conditions: "+weather)

    #destroy buttons created from previous interactions
    for i in buttonsFrame2.pack_slaves():
        i.destroy()
    
    milk=0
    grass=getGrassPrice(weather)*monthDays[current_date.month]*( cows+bulls )
    for i in farm.get_all_animals():
        i.MonthlyCycle()
    profit=(milk*50*monthDays[current_date.month])-grass #Total profit = Income-Maintanence
    money+=profit 
    current_date+=timedelta(days=monthDays[current_date.month])
    
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
            marketInfo.append(Animal(
               current_date.replace(current_date.year-age),
                gender,
                meat,
                ageMilkRelation[age]+meat))
                
        else:
            marketInfo.append(Animal(
                current_date.replace(current_date.year-age),
                gender,
                meat))
    spacing=30
    buttons=[]
    def BuyCow():
        global money
        nonlocal num
        if money >= marketInfo[num].getSalePrice():
            money-=marketInfo[num].getSalePrice()
            farm.add_animal(marketInfo[num])
            marketInfo.remove(marketInfo[num])
            showinfo(message='You have successfully bought the animal')
            if not marketInfo:
                Exit()
                return
            num=num-1 if num else 0
            InsideMarket()
    def InsideMarket():
        label.configure(text=marketInfo[num].getForShowing())
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
        buttonsFrame3=ttk.Frame(buttonsFrame2)
        buttonsFrame3.pack(side='top', anchor='w', pady=30)
        ttk.Button(buttonsFrame3, text='>>>>',
            command = Increasenum).pack(side='right')
        ttk.Button(buttonsFrame3, text='<<<<',
            command = Decreasenum).pack(side='right')        
        buttons.append(ttk.Button(buttonsFrame2, text='Buy', command = BuyCow))
        buttons.append(ttk.Button(buttonsFrame2, text='Exit', command = Exit))
        for i in buttons:
            i.pack(side='right', anchor='center')
    InsideMarket()
    
    if testing:
        for _ in range(cowsInMarket):
            BuyCow() # buy every animal for testing ShowAnimals() function
            Increasenum()
        BuyCow() 
        Decreasenum()
        Exit()

def ShowAnimals():
    i=0
    iterating_list = farm.get_all_animals()
    if iterating_list==[]:
        showerror(message="You don't have a cow or bull. Buy one from market.")
        return
    for j in buttonsFrame2.pack_slaves():
        j.destroy()
    spacing=30
    buttons=[]
    def ShowAnimal():
        nonlocal i
        Text=iterating_list[i].getForShowing()
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
        for j in buttonsFrame2.pack_slaves():
            j.destroy()
        MonthlyCycle()
    def Slay():
        global money
        nonlocal i
        price = iterating_list[i].getSlaughterPrice()

        if askyesno(title='Confirm', message='The butcher offers you '+str(price)):
            money+=price
            iterating_list.remove(iterating_list[i])
            if iterating_list == []:
                Exit()
                return
            i=i-1 if i else 0
        ShowAnimal()
    def Mate():
        nonlocal i
        for j in iterating_list:
            ispassing = False
            if j.gender == 'male':
                ispassing=True
            if ispassing:
                showerror(message = "You don't have a bull buy one from market.")
        if iterating_list[i].gender == 'male':
            showerror(message = "You can't mate a bull with a bull.")
        elif iterating_list[i].age <= [0, 9]:
            showerror(message = "You can't mate a calf with a bull.")
        elif iterating_list[i].ispregnant:
            showinfo(message = 'This cow is already pregnant.')
        else:
            if askyesno(title='Confirm', message='Do you want to breed this cow? It will start to lose milk\
                after 5th month instead of 7th.'):
                iterating_list[i].ispregnant = True
                iterating_list[i].prgDate = current_date
                showinfo(message='This cow is now pregnant.')
        ShowAnimal()
    def Sell():
        global money
        nonlocal i
        print(iterating_list)
        price = iterating_list[i].getSalePrice()
        action=askyesno(title='Sell the animal',
            message='You have got offer of '
                        +str(price)+'. Do you want to sell it?')
        if action:
            money+=price
            iterating_list.remove(iterating_list[i])
            if iterating_list == []:
                Exit()
                return
            i=i-1 if i else 0
        ShowAnimal()
    if buttons == []:
        buttonsFrame3=ttk.Frame(buttonsFrame2)
        buttonsFrame3.pack(side='top', anchor='center', pady=20)
        ttk.Button(buttonsFrame3, text='>>>>',
            command = Increasenum).pack(side='right', padx=60)
        ttk.Button(buttonsFrame3, text='<<<<',
            command = Decreasenum).pack(side='left')
        buttons.append(ttk.Button(buttonsFrame2, text='Slaughter/Slay', command = Slay))
        buttons.append(ttk.Button(buttonsFrame2, text='Exit', command = Exit))
        buttons.append(ttk.Button(buttonsFrame2, text='Sell', command = Sell))
        buttons.append(ttk.Button(buttonsFrame2, text='Mate', command = Mate))
        for j in buttons:
            j.pack(side='right', anchor='center')
    ShowAnimal()
    if testing:
        Increasenum()
        Decreasenum()
        Slay()
        Sell()
        Mate()
        Exit()

def ChangeTheme():
    themes=s.theme_names()
    current_theme=themes.index(s.theme_use())
    current_theme=themes[current_theme+1 if current_theme != len(themes)-1 else 0]
    s.theme_settings(current_theme,
                settings={'TButton': {'configure': {'font': Font}},
                          'TLabel': {'configure': {'font': Font}}})
    s.theme_use(current_theme)

buttonsFrame = ttk.Frame(window)
buttonsFrame.pack(side='left',anchor='n', before=label)

ttk.Button(buttonsFrame, text="Go to the market", command = GoToMarket
    ).pack(anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame, text="Show animals", command = ShowAnimals
    ).pack(anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame, text="Next Month", command = MonthlyCycle
    ).pack(anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame, text="Change Theme", command = ChangeTheme
    ).pack(anchor='w', pady=10, padx=20)
ttk.Button(buttonsFrame,text="Quit", command = window.destroy
    ).pack(anchor='w', pady=10, padx=20)
    
if testing:
    GoToMarket()
    ShowAnimals()
    MonthlyCycle()
    
window.mainloop()
