#coding:utf-8
import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
class ForgetPasswordTest(unittest.TestCase):

    def setUp(self):
        self.broswer = webdriver.Chrome()
        self.broswer.get("/login")
        self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[3]/a').click()
        sleep(2)

    def tearDown(self):
        self.broswer.close()

    def test_ForgetPassword_access(self):
        u'''点击忘记密码按钮，跳转到忘记密码界面'''
        self.assertEqual(self.broswer.current_url,'/forgetpwd','没有跳转到忘记密码界面')

    def test_ForgetPassword_disenabledButton(self):
        u'''输入非邮箱，确认按钮不可点'''
        self.broswer.find_element_by_name('email').send_keys('aaaaaaaaa')
        self.assertFalse(self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/form/div[2]/button[1]').is_enabled(),
                         '输入非邮箱，确认按钮可点')

    def test_ForgetPassword_succeed(self):
        u'''输入正确的邮箱，点击确认按钮，提示邮件已发送'''
        self.broswer.find_element_by_name('email').send_keys('mayivisitor@sina.com')
        self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/form/div[2]/button[1]').click()
        sleep(3)
        self.assertIsNotNone(self.broswer.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/div/p'),'正确邮箱，找回密码失败')




if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_access'))
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_disenabledButton'))
    suite.addTest(ForgetPasswordTest('test_ForgetPassword_succeed'))
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
