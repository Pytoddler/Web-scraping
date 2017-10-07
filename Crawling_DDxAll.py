from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()
list_alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','V','W','X','Y','Z']
f = open('DDx All.txt','w',encoding = 'UTF-8')
f.write("DDx All as below")
f.close()

for i in range(25):
    url = "https://accessmedicine.mhmedical.com/Diagnosaurus.aspx?categoryid=41309&selectedletter="+str(list_alphabet[i])
    browser.get(url)

    browser.implicitly_wait(10)
    DDx_list = browser.find_elements_by_id('leftNav')

    print(str(list_alphabet[i])+": "+str(len(DDx_list))+" ddx\n")
          
    f = open("DDx All.txt",'a',encoding = 'UTF-8')
    f.write(str(list_alphabet[i])+": "+str(len(DDx_list))+" ddx\n")
            
    with open("DDx All.txt",'a',encoding = 'UTF-8') as f:
        for i in range(len(DDx_list)):
            f.write(DDx_list[i].text+"\n")

f.close()
browser.close()