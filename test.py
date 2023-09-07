import requests
import random
import datetime

start_dt = datetime.date(2023, 2, 1)
end_dt = datetime.date(2024, 3, 1)
time_between_dates = end_dt - start_dt
days_between_dates = time_between_dates.days

BASE = "http://127.0.0.1:5000/"

# insert into user and get user id
# response = requests.post(BASE + "/user/")
# print(response.json())

userID = "0958b2bc-7eb1-4e80-af05-503da47b96dd"

data = [{"title": "bill1", "description": "prajwal", "tag": "electricity", "dateTaken": (start_dt + datetime.timedelta(days=random.randrange(days_between_dates))).strftime("%m/%d/%Y, %H:%M:%S"), "imagePath": "a", "userId": userID},
        {"title": "bill2", "description": "pop", "tag": "grocery", "dateTaken": (start_dt + datetime.timedelta(days=random.randrange(days_between_dates))).strftime("%m/%d/%Y, %H:%M:%S"), "imagePath": "a", "userId": userID},
        {"title": "bill3", "description": "soap", "tag": "cosmetics", "dateTaken": (start_dt + datetime.timedelta(days=random.randrange(days_between_dates))).strftime("%m/%d/%Y, %H:%M:%S"), "imagePath": "a", "userId": userID},
        {"title": "bill4", "description": "asdw", "tag": "electronics", "dateTaken": (start_dt + datetime.timedelta(days=random.randrange(days_between_dates))).strftime("%m/%d/%Y, %H:%M:%S"), "imagePath": "a", "userId": userID}
]

for i in range(len(data)):
    response = requests.post(BASE + "bill/" + str(i) + '/', data[i])
    print(response.json())

# input()

# response = requests.get(BASE + "bill/9")
# print(response.json())
