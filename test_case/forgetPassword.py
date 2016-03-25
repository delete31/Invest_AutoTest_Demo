#coding:utf-8
import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
import os

spath = '/Users/lihui/Documents/PycharmProjects/Invest/screenshot/'
class ForgetPasswordTest(unittest.TestCase):

    def setUp(self):
        self.broswer = webdriver.Chrome()
        self.broswer.get("xxxx/login")
        self.broswer.maximize_window()
        self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[3]/a').click()
        sleep(2)

    def tearDown(self):
        self.broswer.close()

    def test_ForgetPassword_access(self):
        u'''点击忘记密码按钮，跳转到忘记密码界面'''
        try:
            self.assertEqual(self.broswer.current_url,'xxxx/forgetpwd','没有跳转到忘记密码界面')
        except:
            self.broswer.get_screenshot_as_file(spath+'没有跳转到忘记密码界面.png')
            raise

    def test_ForgetPassword_disenabledButton(self):
        u'''输入非邮箱，确认按钮不可点'''
        try:
            self.broswer.find_element_by_name('email').send_keys('aaaaaaaaa')
            self.assertFalse(self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/form/div[2]/button[1]').is_enabled(),
                         '输入非邮箱，确认按钮可点')
        except:
            self.broswer.get_screenshot_as_file(spath+'非邮箱，按钮可点.png')
            raise

    def test_ForgetPassword_succeed(self):
        u'''输入正确的邮箱，点击确认按钮，提示邮件已发送'''
        try:
            self.broswer.find_element_by_name('email').send_keys('mayivisitor@sina.com')
            self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/form/div[2]/button[1]').click()
            sleep(2)
            self.assertIsNotNone(self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/div/p'),'正确邮箱，找回密码失败')
        except:
            self.broswer.get_screenshot_as_file(spath+'正确密码，找回失败.png')
            raise




if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_access'))
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_disenabledButton'))
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_succeed'))
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

