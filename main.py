import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# url = "https://nptel.ac.in/courses/105108127/#downloads"
url = "https://nptel.ac.in/courses/105108127"
folder_location = r'nptelCourse'

if not os.path.exists(folder_location):
    os.mkdir(folder_location)

response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")    
print(soup.find('title').text) 

count = 1
list_files = []
for tr in soup.select("tr"):
    check = 0
    for td in tr:
        if check == 0: # To traverse through the tr's
            mod_file = td.text
            mod_file_str = "Module "+str(count)+" - "+tr.td.text
            if mod_file not in list_files:
                os.mkdir(folder_location+"/"+mod_file_str)
                list_files.append(mod_file)
                count+=1
            check+=1
            continue
        
        if check == 1:
            
            link = td.select("a[href$='']")
            req = link[0]['href'].split('/')
            mod_no = int(req[6][-1])
            target = "Module "+str(mod_no)+" - "+list_files[mod_no-1]
            lessonfiles = []
            if('Lesson' in link[0].text):
                loc_file_loc = folder_location+"/"+target+"/"+link[0].text[:8]
                if not os.path.exists(loc_file_loc):
                    os.mkdir(loc_file_loc)
            else:
                loc_file_loc = folder_location+"/"+target
            orgfile = link[0]['href'].split('/')[-1]
            files_dir = os.listdir(loc_file_loc)
            if(orgfile[len(orgfile)-4:] == '.pdf'):
                filename = os.path.join(loc_file_loc,link[0].text+".pdf")     
                if filename.split('/')[-1] in files_dir:       
                    filename = os.path.join(loc_file_loc,link[0].text+str(files_dir.count(filename)+1)+".pdf")
            elif(orgfile[len(orgfile)-4:] == '.doc'):

                filename = os.path.join(loc_file_loc,link[0].text+".doc")

            with open(filename, 'wb') as f:
                print("downloading "+ filename +" ...")
                f.write(requests.get(urljoin(url,link[0]['href'])).content)
            
            break
