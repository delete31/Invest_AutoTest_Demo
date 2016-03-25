#coding:utf-8
import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
from common import login

spath = '/Users/lihui/Documents/PycharmProjects/Invest/screenshot/'
class HomePageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.broswer = webdriver.Chrome()
        cls.broswer.get("xxxx/login")
        login(cls)

    @classmethod
    def tearDownClass(cls):
        cls.broswer.close()

    def test_homepage_release(self):
        u''''点击首页中的今日生产稿件的查看，进入对应界面'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[1]/a').click()
            sleep(2)
            self.broswer.find_element_by_xpath('/html/body/div/div/div/div[1]/div[1]/div/div[3]').click()
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[6]').get_attribute('class'),
                             'active','没有跳转到资讯审核界面')
        except:
            self.broswer.get_screenshot_as_file(spath+'今日生产稿件.png')
            raise

    def test_homepage_myList(self):
        u'''点击首页中的今日我的稿件，进入对应界面'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[1]/a').click()
            sleep(2)
            self.broswer.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div[3]/div').click()
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[6]').get_attribute('class'),
                             'active','没有跳转到资讯审核界面')
            self.assertEqual(self.broswer.current_url[self.broswer.current_url.find('editor=')+7:],'564d406f76bf511e8d000004','没有筛选自己')
            #截取url中的editor后的id来判断有没有进行editor用户的筛选，如果login中登录的用户变更，这里的期望值也要做对应的修改
        except:
            self.broswer.get_screenshot_as_file(spath+'今日我的稿件.png')
            raise

    def test_homepage_sourceToady(self):
        u'''点击首页中的进入入库，进入对应界面'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[1]/a').click()
            sleep(2)
            self.broswer.find_element_by_xpath('/html/body/div/div/div/div[1]/div[3]/div/div[3]/div').click()
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[2]').get_attribute('class'),
                             'active','没有跳转到内容库')
        except:
            self.broswer.get_screenshot_as_file(spath+'今日入库.png')
            raise




if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(HomePageTest('test_homepage_release'))
    suite.addTest(HomePageTest('test_homepage_myList'))
    suite.addTest(HomePageTest('test_homepage_sourceToady'))
    timestr = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
    filename = '/Users/lihui/Documents/PycharmProjects/Invest/report/'+timestr+'.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='result',
        description='report'
    )
    runner.run(suite)
    fp.close()
