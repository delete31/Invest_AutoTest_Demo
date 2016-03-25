#coding:utf-8
from selenium import webdriver
from time import sleep
import time

def login(self):
    #登录操作
    self.broswer.find_element_by_name('email').send_keys('investeditorch@sina.com')
    self.broswer.find_element_by_name('password').send_keys('test1234')
    self.broswer.find_element_by_tag_name('button').click()
    sleep(2)
    try:
        self.broswer.find_element_by_xpath('/html/body/div[2]/ng-transclude/hg-popup-dialog/div/div/div/div[1]/button').click()
    except:
        print('登录后15分钟内不用再次校验')
    sleep(5)
    self.broswer.maximize_window()