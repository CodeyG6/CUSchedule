import requests
import json
import math
import csv
import os
from bs4 import BeautifulSoup

from .professor import Professor
# This code has been tested using Python 3.6 interpreter and Linux (Ubuntu).
# It should run under Windows, if anything you may need to make some adjustments for the file paths of the CSV files.


class ProfessorNotFound(Exception):
    def __init__(self, search_argument, search_parameter: str = "Name"):

        # What the client is looking for. Ex: "Professor Pattis"
        self.search_argument = search_argument

        # The search criteria. Ex: Last Name
        self.search_parameter = search_parameter

    def __str__(self):

        return (
            f"Professor not found"
            + f" The search argument {self.search_argument} did not"
            + f" match with any professor's {self.search_parameter}"
        )


class RateMyProfApi:
    professor_id_list = {}

    def __init__(self, school_id, prof_name, use_name: bool):
        #on initialization, call scrape_professor_by_name. 
        self.professor = self.scrape_professor_by_name(school_id, prof_name)
        self.indexnumber = False

    def scrape_professor_by_name(self, school_id, prof_name):
        prof_id = RateMyProfApi.get_professor_id_from_name(prof_name)
        page = requests.get("https://www.ratemyprofessors.com/professor/" + str(prof_id))

        return RateMyProfApi.scrape_professor(page)
    
    # Modified version of the scraper to get information on one professor based on professor id
    def scrape_professor(page): 
        professor = dict()
        
        prof = []
        scraper = BeautifulSoup(page.text, 'html.parser')
        
        #get the professor's name
        find_name = scraper.find("h1", class_="NameTitle__NameWrapper-dowf0z-2 cSXRap")
        if find_name:
            name = find_name.get_text()
        else:
            print("Error: Name not found")
            name = "Name not found!" #Bug check when name not found

        #get the professor's overall rating
        find_overall_rating = scraper.find("div", class_="RatingValue__Numerator-qw8sqy-2 liyUjw")
        overall_rating = find_overall_rating.string if find_overall_rating else "Rating not found!"

        #get number of ratings
        find_num_ratings = scraper.find("div", class_="RatingValue__NumRatings-qw8sqy-0 erHIUr")
        num_ratings = find_num_ratings.get_text() if find_num_ratings else "No ratings"
        num_ratings = num_ratings[25:28]

        #get percentage that would take professor again and level of difficulty
        find_perc_and_diff = scraper.find_all("div", class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs")
        percentage = find_perc_and_diff[0].string if find_perc_and_diff else "No feedback"
        difficulty = find_perc_and_diff[1].string if len(find_perc_and_diff) > 1 else "No difficulty"
        
        prof.append([name, overall_rating, num_ratings, str(percentage), str(difficulty)])
        #prof.append(['Matthew Re', '4.3', '17', '77', '2.9'])

        return prof
    
    def get_professor_id_from_name(professor_name):
        if len(RateMyProfApi.professor_id_list) == 0:
            #Try-except for CSV file reading
            try:
                with open('rateMyProf/utils/Instructors ID List.csv', 'r', encoding='iso-8859-1') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        RateMyProfApi.professor_id_list[row['Instructor']] = row['ID']
            except FileNotFoundError:
                print("Error csv not found, check file path first")
                return -1
            if professor_name in RateMyProfApi.professor_id_list:
                return RateMyProfApi.professor_id_list[professor_name]
        
            return -1
    
