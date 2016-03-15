#coding=utf-8

import unittest
import sys
sys.path.append("/test_case")
#添加test_case目录

from test_case import forgetPassword,login
import HTMLTestRunner
import time

alltestnames = [login.LoginTest,
                forgetPassword.ForgetPasswordTest,
                ]

testunit = unittest.TestSuite()

for test in  alltestnames:
    testunit.addTest(unittest.makeSuite(test))

timestr = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
filename = '/Users/lihui/Documents/PycharmProjects/Invest/report/'+timestr+'.html'
fp = open(filename,'wb')
runner = HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    title='result',
    description='report'
)
runner.run(testunit)
fp.close()
print('执行完毕，报告路径:'+filename)