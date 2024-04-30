# Hacker News Data Fetcher

This Python script was completed as part of a challenge I completed this year. It fetches new items from the [Hacker News API](https://github.com/HackerNews/API) on a daily basis and saves them into Parquet files, enabling further analysis in the future.

## Challenge Details

- **Task**:
  - Write a python script that extracts information from the [Hacker News API](https://github.com/HackerNews/API) and saves the data as parquet files on your local machine.

- **Bonus challenges**:
  - Don’t use pandas.
  - Clean the data.
  - Avoid fetching the same item twice.
  - Make sure your parquet files don't become too big (limit their size).

- **Duration**: 60-90 minutes

## Code Overview

### `main.py`

This script contains the main logic for fetching and saving Hacker News items. It uses the `HackerNewsClient` class to fetch items and the `DaoParquet` class to save them into Parquet files.

As the API does not allow multiple objects to be fetched in a single request, I chose to make all necessary calls every night at 4 a.m. (when activity is generally lower than during the day). To implement this, I made use of the `time` and `schedule` libraries.

### `client.py`

- `HackerNewsClient`: This class interacts with the Hacker News API to fetch items. It retrieves a set of 500 new IDs, filters out those that have already been saved, and proceeds to execute requests for the remaining IDs, fetching their actual items.

### `dao_parquet.py`

- This (Data Acess Object) class handles the saving of fetched items into Parquet files. It offers a single "public" method, which in turn makes use of multiple "private" methods to handle the actual operations.

- To manage the size of the Parquet files, I chose to create a new file every time new data is saved. Initially, I implemented this by maintaining a simple counter, with the current count appended to the filename of the new file. However, considering the script's daily execution, simply appending the current date to the filename would have been a better approach.

## Requirements

- Python 3.x
- `pyarrow` library
- `schedule` library
- `requests` library

You can install the required libraries using `pip install -r requirements.txt`.

## Usage

Simply run `main.py` to start the script.
