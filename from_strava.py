from datetime import datetime
from pathlib import Path
import pandas as pd
import requests  

from src.api_methods import get_methods
from src.api_methods import authorize
from src.data_preprocessing import main as data_prep


def main():
    """Main function to retrieve and save Strava activity data to a CSV file."""
    # Retrieve the access token
    token: str = authorize.get_acces_token()
    dfs_to_concat = []
    page_number = 1

    # 날짜 설정  
    after_date = int(datetime(2025, 4, 13).timestamp())  

    while True:
        # Access activity data from Strava API
        data: dict = get_methods.access_activity_data(token, params={
            'after': after_date,    
            'per_page': 200,        # 한 페이지당 활동 수
            'page': page_number,    # 페이지 번호 
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
    
    # DataFrame의 정보 출력  
    print("DataFrame 정보:")  
    print(df.info())  
    # DataFrame의 첫 몇 행 출력  
    print(df.head())  
    # DataFrame의 통계적 정보 출력  
    print("\nDataFrame의 통계적 요약:")  
    print(df.describe(include='all'))  

    # Generate a timestamp and save the dataframe to a CSV file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #df.to_csv(Path('data', f'my_activity_data={timestamp}.csv'), index=False)
    df.to_csv(Path('data', f'my_recent_activity.csv'), index=False)


if __name__ == '__main__':
    main()

