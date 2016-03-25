#coding:utf-8

#还缺日期、类目、栏目、来源、撰写机构的筛选,勾选加入草稿箱，点击后查看detail，hover后标重要弃用，查看弃用界面，只看重要文章

import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
from common import login
import re

spath = '/Users/lihui/Documents/PycharmProjects/Invest/screenshot/'
#截图路径
class SourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.broswer = webdriver.Chrome()
        cls.broswer.get("xxxx/login")
        login(cls)
        cls.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[2]').click()
        sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.broswer.close()

    def test_source_searchText(self):
        u'''输入搜索词进行搜索'''
        try:
            #不加延时的话，可能导致获取不到当前的数量
            exResult = re.search('\d+',self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div/div[1]/ul/li/span[2]').text).group()
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[1]/nav/div/div[3]/form/div/input').send_keys(u'大盘')
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[1]/nav/div/div[3]/form/div/div').click()
            sleep(2)
            self.assertNotEqual(exResult,re.search('\d+',self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div/div[1]/ul/li/span[2]').text).group(),'搜索结果条数一样')
        except:
            self.broswer.get_screenshot_as_file(spath+'搜索词搜索.png')
            raise

    def test_source_autoRefresh(self):
        u'''自动刷新功能'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div/div[1]/div/label[1]/i').click()
            currentURL = self.broswer.current_url
            self.assertEqual(currentURL[currentURL.find('refresh=')+8:],'1','没有自动刷新')
        except:
            self.broswer.get_screenshot_as_file(spath+'自动刷新.png')
            raise

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SourceTest('test_source_searchText'))
    suite.addTest(SourceTest('test_source_autoRefresh'))
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
