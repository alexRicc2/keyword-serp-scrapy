import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

pageSpeed_df = pd.read_csv('PS_scores.csv')

# display(pageSpeed_df.head())
print(pageSpeed_df) #display the entire dataframe

page_df = pd.read_csv('page.csv')
mean_df = pageSpeed_df.drop('SERP Position', axis=1).mean(numeric_only=True)
compare_df = pd.concat([mean_df, page_df.iloc[0, 1:]], axis=1)
compare_df.columns = ['Mean', 'www.blog.ultatel']
print(compare_df)

# Plotting a bar chart for comparison
fig, ax = plt.subplots(figsize=(10, 5))
compare_df.plot(kind='bar', ax=ax)
ax.set_ylabel('Score')
ax.set_title('Comparison of Page Speed Scores')
plt.show()


# Fetching data for a specific URL
url = 'https://headless-wordpress-template.vercel.app/'
response = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key=AIzaSyCSI-4T7VL7iLl_qTBurAgFOYSpsMgjb6U&category=performance&category=seo')

if response.status_code == 200:
    # Parse the response as JSON data
    data = json.loads(response.text)
    # Get the result score
    score = data['lighthouseResult']['categories']['performance']['score']
    first_contentful_paint = data['lighthouseResult']['audits']['first-contentful-paint']['score']
    speed_index = data['lighthouseResult']['audits']['speed-index']['score']
    time_to_interactive = data['lighthouseResult']['audits']['interactive']['score']
    seo = data['lighthouseResult']['categories']['seo']['score']
    
    # Creating a new DataFrame with fetched data
    new_data = {'URL': url, 'Performance Score': score, 'First Contentful Paint': first_contentful_paint, 'Speed Index': speed_index, 'Time To Interactive': time_to_interactive, 'SEO Score': seo}
    new_df = pd.DataFrame([new_data])
    
    # Comparing with the mean of the existing DataFrame
    mean_df = pageSpeed_df.drop('SERP Position', axis=1).mean(numeric_only=True)
    compare_df = pd.concat([mean_df, new_df.iloc[0, 1:]], axis=1)
    compare_df.columns = ['Mean', 'searched website']
    print(compare_df)
    
    # Plotting a bar chart for comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    compare_df.plot(kind='bar', ax=ax)
    ax.set_ylabel('Score')
    ax.set_title('Comparison of Page Speed Scores')
    plt.show()
    
else:
    print("Error fetching data")

# Read in the data from the CSV file
data = pd.read_csv("PS_scores.csv")

# Group the data by SERP Position and calculate the mean performance score for each group
grouped_data = data.groupby("SERP Position").mean(numeric_only=True)["Performance Score"]

# Plot the mean performance scores for each SERP position
plt.bar(grouped_data.index, grouped_data.values)
plt.title("Mean Performance Scores for Each SERP Position")
plt.xlabel("SERP Position")
plt.ylabel("Mean Performance Score")
plt.show()


# Read in the data from the CSV files
pageSpeed_df = pd.read_csv('PS_scores.csv')
page_df = pd.read_csv('page.csv')

# Filter the pageSpeed_df to only include rows with SERP Position equal to 1
position_1_df = pageSpeed_df[pageSpeed_df['SERP Position'] == 1]

# Calculate the mean of the other columns for the filtered dataframe
mean_df = position_1_df.drop('SERP Position', axis=1).mean(numeric_only=True)

# Concatenate the mean_df with the performance data for the page_df
compare_df = pd.concat([mean_df, page_df.iloc[0, 1:]], axis=1)

# Rename the columns
compare_df.columns = ['Mean', 'www.blog.ultatel']

# Plotting a bar chart for comparison
fig, ax = plt.subplots(figsize=(10, 5))
compare_df.plot(kind='bar', ax=ax)
ax.set_ylabel('Score')
ax.set_title('Comparison of Page Speed Scores')
plt.show()