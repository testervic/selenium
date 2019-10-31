#coding:utf-8
from selenium import webdriver
import os
import re
import datetime
import unittest
from config import HTMLTestRunner
from config.selenium_config import selenium_config
from public.common.sendEmail import send_email_report
from config.email_config import email_config
from public.selenium_test.ProjectCase.Shopping import *

#webdriver浏览器设置
def set_driver(browser):
    if str(browser).lower() not in ('chrome', 'firefox'):
        return False
    elif str(browser).lower() == 'chrome':
        selenium_config['browser'] = 'Chrome'
        selenium_config['driver'] = webdriver.Chrome()
    elif str(browser).lower() == 'firefox':
        selenium_config['browser'] = 'Firefox'
        selenium_config['driver'] = webdriver.Firefox()
    selenium_config['driver'].implicitly_wait(10)

#报告路径和快照目录配置
def set_path(browser, project):
    # 设置快照和报告路径
    date_str = re.sub('[- :]', '', str(datetime.datetime.now()).split('.')[0])
    selenium_config['snapshot_path'] = '/' + os.getcwd() + '//' + 'snapshot' + '//' + str(project).upper() + '_'
    #selenium_config['report_file_path'] = os.getcwd() + '\\report\\' + str(project).upper() + '_' + str(browser).upper() + '_' + 'HTMLReport' + date_str + '.html'
    selenium_config['report_file_path'] = '/' + os.getcwd() + '//' + 'report' + '//' + str(project).upper() + '_' + str(browser).upper() + '_' + 'HTMLReport' + date_str + '.html'

#执行用例
def selenium_common(browser, project):
    if set_driver(browser) is not False:
        set_path(browser, project)
        from public.selenium_test.ProjectCase.Shopping import Shopping
        # 设置测试用例组件
        suite = unittest.TestSuite()
        # 用例流程添加，把需要执行的case放到这里
        tests = [Shopping("Case_1")
                 #Shopping("Case_2")
                 ]
        suite.addTests(tests)
        #保存测试报告
        with open(selenium_config['report_file_path'], 'w') as report_f:
            runner = HTMLTestRunner.HTMLTestRunner(
                stream=report_f,
                title=project + '_' + 'Automated test report',
                description='generated by HTMLTestRunner.',
                verbosity=2
            )
            runner.run(suite)
        '''
        #邮件发送
        email_config['receiver'] = 'zw.vic@qq.com'
        email_config['attachment'] = [selenium_config['report_file_path']]
        email_config['mail_body'] = '自动化测试报告邮件内容'
        email_config['password'] = ''
        send_email_report(email_config)
        '''
    else:
        print 'driver配置失败，退出执行'.decode('utf-8')
