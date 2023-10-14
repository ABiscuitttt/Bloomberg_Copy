import os
import time
import datetime
import json
import pyautogui
import pyperclip


class COPYDATA():
    def __init__(self, index_name: str) -> None:
        print(f"init for {index_name}")
        self.id_name = index_name
        with open("box.json", "r") as f:
            self.box = json.load(f)
        with open("time_range.json", "r") as f:
            self.time_range = json.load(f)

        # location of date box
        self.time1_center, self.time2_center = \
            pyautogui.center(self.box["time1_box"]),\
            pyautogui.center(self.box["time2_box"])

        # location of Index box
        self.index_center = pyautogui.center(self.box["index_box"])

        # Offset of cut button
        l_points_mid = list()
        with open("posconfig", "r") as fp:
            points = fp.readlines()[1:]
            for i in points:
                t = tuple(map(int, i[:-1].split(',')))
                l_points_mid.append(((t[0] + t[2]) / 2, (t[1] + t[3]) / 2))
        self.offset1 = l_points_mid[5][0] - \
            l_points_mid[4][0], l_points_mid[5][1]-l_points_mid[4][1]
        self.offset2 = l_points_mid[6][0] - \
            l_points_mid[4][0], l_points_mid[6][1]-l_points_mid[4][1]
        self.offset = self.offset1, self.offset2

        print("all points loaded")

        # check dir existing?
        self.data_dir = f"DATASET\\{index_name}"
        if os.path.exists(self.data_dir):
            print("path aleady exists, checking data")
            self.already = sorted(os.listdir(
                self.data_dir))  # TODO Check format
            if self.already.__len__() > 0:
                self.already = self.already[0]
                print(f"using {self.already} as initial date")
            else:
                self.already = None
                print("no previous data")
        else:
            self.already = None
            os.makedirs(self.data_dir)
            print(f"created dir {self.data_dir}")

        # init data var
        self.data = None

    def set_index(self) -> None:
        index_center = self.index_center
        pyautogui.doubleClick(index_center)
        pyautogui.typewrite(self.id_name+" index\n")

    def set_time(self):
        time1_center, time2_center = self.time1_center, self.time2_center

        pyautogui.click(time1_center)
        pyautogui.typewrite(self.time_range["end"])
        pyautogui.click(time2_center)
        pyautogui.typewrite(self.time_range["end"]+"\n")

    def check_status(self):
        # check existing data -> already in __init__()
        # check blm interface
        l = pyautogui.locateOnScreen(
            f"compare\\{self.id_name}.png", confidence=0.98)
        if l:
            return True
        else:
            return False

    def save_compare_img(self):
        im = pyautogui.screenshot(region=self.box["index_box"])
        im.save(f"compare\\{self.id_name}.png")

    def copy_loop(self, delay=3):
        end_day = self.time_range["end"]
        end_day = datetime.date(
            int(end_day[4:]),
            int(end_day[:2]),
            int(end_day[2:4]))

        start_day = self.time_range["start"]
        start_day = datetime.date(
            int(start_day[4:]),
            int(start_day[:2]),
            int(start_day[2:4]))

        #fix the loop (recopy var end_day)
        if self.already:
            tmp = datetime.date(
                int(self.already[:4]),
                int(self.already[4:6]),
                int(self.already[6:])).toordinal()-2
            end_day = datetime.date.fromordinal(tmp)

        for i in range(end_day.toordinal()+1, start_day.toordinal(), -1):
            if datetime.date.fromordinal(i).isoweekday() >= 6:
                continue
            day_to_copy = datetime.date.fromordinal(
                i).isoformat().replace("-", "")
            date_fixed = day_to_copy[4:] + day_to_copy[:4]
            print(f"date:{day_to_copy}")
            self.data = self.__exec_copy(date_fixed, delay), day_to_copy
            self.__save_data()

    def __exec_copy(self, datetime, delay=3) -> str:

        time1_center, time2_center = self.time1_center, self.time2_center

        pyautogui.click(time1_center)
        pyautogui.typewrite(datetime)
        pyautogui.click(time2_center)
        pyautogui.typewrite(datetime+"\n")

        time.sleep(delay)

        offset1, offset2 = self.offset

        print("finding proper position to do copy:")
        l = pyautogui.locateOnScreen("ref.png", region=[400, 240, 1920, 700])
        print("\t\t", l)
        c = pyautogui.center(l)
        pyautogui.rightClick(c[0], c[1], duration=0.1)
        pyautogui.click(c[0]+offset1[0], c[1]+offset1[1], duration=0.1)
        pyautogui.click(c[0]+offset2[0], c[1]+offset2[1], duration=0.1)

        data = pyperclip.paste().replace("\r\n", "\n")
        return data

    def __save_data(self):
        data = self.data
        if data[0][:4] == "Date":
            with open(f"{self.data_dir}\\{data[1]}", "wb") as fp:
                fp.write(data[0].encode())
                print(f"{data[1]} DONE")
                pyperclip.copy("DONE")
        else:
            print(f"{data[1]} NO DATA")

    @staticmethod
    def show_config():
        with open("box.json", "r") as f:
            print(f.read())
        with open("time_range.json", "r") as f:
            print(f.read())
