import gspread  
from Helpers import check_birthdays 
from datetime import datetime as dt  
from Helpers import check_birthdays_sheets, ticktock


today = dt.now()
today_day_month = today.strftime('%d-%m') 
today_day_month_year = today.strftime('%d/%m/%Y') 
current_day = today.timetuple().tm_yday 
'''
gc = gspread.oauth(
    credentials_filename='path/to/the/credentials.json',
    authorized_user_filename='path/to/the/authorized_user.json'
) 
'''
 

credentials = {
    "installed": {
        "client_id": "140651080242-c5a0dqq6hbiqc3mdakcs5qv72smlih43.apps.googleusercontent.com",
        "project_id": "gsheets-419306",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost"]
    }
}

authorized_user = {
    "refresh_token": "1//0g8cfPbu5t6NwCgYIARAAGBASNwF-L9IruOofPEfDUx5Dm5SapjcAkh4yV4qyKEW0qzKQ3u0N7D1gaunC6YB0DWkEGDMQ4HryuoM",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "140651080242-c5a0dqq6hbiqc3mdakcs5qv72smlih43.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
    "universe_domain": "googleapis.com",
    "account": "",
    "expiry": "2024-04-04T08:58:06.479136Z"
}

print("connecting with your google sheet....")
gc, authorized_user = gspread.oauth_from_dict(credentials, authorized_user)
 

 
print("opening the spreadsheet.....")
sh = gc.open("Network") 

wks = sh.sheet1  

max_num_rows=wks.row_count 
max_num_cols=wks.col_count


ranges = [f"D2:D{max_num_rows}"] 
print("Getting Values Through Gsheets API....")
range_object = wks.batch_get(ranges) 

values = [item for sublist in range_object for item in sublist]
#print(values)

  
row_indices = check_birthdays_sheets(values,today_day_month) 
rows_to_print = list() 
for row_index in row_indices:
    row_data = wks.row_values(row_index) 
    
    rows_to_print.append(row_data)     
print("Success in getting Gsheets data...")
 
 
     
