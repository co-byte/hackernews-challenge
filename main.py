import pyarrow as pa
from src import HackerNewsClient, DaoParquet
import schedule
import time

story_type = "newstories"
parquet_data_folder = 'data'
schema = pa.schema([
    ("id", pa.int64()),
    ("deleted", pa.bool_()),
    ("type", pa.string()),
    ("by", pa.string()),
    ("time", pa.timestamp('s')),  # Unix Time
    ("text", pa.string()),
    ("dead", pa.bool_()),
    ("parent", pa.int64()),
    ("poll", pa.int64()),
    ("kids", pa.list_(pa.int64())),
    ("url", pa.string()),
    ("score", pa.int64()),
    ("title", pa.string()),
    ("parts", pa.list_(pa.int64())),
    ("descendants", pa.int64())
])


def main():
    # Fetch new items
    print("Fetching new items...")
    new_items = client.fetch_items(500)

    # Save new items
    if new_items:
        dao_parquet.save_data(new_items)
        print(f"Saving {len(new_items)} new items")
    else:
        print("No new items to save")

if __name__ == '__main__':
    # Create a client to fetch new items
    client: HackerNewsClient = HackerNewsClient(f"{story_type}.json")

    # Create a DAO to save the fetched items
    dao_parquet = DaoParquet(parquet_data_folder,
                             parquet_base_filename=story_type, 
                             schema=schema)
    
    # Run main every day at 4:00 AM (as up to 500 requests can be fired almost at once and this should thus not happen at a busy time for the server)
    # schedule.every().day.at("04:00").do(main)
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute - this is not the most efficient way to do this, but it is simple and works for this use case