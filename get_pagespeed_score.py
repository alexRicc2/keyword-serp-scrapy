import requests
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from dotenv import dotenv_values
# Set your PageSpeed API key here
values = dotenv_values()

API_KEY = values['PAGESPEED_API_KEY']

# Set the input file name here
input_file = 'SERP_links.csv'

# Set the output file name here
output_file = 'PS_scores.csv'

# Define a function to get the PageSpeed score for a given URL
def get_pagespeed_score(keyword, url, position):
    # Construct the URL for the API request
    api_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}&category=performance&category=seo'

    # Send the API request and receive the response
    response = requests.get(api_url)

    # Check the status code of the response
    if response.status_code == 200:
        # Parse the response as JSON data
        data = json.loads(response.text)
        # Get the result score
        score = data['lighthouseResult']['categories']['performance']['score']
        first_contentful_paint = data['lighthouseResult']['audits']['first-contentful-paint']['score']
        speed_index  = data['lighthouseResult']['audits']['speed-index']['score']
        time_to_interactive = data['lighthouseResult']['audits']['interactive']['score']
        seo = data['lighthouseResult']['categories']['seo']['score']
        
        print(f"Keyword: {keyword}, SERP Position: {position}, PageSpeed score for {url}: {score}")
        return [keyword, position, url, score, first_contentful_paint, speed_index, time_to_interactive, seo]
    else:
        print(f"API request for {url} failed with status code {response.status_code}")
        return None

# Read the input file and create a list of keyword, URL, and position tuples
keyword_urls = []
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        keyword, url, position = row
        keyword_urls.append((keyword, url, position))

start_time = time.time()

# Make parallel requests to the PageSpeed API using ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    # Submit the requests to the executor
    futures = [executor.submit(get_pagespeed_score, keyword, url, position) for keyword, url, position in keyword_urls]

    # Collect the results as they become available
    results = []
    for future in as_completed(futures):
        result = future.result()
        if result is not None:
            results.append(result)

# Save the results to the output file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Keyword','SERP Position', 'Link', 'Performance Score', 'First Contentful Paint', 'Speed Index', 'Time To Interactive', 'SEO Score'])
    for result in results:
        writer.writerow(result)

duration = time.time() - start_time
print('Results saved in', output_file)
print(f'Execution time: {duration:.2f} seconds')
