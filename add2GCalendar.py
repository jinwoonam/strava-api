import os.path
from datetime import datetime, timedelta  
from pathlib import Path
import pandas as pd
import math

from src.api_methods import get_methods
from src.api_methods import authorize
from src.data_preprocessing import main as data_prep

import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pprint
from IPython.display import display

desired_columns = [
    #'resource_state',  # #2
    'name',            # 250408 한강
    'distance',        # 54622.9
    'moving_time',     # 7398
    'elapsed_time',    # 7677
    'total_elevation_gain',  # 124.0
    'type',            # Ride
    #'sport_type',      # Ride
    'id',              # 14114098358
    #'start_date',      # 2025-04-08T06:51:30Z
    'start_date_local', # 2025-04-08T15:51:30Z
    'timezone',        # (GMT+09:00) Asia/Seoul
    #'utc_offset',      # 32400.0
    'location_city',   # 
    'average_speed',   # 7.383
    'max_speed',       # 10.74
    'average_cadence', # 68.6
    'has_heartrate',   # True
    'average_heartrate', # 148.3
    'max_heartrate',   # 171.0
    'elev_high',       # 22.2
    'elev_low',        # 7.8
    'average_temp',    # 19.0
    'workout_type',    # 10.0
    'average_watts',   # 144.3
    'max_watts',       # 507.0
    'weighted_average_watts', # 156.0
    'device_watts',    # True
    'kilojoules'       # 1076.0
]
"""
def read_csv_line(csv_file):
    # 원하는 필드만 읽기


    # CSV 파일 읽기
    df = pd.read_csv(csv_file, usecols=desired_columns)
    #print(df)

    print()

    # print selected columns of first 5 rows in a nice format
    # (convert unit and round values)
    for index, row in df.head(5).iterrows():
        for col in df.columns:
            if "nan" in str(row[col]):
                continue;
            
            if "distance" in col:
                row[col] = str(round(row[col] / 1000, 2)) + " km"
            elif "_time" in col:
                row[col] = str(round(row[col] / 60, 2)) + " min"
            elif "_speed" in col:
                row[col] = str(round(row[col], 2)) + " km/h"
            elif "elev" in col:
                row[col] = str(round(row[col], 2)) + " m"
            elif "_watts" in col:
                row[col] = str(round(row[col], 2)) + " watts"

            output = ' '.join([f"{col}: {row[col]}" ])
            print(output)
        print("------\n\n")


    for index, row in df.head(5).iterrows():
        summary = row['name'].split(",")[0]
        summary += "\nhttps://www.strava.com/activities/" + str(row['id'])
        print(summary)
        print("\n")

        if row['location_city']:
            location = row['location_city'] 

        #""
        Ride Summary
        distance: 15.05 km
        time: 65.27 / 95.27 min  (moving / elasped)
        total_elevation_gain: 158.5 m ( 4.2 m ~ 80.4 m)
        average_speed: 3.84 km/h (max: 12.0 km/h)
        'average_temp',    # 19.0
        #""

        desc_summary = f"{row['type']} Summary\n"
        desc_summary += f"distance: {round(row['distance'] / 1000, 2)} km\n"
        desc_summary += "time: "
        if row['elapsed_time'] > 60 * 60:  # over 1Hr
            desc_summary += f"{round(row['moving_time'] / 3600, 2)} / {round(row['elapsed_time'] / 3600, 2)} hr"
        else:
            desc_summary += f"{round(row['moving_time'] / 60, 2)} / {round(row['elapsed_time'] / 60, 2)} min"
        desc_summary += f" ({round(row['moving_time'] / row['elapsed_time'] * 100, 1)}%) (moving / elapsed time)\n"
        desc_summary += f"elevation gain: {row['total_elevation_gain']} m ({row['elev_low']} ~ {row['elev_high']} m)\n"
        desc_summary += f"average speed: {row['average_speed']} km/h (max: {row['max_speed']} km/h)\n"
        if not math.isnan(row['average_temp']):
            desc_summary += f"average temp: {row['average_temp']} °C\n"
        desc_summary += "\n"

        #""
        Performance
        average_heartrate: 148.3 (max: 171.0)
        average power: 144.3 (max: 507.0)
        NP power: 156.0
        'average_cadence', # 68.6
        'kilojoules'       # 1076.0
        #""
        desc_performance = ""
        if row['has_heartrate'] and not math.isnan(row['average_heartrate']):
            desc_performance += f"average heartrate: {row['average_heartrate']} bpm (max: {row['max_heartrate']})\n"
        if not math.isnan(row['average_watts']):
            if math.isnan(row['weighted_average_watts']):
                desc_performance += f"average power: {row['average_watts']} watts (estimated)\n"
            else :
                desc_performance += f"average power: {row['average_watts']} watts (max: {row['max_watts']})\n"
                desc_performance += f"weighted average power: {row['weighted_average_watts']} watts\n"
            # row['device_watts']
        
        if desc_performance != "":
            desc_performance = f"Performance\n" + desc_performance + "\n\n"


        print(desc_summary)
        print(desc_performance)
        print("-----------------------\n") 
"""

def get_description(row):
    print(row['start_date'] + " " + row['timezone'] + "\n\n")

    desc_summary = row['type'] + ": "  + row['name'].split(",")[0]
    if row['location_city']:
        desc_summary += row['location_city'] 
    desc_summary += "\nhttps://www.strava.com/activities/" + str(row['id']) + "\n\n"

    """
    Ride Summary
    distance: 15.05 km
    time: 65.27 / 95.27 min  (moving / elasped)
    total_elevation_gain: 158.5 m ( 4.2 m ~ 80.4 m)
    average_speed: 3.84 km/h (max: 12.0 km/h)
    'average_temp',    # 19.0
    """
    desc_summary += f"{row['type']} Summary\n"
    desc_summary += f"distance: {round(float(row['distance']) / 1000, 2)} km\n"
    desc_summary += "time: "
    
    elapsed_time = int(row['elapsed_time'])
    moving_time = int(row['moving_time'])
    
    if elapsed_time > 60 * 60:  # over 1Hr
        desc_summary += f"{round(moving_time / 3600, 2)} / {round(elapsed_time / 3600, 2)} hr"
    else:
        desc_summary += f"{round(moving_time / 60, 2)} / {round(elapsed_time / 60, 2)} min"
    desc_summary += f" ({round(moving_time / elapsed_time * 100, 1)}%) (moving / elapsed time)\n"
    desc_summary += f"elevation gain: {row['total_elevation_gain']} m ({row['elev_low']} ~ {row['elev_high']} m)\n"
    desc_summary += f"average speed: {round(float(row['average_speed']) * 3.6, 1)} km/h (max: {round(float(row['max_speed']) * 3.6, 1)} km/h)\n" # {float(row['average_speed']) * 3.6 } km/h (max: {float(row['max_speed']) * 3.6} km/h)\n"
    if row['average_temp'] != "":
        desc_summary += f"average temp: {row['average_temp']} °C\n"
    desc_summary += "\n"
    print(desc_summary)

    """
    Performance
    average_heartrate: 148.3 (max: 171.0)
    average power: 144.3 (max: 507.0)
    NP power: 156.0
    'average_cadence', # 68.6
    'kilojoules'       # 1076.0
    """
    desc_performance = ""
    if row['has_heartrate'] and row['average_heartrate'] != "":
        desc_performance += f"average heartrate: {row['average_heartrate']} bpm (max: {row['max_heartrate']})\n"
    if row['average_watts'] and row['average_watts'].strip():
        if row['weighted_average_watts'].strip() != "":
            desc_performance += f"average power: {row['average_watts']} watts (max: {row['max_watts']})\n"
            desc_performance += f"weighted average power: {row['weighted_average_watts']} watts\n"
        else :
            desc_performance += f"average power: {row['average_watts']} watts (estimated)\n"
        # row['device_watts']
    
    if desc_performance != "":
        desc_performance = f"Performance\n" + desc_performance + "\n"

    print(desc_performance)
    print("-----------------------\n")
    return (desc_summary + desc_performance)

def get_end_date(start_date, elapsed_time):
    # 예시 데이터  
    #start_date = "2021-09-15T07:00:00Z"  
    #elapsed_time = 3600  # 1시간  
    
    # 문자열로부터 datetime 객체 생성  
    start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")  
    
    # 경과 시간을 datetime.timedelta 객체로 변환  
    elapsed_time_delta = timedelta(seconds=elapsed_time)  
    
    # 종료 시간 계산  
    end_datetime = start_datetime + elapsed_time_delta  
    
    # 종료 시간을 start_date 같은 형식으로 변환  
    end_date_time_str = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")  
    
    #print("시작 시간:", start_date)  
    #print("경과 시간:", elapsed_time)  
    #print("종료 시간:", end_date_time_str)  

    return end_date_time_str

def add_events_from_csv(service, csv_file):
    # Read events from CSV file
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        #reader = pd.read_csv(csv_file)
        #df = pd.read_csv(csv_file, usecols=desired_columns)
        for row in reader:
            description = get_description(row)
            event = {
                'summary': row['type'] + ": "  + row['name'].split(",")[0],
                'description': description,
                'start': {
                    #'dateTime': row['start_date'] + 'T' + row['start_time'] + ':00',
                    #'timeZone': 'Asia/Seoul'
                    'dateTime': row['start_date'],      # 2025-04-08T06:51:30Z
                    'timeZone': row['timezone'],        # (GMT+09:00) Asia/Seoul

                },
                'end': {
                    #'dateTime': row['end_date'] + 'T' + row['end_time'] + ':00',
                    #'timeZone': 'Asia/Seoul'
                    'dateTime': get_end_date(row['start_date'], int(row['elapsed_time'])),        # 2025-04-08T06:51:30Z
                    'timeZone': row['timezone'],        # (GMT+09:00) Asia/Seoul
                }
            }

            #print(event)

            
            # Add event to Google Calendar
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            

def get_google_service():
     # If modifying these scopes, delete the file token.pickle.
  SCOPES = ['https://www.googleapis.com/auth/calendar']

  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the function
    # CSV 파일 경로
    #csv_file = Path('data', f'my_recent_activity.csv')

    #add_events_from_csv(service, csv_file)
    return service

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None


def main():
    # CSV 파일 경로
    csv_file = Path('data', f'my_recent_activity.csv')
    service = get_google_service()
    add_events_from_csv(service, csv_file)


if __name__ == "__main__":
    main()

  

"""
csv 파일의 구조 참고용
#resource_state,name,distance,moving_time,elapsed_time,total_elevation_gain,type,sport_type,id,start_date,start_date_local,timezone,utc_offset,location_city,location_state,location_country,achievement_count,kudos_count,comment_count,athlete_count,photo_count,trainer,commute,manual,private,visibility,flagged,gear_id,start_latlng,end_latlng,average_speed,max_speed,average_cadence,has_heartrate,average_heartrate,max_heartrate,heartrate_opt_out,display_hide_heartrate_option,elev_high,elev_low,upload_id,upload_id_str,external_id,from_accepted_tag,pr_count,total_photo_count,has_kudoed,athlete.id,athlete.resource_state,map.id,map.summary_polyline,map.resource_state,average_temp,workout_type,average_watts,max_watts,weighted_average_watts,device_watts,kilojoules
#2,Morning Walk,2695.0,1919,2070,10.8,Walk,Walk,14170065801,2025-04-13T21:44:36Z,2025-04-14T06:44:36Z,(GMT+09:00) Asia/Seoul,32400.0,,,,0,0,0,1,0,False,False,False,True,only_me,False,g11383797,"[37.564952, 126.843265]","[37.564145, 126.830895]",1.404,4.1,58.1,True,96.9,111.0,False,True,21.9,6.6,15123762808.0,15123762808,garmin_ping_428823074846,False,0,0,False,140429,1,a14170065801,{ahdFa~deW[zAATWr@E^?TMl@a@hAJVFd@Gb@KRANKh@@XEtAJj@C`@I\D`@IVYLITCTGBSd@_@\S^GRONOb@CC?^MZKfAI^KNOXSVE?APMb@CRORERKNUPQ\i@ZWDUOi@u@q@Sa@?KCc@SBCVTAJSDWNk@b@SXa@XQ\KhAFXVnCg@Q}@MYQSGQVM`@MN]Ku@Ci@VSA]h@M^MxBAfBn@d@b@VjBNfADx@c@b@?DDD\FNRLb@Lz@@`@H\@RBf@@TDJ?hAN\Fr@\PGb@w@XY`@[DADB^h@RI|@QTKHSDe@FOHIfB]VCp@A\H,2,,,,,,,
#2,250408 한강,54622.9,7398,7677,124.0,Ride,Ride,14114098358,2025-04-08T06:51:30Z,2025-04-08T15:51:30Z,(GMT+09:00) Asia/Seoul,32400.0,,,,59,15,0,1,0,False,False,False,False,everyone,False,b5624262,"[37.56495, 126.843011]","[37.564907, 126.843134]",7.383,10.74,68.6,True,148.3,171.0,False,True,22.2,7.8,15065274383.0,15065274383,garmin_ping_427055283840,False,16,0,False,140429,1,a14114098358,mchdFo~deW{@~GY|@a@Bc_@mE_DqBiEkEnGwLfSob@?]]\m@Sq@hAhAeCkAwADMfu@i|A`EmHlGwIbI{JfGgJbGsGpBiLbB}FzCkH|DoNpBoEnU{`@dEyD|@oBn@iD~BmE`@[tAM`B_DrEqHrCu@pAiArMaW|BkFt@qD|Pg[pFcI`DsDdA}CzCCvKuCxB@pDe@~MyCnXaPjPkLrDaFpC}GjKi`@dAaGv@oIh@yLIaM_BaRmAsJsAuI_AcDgAkKy@yCAuAXoAiAeNPoG^iCxAqFtFuMbCeM~@_At@@zGc[jCwDfDiM`DeGxFuMdBiBdCoKnDwMvC_Ih@qEr@aBGeBjCcMO_GDmARy@xAyB]wDEaDp@qEm@aCN{Ie@yIq@gDiBmSi@mCwBaIeAuBcC}A}AeBY{ADiDe@cBaA{@uBs@cAsA_@oBFeDMoAqAaCk@aDeCqE_B{GiAsAyBcAiAgAkCgG_CiCyByDmGgCqAgBu@_DsAImD_E_B_@e`@}d@wVu[uAeDeCcBuVm[wAaCaBmFa@aDSwF\yFbAsGnBoJn@mFnEoTjEiZ|EiUbGsa@fBgIjCoF`KeLxBgDzKwXvBgElAuAtBuAlB}C`IgFlFwBFYs@v@{C`AiJ`GuBdD{D|CyAlCoL`ZmCbEcKdLmCtF}@zDaHbe@eFhVsEzZqCtOu@~Bi@rEgDxQe@fJLvDr@rEbBdFvA~BjVvZlClB|@hChVn[x`@he@lBl@fDtDrAf@r@hCrAjBjAr@vBb@xAbArBtD~BlC`CvF~FfEn@`Bp@tDrClFf@zCrAfCHdAKrC^`CbAtAvDnBf@`BCfDXbBlAzAlCdBhAnB`CtIz@zHa@|MFxBODPq@\oPXjCK[x@fIp@lDh@fJQzIp@xDq@`DElBd@nFoBhDJnIsBhLIvBgAlCW`DuCrH}CpPqC~Hc@v@uAd@g@p@{A~EiHvPsCtK_FhFIbA{@lCDb@mClNC|@_BhCcC|KiG~NgAhE_@pCQpG`AlLSpDdAnFx@xHbAlDfAtGbChSr@xJLzMu@fNu@zHsAxG}Jf_@kBtE_E~FsStNsRnL{B|@mKbCaFr@gDDyGjBiGf@cAhDsC`DqFfIyPf[e@jAObBeAbCmOdZqApAuCt@uEtHyAtC{Bn@gC|Em@jDu@xAmC`CeB~BmSt]_CdFyCnKsEjLwAtFsBdLgHzHaC~D_TzXsDhGo}AhaDcE`KiBtGpChAJd@bAl@lCdEhGw@hAy@nH?lFgCrBR~AfAdGbH~@dBpEyJVgBfA_B~@eCf@iIj@iCTmGTk@,2,19.0,10.0,144.3,507.0,156.0,True,1076.0


# 컬럼 정의
columns = [
    'resource_state',  # #2
    'name',            # 250408 한강
    'distance',        # 54622.9
    'moving_time',     # 7398
    'elapsed_time',    # 7677
    'total_elevation_gain',  # 124.0
    'type',            # Ride
    'sport_type',      # Ride
    'id',              # 14114098358
    'start_date',      # 2025-04-08T06:51:30Z
    'start_date_local', # 2025-04-08T15:51:30Z
    'timezone',        # (GMT+09:00) Asia/Seoul
    'utc_offset',      # 32400.0
    'location_city',   # 
    'location_state',  # 
    'location_country', # 
    'achievement_count', # 59
    'kudos_count',     # 15
    'comment_count',   # 0
    'athlete_count',   # 1
    'photo_count',     # 0
    'trainer',         # False
    'commute',         # False
    'manual',          # False
    'private',         # False
    'visibility',      # everyone
    'flagged',         # False
    'gear_id',        # b5624262
    'start_latlng',    # "[37.56495, 126.843011]"
    'end_latlng',      # "[37.564907, 126.843134]"
    'average_speed',   # 7.383
    'max_speed',       # 10.74
    'average_cadence', # 68.6
    'has_heartrate',   # True
    'average_heartrate', # 148.3
    'max_heartrate',   # 171.0
    'heartrate_opt_out', # False
    'display_hide_heartrate_option', # True
    'elev_high',       # 22.2
    'elev_low',        # 7.8
    'upload_id',       # 15065274383.0
    'upload_id_str',   # 15065274383
    'external_id',     # garmin_ping_427055283840
    'from_accepted_tag', # False
    'pr_count',        # 16
    'total_photo_count', # 0
    'has_kudoed',      # False
    'athlete.id',      # 140429
    'athlete.resource_state', # 1
    'map.id',          # a14114098358
    'map.summary_polyline', # mchdFo~deW{@~GY|@a@Bc_@mE_DqBiEkEnGwLfSob@?]]\m@Sq@hAhAeCkAwADMfu@i|A`EmHlGwIbI{JfGgJbGsGpBiLbB}FzCkH|DoNpBoEnU{`@dEyD|@oBn@iD~BmE`@[tAM`B_DrEqHrCu@pAiArMaW|BkFt@qD|Pg[pFcI`DsDdA}CzCCvKuCxB@pDe@~MyCnXaPjPkLrDaFpC}GjKi`@dAaGv@oIh@yLIaM_BaRmAsJsAuI_AcDgAkKy@yCAuAXoAiAeNPoG^iCxAqFtFuMbCeM~@_At@@zGc[jCwDfDiM`DeGxFuMdBiBdCoKnDwMvC_Ih@qEr@aBGeBjCcMO_GDmARy@xAyB]wDEaDp@qEm@aCN{Ie@yIq@gDiBmSi@mCwBaIeAuBcC}A}AeBY{ADiDe@cBaA{@uBs@cAsA_@oBFeDMoAqAaCk@aDeCqE_B{GiAsAyBcAiAgAkCgG_CiCyByDmGgCqAgBu@_DsAImD_E_B_@e`@}d@wVu[uAeDeCcBuVm[wAaCaBmFa@aDSwF\yFbAsGnBoJn@mFnEoTjEiZ|EiUbGsa@fBgIjCoF`KeLxBgDzKwXvBgElAuAtBuAlB}C`IgFlFwBFYs@v@{C`AiJ`GuBdD{D|CyAlCoL`ZmCbEcKdLmCtF}@zDaHbe@eFhVsEzZqCtOu@~Bi@rEgDxQe@fJLvDr@rEbBdFvA~BjVvZlClB|@hChVn[x`@he@lBl@fDtDrAf@r@hCrAjBjAr@vBb@xAbArBtD~BlC`CvF~FfEn@`Bp@tDrClFf@zCrAfCHdAKrC^`CbAtAvDnBf@`BCfDXbBlAzAlCdBhAnB`CtIz@zHa@|MFxBODPq@\oPXjCK[x@fIp@lDh@fJQzIp@xDq@`DElBd@nFoBhDJnIsBhLIvBgAlCW`DuCrH}CpPqC~Hc@v@uAd@g@p@{A~EiHvPsCtK_FhFIbA{@lCDb@mClNC|@_BhCcC|KiG~NgAhE_@pCQpG`AlLSpDdAnFx@xHbAlDfAtGbChSr@xJLzMu@fNu@zHsAxG}Jf_@kBtE_E~FsStNsRnL{B|@mKbCaFr@gDDyGjBiGf@cAhDsC`DqFfIyPf[e@jAObBeAbCmOdZqApAuCt@uEtHyAtC{Bn@gC|Em@jDu@xAmC`CeB~BmSt]_CdFyCnKsEjLwAtFsBdLgHzHaC~D_TzXsDhGo}AhaDcE`KiBtGpChAJd@bAl@lCdEhGw@hAy@nH?lFgCrBR~AfAdGbH~@dBpEyJVgBfA_B~@eCf@iIj@iCTmGTk@
    'average_temp',    # 19.0
    'workout_type',    # 10.0
    'average_watts',   # 144.3
    'max_watts',       # 507.0
    'weighted_average_watts', # 156.0
    'device_watts',    # True
    'kilojoules'       # 1076.0
]
"""