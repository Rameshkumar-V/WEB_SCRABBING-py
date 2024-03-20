from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np

#for designing text intro: 
from pyfiglet import Figlet as ft
from termcolor import colored

import matplotlib.pyplot as plt




def scraper(rollno_cstr,start,stop,url):
    all_data = [] # List to accumulate data from each iteration
    codes=[]

    try:
         with open('subcodes.txt','r') as f:
            data=f.readlines()

            for i in data:
                codes.append(str(i).replace('\n',''))
            print('Datas iniiiiii')
    except Exception as e:
        print('err on code init section ')
        pass
    print(codes)

    #codes=['IV', 'III', '']


    for n in range(start, stop):
        sub_title = np.array([])
        sub_totals = np.array([])
        sub_result = np.array([])
        sub_perc_total_list = np.array([])
        ex_data = {}
        no = f'u22csc{str(n).zfill(3)}'
        no = f'{str(rollno_cstr)}{str(n).zfill(3)}'

        chrome_driver_path = r'D:\WEB-SCRABBING\chromedriver\chromedriver-win64\chromedriver-win64\chromedriver.exe'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

        wd = webdriver.Chrome(options=chrome_options)

        result_p_link = "https://www.nmc.ac.in/results/res_april2023.html"
        wd.get(result_p_link)

        inp_field = wd.find_element(By.NAME, "kmr")
        inp_field.send_keys(no)

        submit_btn = wd.find_element(By.NAME, "Submit")
        submit_btn.click()

        roll_std = no
        name_std = wd.find_element(By.XPATH, "/html/body/center/table/tbody/tr[1]/td/b/b/b")
        print('name is : ',name_std)

        table = wd.find_element(By.TAG_NAME, 'table')
        table_row = table.find_elements(By.TAG_NAME, "tr")

        try:

            for row in table_row[2:-1]:
                datas = [data.text for data in row.find_elements(By.TAG_NAME, 'td')]
                print('datas is : ',datas)
                sub_title = np.append(sub_title, datas[1])
                sub_totals = np.append(sub_totals, datas[4])
                sub_result = np.append(sub_result, datas[5])

             
                if any(str(substring).strip()==str(datas[0]).strip() for substring in codes):
                   
                    sub_perc_total_list = np.append(sub_perc_total_list, int(datas[4]))
                else:
                  

                    pass
        except Exception as e:
            print('Table not found on your weblink !')

        val = np.shape(sub_perc_total_list)[0]
        print('val is : ',val)
        print('percentge list : ',sub_perc_total_list)
        try:
            percentage = (sum(sub_perc_total_list) / val)
            print('percentage counted successfully !')
        except Exception as e:
            print('error on percentage')
            percentage=0

        ex_data.update({"ROLL NO": roll_std, 'NAME': name_std.text})
        ex_data.update({sub_title[i]: int(sub_totals[i]) for i in range(len(sub_title))})
        ex_data.update({"RESULT": str("Pass" if all(key == 'Pass' for key in sub_result) else "Fail")})
        ex_data.update({"PERCENTAGE": percentage})

        all_data.append(ex_data)
        wd.close()

        #time.sleep(1)

        

    wd.quit()
    df = pd.DataFrame(all_data)
    df.set_index('ROLL NO', inplace=True)
    print("all list : = ",all_data)
    filename: str=str(input("ENTER EXCEL FILE NAME : "))

    df.to_excel(f'{filename}.xlsx')
    print(colored("NOTE  ! ","green"),"You want Barchart for this data  (Yes / No) :")
    while True:
        entry=str(input('Enter : '))
        if(entry=='Yes'):
            print(colored('PLOTTING ...','yellow'))
            plotting(all_data)

            break
        elif(entry=='No'):
            print(colored('Finishing ...','yellow'))
            break
        else:
            print('INVALID INPUT RETRY !')
            continue


    

def plotting(datas):
    print(colored("Maximum 50 records Process at a Chart ! ",'red'))
    roll_no=np.array([])
    percentage=np.array([])

    for data in datas:
        roll_no=np.append(roll_no,str(data['ROLL NO']))
        percentage=np.append(percentage,int(data['PERCENTAGE']))


    plt.bar(roll_no,percentage)
    plt.ylim(0,100)
    plt.yticks(range(0,101,10))

    for m,n in enumerate(percentage):
        plt.text(m,n+1,f'{n}%',ha='center')

    filename=str(input("Enter File Name for Save plot img : "))
    plt.savefig(filename)
    plt.show()
    
    plotting_subjects(datas)




    print('DATA IS : ',data)
    pass

def plotting_subjects(datas):

    if(datas and len(datas)>=2):

        titles=datas[0].keys()

        dictionary={}

        for topic in titles:
            submark_collection=np.array([])
            for j in datas:
                mark=j[str(topic)]
                submark_collection=np.append(submark_collection,mark)
            dictionary[str(topic)]=list(submark_collection)

        piec_names=[]
        piec_perc=[]
        subname=list(dictionary.keys())[2:-2]

        for subnames in subname:
        
            percentage=(sum(dictionary[str(subnames)])) / (100*len(dictionary[str(subnames)])) * 100
            piec_names.append(str(subnames[0:10]))
            piec_perc.append(int(percentage))
        print('plotting started')
            


        plt.bar(piec_names,piec_perc)
        plt.ylim(0,100)
        plt.yticks(range(0,101,10))
        #plt.xticks(rotation='vertical')
        plt.title("SUBJECT CALCULATION")
        for m,n in enumerate(piec_perc):
            plt.text(m,n+1,f'{n}%',ha='center')

        plt.savefig("SUBJECTCALCULATION")
        plt.show()

        pass




def main():

    def intro_app():
        font=ft(font='slant')

        clr_text=font.renderText('RK UNIVERSE ')


        print(colored(clr_text,'blue'))
        for i in range(100):
            print(colored('-','red'),end='')
        print('\n \n \n \n')


    intro_app()



    def scrab_start():
        

        while True:
            url : str =str(input("ENTER YOUR RESULT PAGE URL : "))
            rollno_cstr=str(input("ENTER COMMON Roll No STRING : ")).strip()
            start=int(input("ENTER NO 1 TO 40 : "))
            stop=int(input("ENTER END NO 2 TO 50 : "))

            print(type(url).__name__)
            if(type(url).__name__=='str' and type(rollno_cstr).__name__=='str') and len(url)>=20 and len(rollno_cstr)>=3:
                if start>=1 and stop<=60:
                    scraper(url=url,start=start,stop=stop,rollno_cstr=rollno_cstr)
                    break
                    pass
                else:
                    print(' ENTER START AND STOP (1-60)')
                    continue
            else:
                print('INVALID input !')
                continue
    def subcode_add():
       
            no=int(input('How many codes : '))
            for i in range(no):
                code=str(input('Enter code : '))
                code=str(code)+'\n'
                with open('subcodes.txt','a') as f:
                    f.write(code)
            print('Finish')
    def subcode_delall():

        confirm=str(input('Confirm to Delete all codes : (Yes / No) :'))

        if confirm=='Yes':
            with open('subcodes.txt','w') as f:
                    f.truncate()
                    print('Finished')
        else:
            print('Cancelled...')
    def subcode_view():

        print('YOUR SUBJECT CODES ')
        with open('subcodes.txt','r') as f:
            data=f.readlines()
            for i in data:
                print(i)
        print('Showed...')




    msg="""
        [1]-> Start Scrabbing
        [2]-> Percentage Code Adding
        [3]-> Percentage Code Viewing
        [4]-> Percentage Code Deleting All
        [5]-> Close """
    print(colored(msg,'green'))

    while True:
        key=int(input('Enter Key : '))
        if key==1:
            scrab_start()
        elif key==2:
            subcode_add()
        elif key==4:
            subcode_delall()
        elif key==3:
            subcode_view()
        elif key==5:
            print('Exited...')
            break
        else:
            print('Invlid Key Retry !')



main()


