import requests
import pandas as pd
import re
from dotenv import load_dotenv
import os 


def get_tmdb_genre_id(genre_name, api_key):

    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        'api_key': api_key,
        'language': 'en-US'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        genres = response.json().get('genres', [])
        for genre in genres:
            if genre['name'].lower() == genre_name.lower():
                return genre['id']
        print(f"Genre '{genre_name}' not found.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching genres: {e}")
        return None

def fetch_movies_by_genre(genre_id, api_key, genre_name, year_filter=None, rating_filter=None):

    movies = []
    url = "https://api.themoviedb.org/3/discover/movie"
    page = 1
    while True:
        params = {
            'api_key': api_key,
            'with_genres': genre_id,
            'page': page,
            'vote_average.gte': rating_filter if rating_filter else 0,
            'primary_release_year': year_filter if isinstance(year_filter, int) else None,
            'primary_release_date.gte': f"{year_filter[0]}-01-01" if isinstance(year_filter, tuple) else None,
            'primary_release_date.lte': f"{year_filter[1]}-12-31" if isinstance(year_filter, tuple) else None,
            'sort_by': 'popularity.desc'
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching movies: {e}")
            break
        data = response.json()
        results = data.get('results', [])
        if not results:
            break
        for movie in results:
            movies.append({
                'Title': movie.get('title', 'N/A'),
                'Year': movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A',
                'Genre': genre_name,
                'TMDb Rating': movie.get('vote_average', 'N/A')
            })
        if page >= data.get('total_pages', 1):
            break
        page += 1
    return movies

def save_movies_to_csv(movies, genre):

    if not movies:
        print("No movies to save.")
        return
    df = pd.DataFrame(movies)
    sanitized_genre = re.sub(r'[\\/*?:"<>|]', "", genre)
    filename = f"{sanitized_genre}_movies.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved {len(movies)} movies to '{filename}'.")

def main():
    load_dotenv()
    
    tmdb_api_key = os.getenv('API_KEY')
    if not tmdb_api_key:
        print("API key is required to proceed.")
        return

    genre_name = input("Enter a movie genre for search (ex: Action, Comedy): ").strip()
    if not genre_name:
        print("Genre input is required to proceed.")
        return

    genre_id = get_tmdb_genre_id(genre_name, tmdb_api_key)
    if not genre_id:
        print("Cannot proceed without a valid genre ID.")
        return

    apply_filters = input("Do you want to apply filters? (yes/no): ").lower().strip()
    year_filter = None
    rating_filter = None
    if apply_filters == 'yes':
        year_input = input("Filter by year? Enter a specific year or a range (ex:2000-2010), or press Enter to skip: ").strip()
        if year_input:
            if '-' in year_input or '-' in year_input:  
                parts = re.split(r'[--]', year_input)
                if len(parts) == 2:
                    try:
                        start_year = int(parts[0].strip())
                        end_year = int(parts[1].strip())
                        year_filter = (start_year, end_year)
                    except ValueError:
                        print("Invalid year range format. Skipping year filter.")
                else:
                    print("Invalid year range format. Skipping year filter.")
            else:
                try:
                    year_filter = int(year_input)
                except ValueError:
                    print("Invalid year format. Skipping year filter.")

        rating_input = input("Filter by minimum TMDb rating (ex: 7.5), or press Enter to skip: ").strip()
        if rating_input:
            try:
                rating_filter = float(rating_input)
                if not (0 <= rating_filter <= 10):
                    print("TMDb rating must be between 0 and 10. Skipping rating filter.")
                    rating_filter = None
            except ValueError:
                print("Invalid rating format. Skipping rating filter.")

    print(f"\nFetching movies in the genre '{genre_name}'...")
    movies = fetch_movies_by_genre(genre_id, tmdb_api_key, genre_name, year_filter, rating_filter)
    if not movies:
        print("No movies found for the specified genre and filters.")
        return

    save_movies_to_csv(movies, genre_name)
    print("\nMovies fetched successfully.")
    
    try:
        sanitized_genre = re.sub(r'[\\/*?:"<>|]', "", genre_name)
        filename = sanitized_genre + "_movies.csv"
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            print("\nHere are some movies we found:")
            print(df.head())  # Print only the first few rows
        else:
            print(f"\nError: The file '{filename}' does not exist.")
    except pd.errors.EmptyDataError:
        print("No data available to display.")
    except Exception as e:
        print(f"An error occurred while trying to read the CSV file: {e}")

if __name__ == "__main__":
    main()
