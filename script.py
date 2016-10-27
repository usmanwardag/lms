from bs4 import BeautifulSoup
import requests
import os

import warnings
warnings.filterwarnings('ignore')

from tqdm import tqdm

# Create a persistent global session
s = requests.session()

url = 'https://lms.nust.edu.pk/portal/login/index.php'
values = {'username': '13beeukhan',
          'password': 'Islamabad1_'}

powerpoint = 'https://lms.nust.edu.pk/portal/theme/image.php/nust/core/1464680422/f/powerpoint-24'
pdf = 'https://lms.nust.edu.pk/portal/theme/image.php/nust/core/1464680422/f/pdf-24'
word = 'https://lms.nust.edu.pk/portal/theme/image.php/nust/core/1464680422/f/document-24'

def log_in():
    return s.post(url, data=values, verify=False).content

def routine():
    source = log_in()
    tree = BeautifulSoup(source, 'html.parser')

    # Iterate through all current courses (which have 'id' 1)
    for t in tree.findAll('div', {'id': '1'}):

        # Find course links and titles
        courses = t.findAll('div', {'class': 'course_title'})
        links = [c.findChildren('a')[0]['href'] for c in courses]
        titles = [c.findChildren('a')[0]['title'] for c in courses]
        
        # Create course folder if they do not already exist
        for title in titles:
            if not os.path.exists(title):
                os.makedirs(title)
                os.makedirs(title+'/'+'Labs')
                os.makedirs(title+'/'+'Assignments')

        # Check for files that are already downloaded
        files = []
        for root, subdirs, f in os.walk(os.getcwd()):
            files.append(f)
            
        all_files = []
        map(all_files.extend, files)
        
        # Iterate through course contents and download any new material
        for link, title in zip(links, titles):    
            chtml = s.get(link, verify=False).content
            ctree = BeautifulSoup(chtml, 'html.parser')
            
            # Check for all resources
            for t in ctree.findAll('li', {'class': 'activity resource modtype_resource'}):
                r_image = t.findChildren('img')[0]['src']
                
                # File extension
                if r_image == powerpoint: 
                    r_type = '.pptx'
                elif r_image == pdf: 
                    r_type = '.pdf'
                elif r_image == word: 
                    r_type = '.docx'
                else: 
                    continue
                
                # File link 
                r_link = t.findChildren('a')[0]['href']
                print r_link
                
                # File name
                r_title = t.findAll('span', {'class': 'instancename'})[0].text + r_type
                print r_title
                
                # Move on if file aready exists
                if r_title in all_files: 
                    continue
                
                # Some pattern matching to classify files
                if 'lab' in r_title.lower():
                    r_title = title + '/Labs/' + r_title
                elif 'assignment' in r_title.lower():
                    r_title = title + '/Assignments/' + r_title
                else:
                    r_title = title + '/' + r_title
                
                # If pdf, need to do some extra work to get file link
                if r_type == '.pdf':
                    page = s.get(r_link, verify=False).content
                    page_tree = BeautifulSoup(page, 'html.parser')
                    
                    r_link = page_tree.findAll('object', {'type': 'application/pdf'})[0]['data']
                    print 'Modified: ', r_link
                
                # Download file now  
                response = s.get(r_link, stream=True, verify=False)
                
                with open(r_title, "wb") as handle:
                    for data in tqdm(response.iter_content()):
                        handle.write(data)

routine()