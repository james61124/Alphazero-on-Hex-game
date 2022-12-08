from selenium import webdriver
import re

# maintain the board game on the website
# r: 1; b: 2
class hex_bot:
    def index_convert_i_e(n):
        letter = chr(n // 11 + 65)
        col = n % 11 + 1
        idx = str(letter) + str(col)
        return idx

    driver = webdriver.Chrome("./chromedriver")
    driver.get("http://www.lutanho.net/play/hex.html")

    # web objects
    btn_new_game = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[9]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/input")

    btn_r_p = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[2]")
    btn_b_p = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[3]/td/table/tbody/tr[1]/td/input")
    
    btn_b_lvl1 = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[1]")
    btn_b_lvl2 = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[2]")
    btn_b_lvl3 = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[3]")

    chkbox_swaprule = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[7]/td/table/tbody/tr/td/input[1]")

    msgbox = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[9]/td/table/tbody/tr[3]/td/input")
    movelistbox = driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[5]/table/tbody/tr[11]/td/table/tbody/tr[1]/td/textarea")

    hex_btn = []
    for i in range(0, 120):
        hex_btn.append(driver.find_element_by_xpath("//img[@title='" + index_convert_i_e(i) + "']"))
    # end of web objects

    # mode code:
        # agent-bot: 1
        # agent-agent: 2
        # swaprule 0: deactivate
    mode = 1
    MoveCount = 0
    def __init__(self, _mode, level, swaprule):
        self.new_game(_mode, level, swaprule)
        return
    
    def new_game(self, _mode, level, swaprule):
        self.btn_new_game.click()
        MoveCount = 0
        self.mode = _mode
        if self.mode == 1:
            if level == 1:
                self.btn_b_lvl1.click()
            if level == 2:
                self.btn_b_lvl2.click()
            if level == 3:
                self.btn_b_lvl3.click()
        elif self.mode == 2:
            self.btn_r_p.click()
            self.btn_b_p.click()
        if (not swaprule):
            # if (self.chkbox_swaprule.get_attribute("value") == "on"):
            self.chkbox_swaprule.click()
        return

    # not ended: 0
    # red won: 1
    # blue won: 2
    def is_done(self):
        msg = self.msgbox.get_attribute('value') 
        done_flag = self.driver.execute_script("return IsOver")
        if (done_flag):
            if (bool(re.search("Red", msg))):
                return 1
            else:
                return 2
        else:
            return 0

    def agent_put(self, move):
        if (self.mode == 1):
            self.MoveCount += 2

            # wait the history array to be updated and get what move did the bot make
            history = self.driver.execute_script("return History")[self.MoveCount - 1]
            self.hex_btn[move].click()
            new_history = self.driver.execute_script("return History")[self.MoveCount - 1]
            while history == new_history:
                new_history = self.driver.execute_script("return History")[self.MoveCount - 1]
            history = new_history
            i, j = history

            idx = i + j * 11
            return idx
        return 0