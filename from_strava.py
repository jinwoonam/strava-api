from datetime import datetime
from pathlib import Path
import pandas as pd

from src.api_methods import get_methods
from src.api_methods import authorize
from src.data_preprocessing import main as data_prep


def main():
    """Main function to retrieve and save Strava activity data to a CSV file."""
    # Retrieve the access token
    token: str = authorize.get_acces_token()
    dfs_to_concat = []
    page_number = 1

    while True:
        # Access activity data from Strava API
        data: dict = get_methods.access_activity_data(token, params={
            'per_page': 200,
            'page': page_number,
        })
        page_number += 1
        
        # Preprocess the retrieved data
        cur_df = data_prep.preprocess_data(data)
        dfs_to_concat.append(cur_df)
        
        # Break the loop if no more data is returned
        if len(data) == 0:
            break
    
    # Concatenate all dataframes into a single dataframe
    df = pd.concat(dfs_to_concat, ignore_index=True)
    
    # Generate a timestamp and save the dataframe to a CSV file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    df.to_csv(Path('data', f'my_activity_data={timestamp}.csv'), index=False)


if __name__ == '__main__':
    main()

