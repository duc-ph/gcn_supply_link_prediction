## import dependencies
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

## create an object of the chrome webdriver
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
## open selenium URL in chrome browser
driver.get('https://www.marklines.com/en/members/login')


#driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div[1]/a/span').click()
time.sleep(2)#wait

#input id
driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div[5]/div/div[1]/div[2]/div/div[2]/div/div/form/div[1]/input').send_keys('oroaUBdlN8')
#input password
driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div[5]/div/div[1]/div[2]/div/div[2]/div/div/form/div[2]/input').send_keys('pw4a39')
#click login button
driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div[5]/div/div[1]/div[2]/div/div[2]/div/div/form/div[3]/div[4]/button').click()

time.sleep(5)#wait

#scroll to bottom
driver.execute_script("window.scrollTo(19, 1427)")

time.sleep(2) #wait

driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/ul/li[10]/ul/a[1]/li/span').click()


driver.execute_script("window.scrollTo(200, 1427)")

#suppliers to check out (starting, will add more as we find more)
nodes_to_check = ['Volvo']

#navigate to search bar, make it an exact match, enter the first supplier to search, press enter to search
time.sleep(3)#wait
driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[5]/form/div/div/label[2]/input').click()
time.sleep(1)
driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[5]/form/input').send_keys(nodes_to_check[0])
time.sleep(1)
driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[5]/form/input').send_keys(Keys.RETURN)
#driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/ul/li[10]/ul/a[1]/li/span').click()
time.sleep(2)#wait


nodes_checked = []
current_supplier = ''
nodes = []

try:
    while len(nodes_to_check) > 0:
        if len(nodes_checked) == 0: #we are on the first supplier
            #move to checked and set current
            current_supplier = nodes_to_check[0]
            del nodes_to_check[0]
            nodes_checked.append(current_supplier)
        else: #check the next supplier
            print("----------------------NEW SUPPLIER------------------")
            #get next supplier
            current_supplier = nodes_to_check[0]
            del nodes_to_check[0]
            nodes_checked.append(current_supplier)

            search_input_elm = driver.find_element("xpath", '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/section[1]/div[3]/form/input')
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(1)
            driver.execute_script(f"window.scrollTo({search_input_elm.location['x']}, {search_input_elm.location['y']})")
            time.sleep(1)
            search_input_elm.clear()
            search_input_elm.send_keys(current_supplier)
            search_input_elm.send_keys(Keys.RETURN)
            time.sleep(2)
            

        try: #try to get this seller's customers
            more_pages = True #go through first page
            
            while more_pages: #while there are more pages for the current supplier, 
                driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(1)
                print('next page')
                for supplier in driver.find_elements(By.CLASS_NAME,'supplier_name'):
                    supplier_root = supplier.text.split(' ')
                    #the root is the first two words, unless the name is only one word or 
                    #if the second word has a '(', which means that it is something like '(usa office)' and is unneeded
                    supplier_root = f'{supplier_root[0]} {supplier_root[1]}' if (len(supplier_root) > 2 and '(' not in supplier_root[1]) else supplier_root[0]
                    
                    if len(supplier_root) > 1:
                        node = (current_supplier.replace(',',''),supplier_root.replace(',','')) #take away commas, as some names include commas
                        print(node)
                        nodes.append(node) #the current supplier is supplied by the specified supplier, so add it
                        if supplier_root not in nodes_to_check and supplier_root not in nodes_checked: #if the root is not yet saved, save it
                            nodes_to_check.append(supplier_root)
                            #print(supplier.text)
                
                #check if there are more pages
                try:
                    found = False
                    for page_item in driver.find_elements(By.CLASS_NAME,'page-link'):
                        #print(page_item.text)
                        #print(page_item.get_attribute('href'))
                        if page_item.text == '›':
                            found = True
                            driver.execute_script(f"window.scrollTo({page_item.location['x']}, {page_item.location['y']})")
                            time.sleep(1)
                            page_item.click()
                            
                            
                            break
                    if not found: #did not find it, stop looking
                        more_pages = False
                except Exception as e:
                    print(e)
                    #more_pages = False
        except:
            print("no suppliers for this supplier")

except:
    print('error on browser side, skipping to printing')

    #finished checking this supplier's suppliers


print("saving to csv")

with open('nodes.csv','w', encoding="utf-8") as f:
    writer=csv.writer(f, delimiter=' ',lineterminator='\n',)
    for node in nodes:
        writer.writerow(f'{node[0]},{node[1]}')\
        

print('DONE')

driver.quit()