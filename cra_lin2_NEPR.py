import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_professors_info(program_url):
    response = requests.get(program_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    professors = []
    
    # Find all relevant parts of the structure provided
    for a_tag in soup.find_all('a', href=True):
        if 'mailto:' in a_tag['href']:
            try:
                # Extract professor's name
                prof_name = a_tag.find_previous('strong').text.strip()

                # Extract professor's email
                email = a_tag['href'].replace('mailto:', '')

                # Extract program name and research area
                parent_td = a_tag.find_parent('td')
                next_td = parent_td.find_next('td')
                
                # Extract program name
                program_name = ""
                research_area = ""
                for item in next_td.stripped_strings:
                    if program_name == "":
                        program_name = item
                    else:
                        research_area = item
                        break

                professors.append({
                    'name': prof_name,
                    'email': email,
                    'programs': program_name,
                    'research area': research_area
                })
            except Exception as e:
                print(f"Error processing a professor entry: {e}")

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
