from datetime import datetime, timedelta
import math

time_str = "Comienza en 34 min"
mins = int(time_str.split()[2])
date_match = datetime.now() + timedelta(minutes=mins)
diff = (round(date_match.minute/5)*5) - date_match.minute
date_match = date_match + timedelta(minutes=diff)
ret = f"{date_match.day}-{date_match.hour:0>2}:{date_match.minute:0>2}"
print(ret)