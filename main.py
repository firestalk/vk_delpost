#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from splinter import Browser
from time import sleep
import re
import json
import sys


class VkDelPost:
    def __init__(self):
        self.account = self.load_cfg()

    def main(self):
        email = self.account['email']
        passw = self.account['passw']
        with Browser('phantomjs') as browser:
            url = "http://vk.com"
            browser.visit(url)
            browser.fill('email', email)
            browser.fill('pass', passw)
            browser.find_by_id('quick_login_button').click()
            mypage = browser.find_by_id('myprofile')
            if mypage:
                print('Logged In')
            else:
                print('Login failed')
                self.dump_page(browser.html)
                return False
            profile_str = browser.find_by_id('myprofile_wrap').first
            profile = re.findall(r'href="([^."]+)', profile_str.html)[0]
            url = "http://vk.com" + profile
            while True:
                sleep(2)
                browser.visit(url)
                sec_chk = browser.find_by_id('check_msg')
                if sec_chk:
                    print("Security check page.")
                    self.sec_page(browser)
                    return False
                pagetxt = browser.html
                id_lst = re.findall(r'id="post_delete([^.]\d+_\d+)"', pagetxt)
                if len(id_lst) > 0:
                    print("Post Count: {}".format(len(id_lst)))
                    for i in id_lst:
                        button = browser.find_by_id('post_delete' + str(i))
                        button.click()
                    print('Posts deleted')
                else:
                    print('Post deletion button not found')
                    return False

    def sec_page(self, browser):
        print('TODO: This part is not done yet.')
        ppref = browser.find_by_xpath('/html/body/div[9]/div/div/div/div[3]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/div')
        print(ppref)
        ppost = browser.find_by_xpath('/html/body/div[9]/div/div/div/div[3]/div[3]/div/div/div/div/table/tbody/tr[1]/td[3]/span')
        print(ppost)

    def dump_page(self, html):
        with open('pagedump.html', 'w') as htp:
            try:
                htp.write(html)
            except UnicodeEncodeError:
                htp.write(str(html.encode(sys.stdout.encoding, errors='replace')))
        return

    def load_cfg(self):
        with open('config.json', 'r') as cfg:
            data = json.load(cfg)
        return data


if __name__ == "__main__":
    vkd = VkDelPost()
    vkd.main()
