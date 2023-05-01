import requests
import csv
from dotenv import dotenv_values

values = dotenv_values()


input_file = 'keywords.csv'
output_file = 'SERP_links.csv'
results=[]

def getResult(q):
    params = {
        'api_key': values['SCALE_API_KEY'],
        'q': q,
        'page': '1',
        'max_page': '1',
        'num': '10',
        'output': 'json',
    }

    # make the http GET request to Scale SERP
    api_result = requests.get('https://api.scaleserp.com/search', params)
    api_result.raise_for_status()  # raise an exception for 4xx or 5xx errors
    response_json = api_result.json()
    links = [{'link': result['link'],  'pos': result['position']} for result in response_json['organic_results']]
    return links

with open(input_file, mode='r') as file, open(output_file, mode='w', newline='') as output:
    reader = csv.reader(file)
    writer = csv.writer(output)
    writer.writerow(['keyword', 'link', 'position'])  # write header row
    for row in reader:
        keyword = row[0]
        keyword = keyword.replace(" ", "+")
        print(f'keyword: {keyword}')
        links = getResult(keyword)
        for link in links:
            keyword = keyword.replace('+', ' ')
            writer.writerow([keyword, link['link'], link['pos']])
