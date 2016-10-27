from bs4 import BeautifulSoup
import requests
import os
import yaml

import warnings
warnings.filterwarnings('ignore')

from tqdm import tqdm

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
        
        # Create course folders if they do not already exist
        for title in titles:      
            dir_ = directory + '/' + title
            if not os.path.exists(dir_):
                os.makedirs(dir_)
                os.makedirs(dir_+'/'+'Labs')
                os.makedirs(dir_+'/'+'Assignments')

        # Check for files that are already downloaded
        files = []
        for root, subdirs, f in os.walk(directory):
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
                
                # File name
                r_title = t.findAll('span', {'class': 'instancename'})[0].text + r_type
                
                # Move on if file aready exists
                if r_title in all_files: 
                    continue
                
                # Some pattern matching to classify files
                if 'lab' in r_title.lower():
                    r_title = directory + '/' + title + '/Labs/' + r_title
                elif 'assignment' in r_title.lower():
                    r_title = directory + '/' + title + '/Assignments/' + r_title
                else:
                    r_title = directory + '/' + title + '/' + r_title
                
                # If pdf, need to do some extra work to get file link
                if r_type == '.pdf':
                    page = s.get(r_link, verify=False).content
                    page_tree = BeautifulSoup(page, 'html.parser')
                    
                    r_link = page_tree.findAll('object', {'type': 'application/pdf'})[0]['data']
                
                # Download file now  
                response = s.get(r_link, stream=True, verify=False)
                
                with open(r_title, "wb") as handle:
                    for data in tqdm(response.iter_content()):
                        handle.write(data)

# Create a persistent global session
s = requests.session()

# Load configurations
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

directory = cfg['directory']['local']
url = cfg['resources']['url']

values = {'username': cfg['login']['user'],
          'password': cfg['login']['password']}

powerpoint = cfg['resources']['powerpoint']
pdf = cfg['resources']['pdf']
word = cfg['resources']['word']

routine()