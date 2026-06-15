import pandas as pd

df = pd.read_csv("netflix_titles.csv", encoding="latin1")

print(df.head())

#unwanted coloums remove
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print(df.head())
print(df.shape)

#understand the data
print(df.shape)      # rows & columns
print(df.columns)    # column names
print(df.info())     # data types

#data cleaning 
# Missing values fill
df.fillna("Unknown", inplace=True)

# date_added ko datetime me convert
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Year column create
df['year_added'] = df['date_added'].dt.year

#movies vs tv shows
import matplotlib.pyplot as plt
import seaborn as sns

sns.countplot(x='type', data=df)
plt.title("Movies vs TV Shows")
plt.show()

#hypotheses 1:
#movies are more than TV shows
movies = df[df['type'] == 'Movie'].shape[0]
tv = df[df['type'] == 'TV Show'].shape[0]

print("Movies:", movies)
print("TV Shows:", tv)

#conclusion
if movies > tv:
    print("Hypothesis True: Movies are more than TV Shows")
else:
    print("Hypothesis False")

#content added per year
year_data = df['year_added'].value_counts().sort_index()

year_data.plot(kind='line')
plt.title("Content Added Over Years")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

#hypotheses 2:
#content increase in recent year
df['year_added'] = pd.to_datetime(df['date_added']).dt.year

year_counts = df['year_added'].value_counts().sort_index()

print(year_counts)

#top countries
country_data = df['country'].value_counts().head(10)

country_data.plot(kind='bar')
plt.title("Top 10 Countries")
plt.xticks(rotation=45)
plt.show()

#Rating distribution
sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index)
plt.title("Ratings Distribution")
plt.show()

#hypotheses 3:
#TV-MA is a common rating
top_rating = df['rating'].value_counts().idxmax()
print("Most common rating:", top_rating)

#top geners
genre_data = df['listed_in'].str.split(',', expand=True).stack()

top_genres = genre_data.value_counts().head(10)

top_genres.plot(kind='bar')
plt.title("Top Genres")
plt.xticks(rotation=45)
plt.show()

#movie duration
movies = df[df['type'] == 'Movie'].copy()

movies['duration'] = movies['duration'].str.replace(' min', '')
movies['duration'] = pd.to_numeric(movies['duration'], errors='coerce')

sns.histplot(movies['duration'], bins=20)
plt.title("Movie Duration Distribution")
plt.show()

#hypotheses 4:
#Duration of Movies is more than Tv shows
avg_duration = movies['duration'].mean()

print("Average movie duration:", avg_duration)
