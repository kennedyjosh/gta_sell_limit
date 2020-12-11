import datetime
import os
import pickle
import sys
import time

save_path = os.path.join(os.getcwd(), ".picklejar")

class TTL:
    HOUR = 3600
    def __init__(self, ts = None):
        if ts == None:
            self.ts = int(time.time())
        else:
            self.ts = ts

    def __eq__(self, other):
        return self.ts == other

    def __hash__(self):
        return hash(self.ts)

    def __getnewargs_ex__(self):
        return ((), {'ts': self.ts})

    def get_time_passed(self):
        return int(time.time()) - self.ts
        
    def check_2hr_limit(self):
        return 0 if self.get_time_passed() > (2 * TTL.HOUR) else (2 * TTL.HOUR) - self.get_time_passed()

    def check_30hr_limit(self):
        return 0 if self.get_time_passed() > (30 * TTL.HOUR) else (30 * TTL.HOUR) - self.get_time_passed()

def save(data):
    data += load()
    data = list(dict.fromkeys(data))
    try:
        os.remove(save_path)
    except:
        pass
    with open(save_path, "wb") as f:
        pickler = pickle.Pickler(f)
        pickler.dump(data)

def load():
    timestamps = [1607562900, 1607634662, 1607577300, 1607577780, 1607586900, 1607588640, 1607634660]
    data = [TTL(ts) for ts in timestamps]
    if os.path.isfile(save_path):
        with open(save_path, "rb") as f:
            unpickler = pickle.Unpickler(f)
            data = unpickler.load()
    return data

def main(opt = None):
    running = True
    while running:
        if opt not in [1, 2]:
            print("Choose one of the following:")
            print("\t1. Sold a car")
            print("\t2. Check limits")
            print("\t3. Exit program")
            opt = None
            while opt not in [1, 2, 3]:
                response = input("Enter a number corresponding with your desired choice: ")
                try:
                    opt = int(response.strip())
                except:
                    opt = None
        print("-" * 40)
        if opt == 1:
            data = load()
            data.append(TTL())
            save(data)
            opt = 2
        if opt == 2:
            data = load()
            data = list(dict.fromkeys(data))
            limit_2hr = 0
            limit_30hr = 0
            limit_2hr_ends = float("inf")
            limit_30hr_ends = float("inf")

            to_remove = []
            for ttl in data:
                if ttl.check_2hr_limit() > 0:
                    limit_2hr += 1
                    if ttl.check_2hr_limit() < limit_2hr_ends:
                        limit_2hr_ends = ttl.check_2hr_limit()
                else:
                    to_remove.append(ttl)
                if ttl.check_30hr_limit() > 0:
                    limit_30hr += 1
                    if ttl.check_30hr_limit() < limit_30hr_ends:
                        limit_30hr_ends = ttl.check_30hr_limit()
                else:
                    to_remove.append(ttl)

            to_remove = list(dict.fromkeys(to_remove))
            for ttl in to_remove:
                data.remove(ttl)

            save(data)

            if limit_2hr < 2 and limit_30hr < 7:
                print("You can sell a car.")
            else:
                print("Do not sell any more cars.")
                if limit_2hr >= 2:
                    print("You have reached the 2 car per 2hr limit.")
                    date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(time.time()) + limit_2hr_ends)
                    date = date.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                    ok_date = date.strftime("%I:%M%p on %b %d").replace("AM", "am").replace("PM", "pm")
                    print("This limit expires at {}".format(ok_date))
                if limit_30hr >= 7:
                    print("You have reached the 7 car per 30 hour limit.")
                    date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(time.time()) + limit_30hr_ends)
                    date = date.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                    ok_date = date.strftime("%I:%M%p on %b %d").replace("AM", "am").replace("PM", "pm")
                    print("This limit expires at {}".format(ok_date))
            print()        
            print("You currently have {} car{} sold in the last 2 hours.".format(limit_2hr,
                                                                                     "s" if limit_2hr != 1 else ""))
            print("You currently have {} car{} sold in the last 30 hours.".format(limit_30hr,
                                                                                     "s" if limit_30hr != 1 else ""))
            opt = None
        if opt == 3:
            running = False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            opt = int(sys.argv[1])
            main(opt = opt)
        except:
            main()
    else:
        main()
