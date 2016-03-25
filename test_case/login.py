#coding:utf-8
import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
import os

spath = '/Users/lihui/Documents/PycharmProjects/Invest/screenshot/'
class LoginTest(unittest.TestCase):

    def setUp(self):
        self.broswer = webdriver.Chrome()
        self.broswer.get("xxxx/login")
        self.broswer.maximize_window()

    def tearDown(self):
        self.broswer.close()

    def test_login_wrongEmail(self):
        u'''输入非邮箱，登录按钮不可点'''
        try:
            self.broswer.find_element_by_name('email').send_keys('investeditorchsina.com')
            self.assertFalse(self.broswer.find_element_by_tag_name('button').is_enabled(),'输入非邮箱，登录按钮可点')
        except:
            self.broswer.get_screenshot_as_file(spath+'非邮箱，登录按钮不可点.png')
            raise

    def test_login_tooShortPassword(self):
        u'''正确邮箱，小于8位密码，登录按钮不可点'''
        try:
            self.broswer.find_element_by_name('email').send_keys('investeditorch@sina.com')
            self.broswer.find_element_by_name('password').send_keys('test')
            self.assertFalse(self.broswer.find_element_by_tag_name('button').is_enabled(),'正确邮箱，小于8位的密码，登录按钮可点')
        except:
            self.broswer.get_screenshot_as_file(spath+'密码小于8位，登录按钮不可点.png')
            raise

    def test_login_wrongPassword(self):
        u'''错误的账号密码，提示语正确'''
        try:
            self.broswer.find_element_by_name('email').send_keys('investeditorch@sina.com')
            self.broswer.find_element_by_name('password').send_keys('test12345678')
            self.broswer.find_element_by_tag_name('button').click()
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/form/div[4]').text,
                         u'登录失败：邮箱或密码错误。','错误的账号密码的提示错误')
        except:
            self.broswer.get_screenshot_as_file(spath+'错误账号密码，提示错误.png')
            raise
        #遇到的坑，编码问题，把要匹配的编码改成和被匹配的编码一致

    def test_loginSucceed(self):
        u'''正确的账号密码，登录成功'''
        try:
            self.broswer.find_element_by_name('email').send_keys('investeditorch@sina.com')
            self.broswer.find_element_by_name('password').send_keys('test1234')
            self.broswer.find_element_by_tag_name('button').click()
            sleep(2)
            try:
                self.broswer.find_element_by_xpath('/html/body/div[2]/ng-transclude/hg-popup-dialog/div/div/div/div[1]/button').click()
            except:
                print('登录后15分钟内不用再次校验')
            sleep(2)
            self.assertEqual(self.broswer.current_url,'xxxx/home','未跳转至首页')
        except:
            self.broswer.get_screenshot_as_file(spath+'登录成功，未跳转至首页.png')
            raise



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_login_wrongEmail'))
    suite.addTest(LoginTest('test_login_tooShortPassword'))
    suite.addTest(LoginTest('test_login_wrongPassword'))
    suite.addTest(LoginTest('test_loginSucceed'))
    timestr = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
    #os.mkdir(os.path.join(os.path.dirname(__file__),timestr))
    #filename = os.path.dirname(__file__)+'/'+timestr+'/'+timestr+'.html'
    filename = '/Users/lihui/Documents/PycharmProjects/Invest/report/'+timestr+'.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='result',
        description='report'
    )
    runner.run(suite)
    fp.close()
