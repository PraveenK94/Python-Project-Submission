This Python script allows users to fetch movie recommendations based on genre, year, and rating from The Movie Database (TMDb) API.

## Features

- Search movies by genre
- Filter results by year (specific year or range)
- Filter results by minimum TMDb rating
- Save results to a CSV file
- Display fetched movie data

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- A TMDb API key

## Installation

1. Clone this repository:

git clone https://github.com/PraveenK94/Python-Project-Submission.git


2. Navigate to the project directory:

3. Create a `.env` file in the project root and add your TMDb API key:

API_KEY=your_tmdb_api_key_here


## Usage

Run the script:

python main.py


Follow the prompts to:
1. Enter a movie genre
2. Choose whether to apply filters
3. If yes to filters, enter a year or year range
4. If yes to filters, enter a minimum TMDb rating

The script will fetch movies based on your inputs and save them to a CSV file named after the genre you chose.