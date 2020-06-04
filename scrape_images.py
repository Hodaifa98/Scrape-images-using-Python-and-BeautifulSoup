# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:46:20 2020

@author: Hodaifa
"""

import os
from sys import exit, argv
import requests
from bs4 import BeautifulSoup
import cv2
from skimage import io

#Method to create directories
def create_dir(path):
    try:
        #Check if the directory exists, if not, then create it
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as e:
        print("Error - create_dir")

#Method to create files
def create_file(path):
    try:
        #Check if the file doesn't already exist
        if not os.path.exists(path):
            #Open the file and write "Alt, Name" to it
            f = open(path, "w")
            f.write("Alt,Name\n")
            f.close()
    except OSError as e:
        print("Error - create_file")

#Method to save images
def save_image(search_term, page_num=1):
    search_term_query = search_term.replace(" ", "%20")
    url = "https://www.freepik.com/search?dates=any&format=search&page="+str(page_num)+"&query="+str(search_term_query)+"&selection=1&sort=popular&type=photo"
    header = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36"}
    
    #Make GET request
    result = requests.get(url, headers=header)
    
    #Check the status code of the request's result
    if result.status_code == 200:
        #Using BeautifulSoup to parse the result
        soup = BeautifulSoup(result.content, "html.parser")
    else:
        print("Error - checking status code")
        exit()
        
    #Specifying the directory for the images
    dir_path = f"Downloads/{search_term}/"
    file_path = f"{dir_path}{search_term}.csv"
    
    #Creating the directory and file
    create_dir(dir_path)
    create_file(file_path)
    
    #Opening the CSV file
    f = open(file_path, "a")
        
    #Extract the images
    for tag in soup.find_all("a", class_="showcase__link"):
        #If the "a" tag has an img
        if tag.img:
            try:
                #Get the "data-src" and "alt" attributes from the image tag
                src = tag.img["data-src"]
                alt = tag.img["alt"]
            except Exception as e:
                alt = None
            try:
                #if the alt attribute exists
                if alt:
                    #Read the image from its source url
                    image = io.imread(src)
                    #Get the name of the image by splitting the url
                    name = src.split("/")[-1].split("?")[0]
                    #Prepare and write the name of the image file and its alt (description) to the CSV file
                    data = f"{alt},{name}\n"
                    f.write(data)
                    #Convert the image format from BGR to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    #Write the image inside the directory
                    cv2.imwrite(dir_path + name, image)
            except Exception as e:
                pass
    #Closing the CSV file
    f.close()
    
#Main
if __name__ == "__main__":
    #Check if command line arguments were provided
    try:
        if len(argv) > 1:
            #Check if a page_number argument was provided
            page = argv[2] if len(argv) > 2 else 1
            #Check if the page_number is a number
            if not page.isdigit():
                page = 1
            print(f"Currently scrapping images from page: {page}!")
            #Replace the "_" in the term into a space
            term = argv[1].replace("_", " ")
            #Start the scrapping
            save_image(term, page)
        else:
            print("Please provide a term to have images scraped! Usage: scrape_images.py term [page_number]")
    except Exception as e:
        print("Error reading arguments!")