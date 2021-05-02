import sys
import csv
import matplotlib
import matplotlib.pyplot as plt


MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']

#python invest.py Transaction_History.csv 2021

def main(argv):
    ''' i dont want to manually have to update my divedend graphs on google docs '''
    
    if validate_input(argv) ==1:
        return 0 #kill the program
        
    cat=format_input(argv)#new_name, format
    
    #return 0
    while True:
        div=get_div(cat,argv)  #dict for div earned
        reinvest=get_reinvest(cat,argv) #dict for reinvest
        div_left=get_div_reinvest(div, reinvest) #how much $ is not re invest
        symbols=get_unique(div) #make a list of the instances of the symbol
        choice=user_options(symbols,reinvest) #user_choice returns: symbol, year_pref[y\n], reinvest
        earnings=data_for_plot(choice[0], div)#shows the div earned per month
        date_reinvest=get_reinvested(reinvest,choice,div_left,div) #these are the dates that $ was reinvested
        
        
        graph_symbol(choice, earnings, argv)
        graph_reinvest(choice,date_reinvest,argv,symbols)
        graph_year(choice,symbols, div,argv )
        
        done=input("Quit?:[Y/N]: ").upper() 
    
        if done =='Yes' or done=="Y":
            break
    
    print("Hope it was use ful :)")

def graph_symbol(choice, earnings, argv): #graphs the indi symbol
    g_tite=choice[0]+" gross earnings: $"+str(round(sum(earnings),2))+" for "+str(argv[2])
    graph_stuff(MONTHS, earnings,choice[0],argv,g_tite)#individual symbols  #this graphs the info for the symbol selected

def graph_year(choice,symbols, div,argv ):
    if choice[1]=="YES" or choice[1]=='Y': #show the procedings for the year 
        earned=year_preformance(symbols,div)
        g_tite=str(argv[2])+"'s total earngings: $"+str(round(sum(earned),2))
        graph_stuff(MONTHS, earned, choice[0], argv, g_tite)

def graph_reinvest(choice,date_reinvest,argv,symbols ):
    if choice[2]=="YES" or choice[2]=="Y": #shows on what dates i reinvested on
       #i just want to see amount reinvested
        net_gain=round(sum(date_reinvest[2])+sum(date_reinvest[1]),2)
        g_tite=str(argv[2])+" month's reinvestment in "+str(choice[0])+' net gain:$ '+str(net_gain)
        
        #''' https://bit.ly/3nEMvpV
        fig, ax = plt.subplots(figsize=(10,8),facecolor="#C6CDCC")
        
        months=[]
        for a in range(len(MONTHS)):
            #continue
            months.append(MONTHS[a]+":"+str(date_reinvest[3][a]))#pc bought) )
            
        #data for the graph #feed in test 
        p1=ax.bar(months,date_reinvest[2], .45, label='Dividend') #pure div
        p2=ax.bar(months,date_reinvest[0], .45, label='Reinvested')#re invest
        p3=ax.bar(months,date_reinvest[1], .45, label='Dividend Left', bottom=date_reinvest[0]) #div left 
        
        #labels for the graph
        ax.bar_label(p1, label_type='center')
        ax.bar_label(p2, label_type='center')
        ax.bar_label(p3, label_type='center')
        
        #visuals of the graph
        #graph_apperance(choice, argv, None,g_tite)
        plt.tick_params(axis='x', rotation=35)
        plt.title(g_tite)
        plt.ylabel('$ earned')
        plt.xlabel("Month: PC Reinvested")
        plt.legend(['Pure Dividend','Dividend Reinvested', 'Dividend Left'])
        
        plt.show()
    
def user_options(symbols,reinvest): #needs un-mute 
    for a in enumerate(symbols):
        #continue#unmute when done
        print(a)
    
    user_choice=int(input("Which symbol's gross div do you want to see?:[2]:  "))
    #user_choice=0
    
    show_reinvest='No'
    #print(symbols[user_choice])
    if symbols[user_choice] in get_unique(reinvest):
        show_reinvest=input("Do you want to see amount re-invested?:[Y/N]: ")
        #show_reinvest='Yes'
    
    show_year_preformance=input("Do you want to see years preformance?:[Y/N]: ")
    #show_year_preformance='N'
    
    #print(show_reinvest)
    return symbols[user_choice], show_year_preformance.upper(), show_reinvest.upper()

def get_reinvested(reinvest,choice,div_left,div):
    dates=[] #stores the dates that i got re-invested
    remain_div=[] #store the div that is cash 
    div_no_reinvest=[] #a list of the dates that i did not reinvest 
    pc_bought=[]
    for a in range(len(MONTHS)):
        dates.append(0)
        remain_div.append(0)
        div_no_reinvest.append(0)
        pc_bought.append(0)
        
    
    for a in reinvest:
        if choice[0] == a['symbol']:
            #date working with 
            date=a['date'].split(' ')
            for m in range(len(MONTHS)):
                if date[1] == MONTHS[m]:
                    dates[m]=a['spent'] *-1
        
    for a in div_left:
        if choice[0]== a['symbol']:
            date=a['date'].split(' ')
            for m in range(len(MONTHS)):
                if date[1] == MONTHS[m]:
                    remain_div[m]=a['remain_$']
                    pc_bought[m]=a['q_bought']
                    
    for a in div:
        if choice[0]== a['symbol']:
            date=a['date'].split(' ')
            for m in range(len(MONTHS)):
                if date[1] == MONTHS[m]:
                    if dates[m]==0:
                        div_no_reinvest[m]=a['earned']
                        
    
    '''# not sure if needed rn 
    for a in div:
        if choice[0] == a['symbol']:
            date=a['date'].split(' ')#date working with 
            for m in range(len(MONTHS)):
                if date[1] == MONTHS[m]:
                    if dates[m] ==0: #if its empty after assighnment assighn div to them 
                        dates[m]=a['earned']
    
    '''
    return dates, remain_div, div_no_reinvest, pc_bought

def year_preformance(symbols,div):
    #i want to see years earings
    dates=[]
    for a in range(len(MONTHS)):
        dates.append(0)
    
    #print(len(dates))
    for a in symbols:
        earned=data_for_plot(a, div)
        #print(a,earned,'\n')
        for a in range(len(earned)):
            dates[a]+=earned[a]
    
    return dates
    
def graph_stuff(MONTHS, earnings,choice, argv,g_tite):
    graph_apperance(choice,argv,earnings,g_tite)
    plt.bar(MONTHS, earnings,color='#245612')
    
    plt.show()
    
def graph_apperance(choice,argv,earnings,g_tite): #how i want the graphs to look 
    ''' 
    i want havew a graph that shows me the divedent that i recived per month per symbol
        On the same graph 
            i want to see the pc bought in a bar graph
            I want to see div left over as a line above the bargraph
            i want to see the div growth in a connected scattered
    
    #https://bit.ly/3sQOxEv 
    '''
    #--------- estetics
    plt.figure(figsize=(10,8),facecolor='#C6CDCC')
    addlabels(MONTHS,earnings)
    plt.tick_params(axis='x', rotation=35)
    # ---------labels
    plt.title(g_tite)
    plt.ylabel('$ earned')
    plt.xlabel("Month's earnings")
    
def addlabels(x,y): #credit: https://bit.ly/31ECTkN
    if y== None:
        return 0
    for i in range(len(x)):#rotation=45
        plt.text(i, y[i], y[i], ha = 'center' ,Bbox = dict(facecolor = 'white', alpha =.6))

def data_for_plot(choice, div):
    ''' get the data for the purpose of plotting
        currently: if i get div in march that is the 'jan'
        so i need to go over MONTHS 
            if the payment matches add the $ to that month,
            elif: earings[month] ==None set it to 0
    dates=[]
    earnings=[]
    
   
    for d in div:
        if d['symbol']==choice:
            earnings.append(d['earned'])
            date=d['date'].split(' ')
            dates.append(date[1])
            

    for a in MONTHS: #creates data for the rest of the year  
        if a not in dates:
            earnings.append(0)
            dates.append(a)
    '''
    
    earnings=[]
   
    for a in range(12):#populate with none
        earnings.append(0)
    
    counter=-1
    for m in MONTHS: #m==January
        counter+=1
        for d in div:
            date=d['date'].split(' ')
            date=date[1] #date=January
            #can i find a date that matches for this symbol?
            #dose the symbol and month match?
            if (m==date) and d['symbol']==choice:
                #print(m, d['earned'], len(earnings) )
                earnings[counter]=d['earned']
                
    #print(len(earnings))
    for a in earnings:
        continue
        print(a)
    #print(len(earnings))
    return earnings

def get_unique(div):
    unique_symbols=[]
    for a in div:
        if a['symbol'] not in unique_symbols:
            unique_symbols.append(a['symbol'])

    return unique_symbols  

def get_div_reinvest(div, reinvest):
    '''i want to see what my net div is and how many pc i gained'''
    new_amounts=[]
    for r in reinvest:#the info im looking for
        r_date=r['date']
        r_symbol=r['symbol']
        for d in div:
            if r_date==d['date'] and r_symbol==d['symbol']:#if the months and symbol equal 
                div_left=round( (d['earned']+r['spent']),2)
                #i info for graphs
                new_dict={
                    'symbol':r_symbol,
                    'q_bought':r['Quantity'],
                    'remain_$':div_left,
                    'date':r_date,
                    'spent':r['spent']
                    }
                new_amounts.append(new_dict)
    
    return new_amounts
    
def get_reinvest(cat, argv):
    ''' i want the instances of reinvest'''
    with open(cat, 'r')as file:
        reader=csv.DictReader(file)
        dates=[]
        for i in reader:#i:instance
            #i want to see the instances of reinvest to make sure reinvest follows divedend
            date=i['Transaction Date'].split(' ')
            
            if i['Transaction Type'] =="Reinvest" and date[3]==argv[2]:
                
                new_dict={
                    'symbol': i['Symbol'],
                    'Quantity': i['Quantity'],
                    'spent':float(i['Amount']),
                    'date':i['Transaction Date'],
                    }
                
                dates.append(new_dict)
    return dates
    
def get_div(cat, argv):
    ''' get all the instances of div and append it to the list'''
    monies=[]
    with open(cat, "r")as file:
        reader=csv.DictReader(file)
        
        for item in reader:
            date=item['Transaction Date'].split(' ')#deal with the date
            
            if len(date)!=1 : #for empty cases
                if argv[2] == date[3]:#user:2021
                    day=date[2].split(',')
                
                    if item['Transaction Type'] == 'Dividend':  #check if div
                        #assighnment loop for symbols yet accounted for.
                        date=str(date[1])+' '+str(day[0])
                        new_dict={
                            'date':item['Transaction Date'],
                            'symbol':item['Symbol'],
                            'earned':float(item['Amount']),
                            '$_/_share':round(float(item['Price']),2),
                            }
                            
                        #print(item['Symbol'], item['Amount'])
                        monies.append(new_dict)
    
    return monies 

def format_input(argv):
    ''' the first 9 lines are infor that messes with ReadDict.
        format in such a wat to make the info usable to
        return the name of file working with
    '''
    with open(argv[1], "r") as csvfile:
        #read downloaded file into new file from line 7, formatting for dictReader
        cat=argv[1].split('.')
        cat[0]+="_copy.csv"
        reader=list(csv.reader(csvfile))
        
        counter=0
        open_at=0
        for item in reader:
            counter+=1
            if item[0]=='Transaction Date':
                open_at=counter-1
                #print(item)
        
        with open(cat[0], "w", newline='')as file:
            for item in reader[open_at:]:
                #print(item)
                write =csv.writer(file) 
                write.writerow(item)
    
    return cat[0] 

def validate_input(argv):
    if len(argv)!=3:
        print("\tusage: python invest.py data_input.csv year(2021) \n")
        print("\thope this is help full :)")
        return 1
    
    return 0
main(sys.argv)