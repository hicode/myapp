#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from blogProcessAPI import BlogProcess

getBlog_3ms = BlogProcess()
username = raw_input("please input your domain account:")
password = raw_input("please input your password:")

open_dir_path = r"d:\123\download"
save_dir_path = r"d:\123\content"

origURL = raw_input("please input entrance page address of the blog:")
if not origURL.startswith("http"):
  print "url must start with http"

getBlog_3ms.setinfo(username, password, origURL)
getBlog_3ms.login()
getBlog_3ms.getALLBlogsInfo()

getBlog_3ms.download_html_of_blog_list(open_dir_path, getBlog_3ms.Allblogs)
getBlog_3ms.parse_and_save_files(open_dir_path, save_dir_path)

