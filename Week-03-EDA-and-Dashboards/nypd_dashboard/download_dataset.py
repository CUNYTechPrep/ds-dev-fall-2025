# Import libraries.
import time

from requests import get
from tqdm import tqdm

# Define the file name.
file_name = "nypd_arrests_dataset.csv"
# Define the API endpoint's limit string query parameter. How many rows/samples to download from the API.
limit = 5986025
# Define the API endpoint.
url = f"https://data.cityofnewyork.us/resource/8h9b-rp9u.csv?$limit={limit}"

# Start timer and create progress bar.
start_time = time.time()
print("Starting download process...")

# Make a GET request with progress tracking.
with tqdm(total=100, desc="Downloading data from API") as pbar:
    # Download data.
    pbar.set_description("Downloading data from API")
    response = get(url)
    pbar.update(50)
    
    # Save the content to a CSV file.
    pbar.set_description("Writing data to file")
    with open(f"{file_name}", "wb") as f:
        f.write(response.content)
    pbar.update(50)

# Calculate and display total time.
end_time = time.time()
total_time = end_time - start_time
print(f"Data saved to: {file_name}")
print(f"Total time to download and save data from API: {total_time:.2f} seconds")