import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_professors_info(program_url):
    response = requests.get(program_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    professors = []
    
    # Find all <a> tags that contain the structure provided in the example
    for a_tag in soup.find_all('a', href=True):
        if 'mailto:' in a_tag['href']:
            # Extract professor's name
            prof_name = a_tag.find_previous('strong').text.strip()
            
            # Extract professor's email
            email = a_tag['href'].replace('mailto:', '')
            
            professors.append({'PROF_NAME': prof_name, 'EMAIL_ADDRESS': email})
    
    return professors

def save_to_excel(data, filename='output.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    while True:
        program_url = input('Enter the URL of the university program: ')
        output_file = input('Enter the output Excel file name (e.g., output.xlsx): ')
        
        professors = extract_professors_info(program_url)
        save_to_excel(professors, filename=output_file)
        
        another_request = input('Do you have any other requests? (y/n): ')
        if another_request.lower() != 'y':
            break

if __name__ == '__main__':
    main()
