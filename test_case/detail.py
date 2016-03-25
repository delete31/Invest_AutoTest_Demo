#coding:utf-8

#编辑直播的验证，最好加上对原文章标题、正文、来源的检测，延后
import unittest
from selenium import webdriver
import time
import HTMLTestRunner
from time import sleep
from common import login
import re

spath = '/Users/lihui/Documents/PycharmProjects/Invest/screenshot/'
#截图路径
class DetailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.broswer = webdriver.Chrome()
        cls.broswer.get("xxxx/login")
        login(cls)
        cls.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[2]').click()
        #进入到内容库界面
        sleep(4)
        cls.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div/div[2]/doc-list/div/div[5]/div/div[1]/a/div[2]/span').click()
        #点击一篇文章标题，进入该详情界面
        sleep(4)

    @classmethod
    def tearDownClass(cls):
        cls.broswer.close()

    def test_Detail_articleZoom(self):
        u'''字体大小切换'''
        try:
            exClass = self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/article-view/div').get_attribute('class')
            #获取当前的class属性，判断字体大小
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/div/div/span[2]/i').click()
            #点击字体放大
            sleep(1)
            exClass2 = self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/article-view/div').get_attribute('class')
            #点击字体放大的class属性
            self.assertNotEqual(exClass,exClass2,'字体没有变化')
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/div/div/span[1]/i').click()
            #点击字体变小后的class属性
            sleep(1)
            exClass3 = self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/article-view/div').get_attribute('class')
            sleep(1)
            self.assertNotEqual(exClass3,exClass2,'字体没有变化')
            #字体变大再变小后，class属性不一致，会多一个zoom = 0，默认就是0，但是没显示，所以改用2和3来进行判断
        except:
            self.broswer.get_screenshot_as_file(spath+'字体大小切换.png')
            raise


    def test_Detail_important(self):
        u'''标记重要'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[1]/button').click()
            #点击标记重要
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[1]/button/span').text,u'取消重要','没有取消重要按钮')
            #判断按钮是不是变成了取消重要
            self.assertFalse(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[2]/button').is_displayed(),'弃用按钮还显示')
            #判断弃用按钮是不是不显示了
        except:
            self.broswer.get_screenshot_as_file(spath+'标记重要.png')
            raise

    def test_Detail_importantRemove(self):
        u'''取消标记重要'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[1]/button').click()
            #点击取消重要按钮
            sleep(2)
            self.assertEqual(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[1]/button/span').text,u'标记重要','没有取消重要按钮')
            #判断按钮是不是变为了重要
            self.assertTrue(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[2]/button').is_displayed(),'弃用按钮不显示')
            #判断弃用按钮是否显示
        except:
            self.broswer.get_screenshot_as_file(spath+'取消重要.png')
            raise

    def test_Detail_useless(self):
        u'''标记弃用'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[2]/button').click()
            #点击弃用按钮
            sleep(4)
            self.assertIsNotNone(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/ui-view/div[2]/article-aside/div[1]/div/div/button'),'恢复按钮不存在')
            #判断恢复按钮是否存在
        except:
            self.broswer.get_screenshot_as_file(spath+'标记弃用.png')
            raise

    def test_Detail_uselessRemove(self):
        u'''恢复弃用稿件'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/ui-view/div[2]/article-aside/div[1]/div/div/button').click()
            #点击恢复按钮
            sleep(4)
            self.assertTrue(self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[2]/div[2]/button').is_displayed(),'弃用按钮不显示')
            #判断弃用按钮是否显示
        except:
            self.broswer.get_screenshot_as_file(spath+'恢复弃用.png')
            raise

    def test_Detail_link(self):
        u'''查看原文'''
        try:
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[2]/div[2]/table/tbody/tr[5]/td[2]/a').click()
            #点击查看原文
            sleep(4)
            self.assertEqual(2,len(self.broswer.window_handles),'没有打开原始链接')
            #通过当前的窗口数来判断是否打开了新的窗口
            now_handle = self.broswer.current_window_handle
            for handle in self.broswer.window_handles:#先切换到新打开的窗口，然后关掉
                if handle !=now_handle:
                    self.broswer.switch_to_window(handle)
                    self.broswer.close()
            self.broswer.switch_to_window(now_handle)#切换回原来的窗口
        except:
            self.broswer.get_screenshot_as_file(spath+'查看原文.png')
            raise

    def test_Detail_editLive(self):
        u'''编辑直播'''
        try:
            exURL = self.broswer.current_url
            #获取当前的url
            #exTitle = self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/article-view/div/h2').text
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[1]/div[2]/button').click()
            #点击编辑直播按钮
            sleep(4)
            self.assertEqual('xxxx/draft/live/_new',self.broswer.current_url,'没有进入到编辑直播界面')
            #由于新建直播的url都是一样的，所以直接用url来判断是否进入到了编辑直播界面
        except:
            self.broswer.get_screenshot_as_file(spath+'编辑直播.png')
            raise
        self.broswer.get(exURL)
        #打开原来的url，后退的话会回到内容库列表界面
        sleep(2)
        alert = self.broswer.switch_to_alert()
        alert.accept()
        print('accept done')
        sleep(4)
        #点击“是否离开当前界面”的弹出框

    def test_Detail_addDraft(self):
        u'''添加到草稿箱'''
        try:
            url = self.broswer.current_url
            exTitle = self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[1]/div/article-view/div/h2').text
            #获取当前稿件的title
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[1]/div[3]/button').click()
            #添加到草稿箱
            sleep(4)
            self.broswer.find_element_by_xpath('/html/body/div/ng-include[2]/aside/nav[2]/ul/li[5]').click()
            #切换到稿件箱界面
            sleep(4)
            self.assertEqual(exTitle,self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div/div/div[2]/div/div/table/tbody/tr[1]/td[3]/a').text,'没添加到草稿箱')
            #新添加的草稿会显示在第一个，看title是否和之前记录的一致
        except:
            self.broswer.get_screenshot_as_file(spath+'添加草稿箱.png')
            raise
        self.broswer.get(url)
        sleep(4)

    def test_Detail_editCol(self):
        u'''编辑稿件'''
        try:
            exurl = self.broswer.current_url
            self.broswer.find_element_by_xpath('/html/body/div/div/ui-view/div[2]/article-aside/div[1]/div[1]/div[1]/button').click()
            #点击编辑稿件按钮
            sleep(4)
            url = self.broswer.current_url
            self.assertEqual(url[:-24],'xxxx/draft/columns/','没有进入到编辑稿件界面')
        except:
            self.broswer.get_screenshot_as_file(spath+'编辑稿件.png')
            raise
        self.broswer.get(exurl)
        sleep(2)
        alert = self.broswer.switch_to_alert()
        alert.accept()
        sleep(4)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(DetailTest('test_Detail_articleZoom'))
    suite.addTest(DetailTest('test_Detail_important'))
    suite.addTest(DetailTest('test_Detail_importantRemove'))
    suite.addTest(DetailTest('test_Detail_useless'))
    suite.addTest(DetailTest('test_Detail_uselessRemove'))
    suite.addTest(DetailTest('test_Detail_link'))
    suite.addTest(DetailTest('test_Detail_editLive'))
    suite.addTest(DetailTest('test_Detail_addDraft'))
    suite.addTest(DetailTest('test_Detail_editCol'))
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
