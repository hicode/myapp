


#mysql
SHOW CHARACTER SET;

create database tradeData character set utf8;
use tradeData;
create table tradeData (pId int, pName char(19), tradeDay datetime, buyerName varchar(39), buyAmount int, sellerName varchar(39), sellAmount int) ;

create table test (s varchar(8)) CHARACTER SET gb2312 COLLATE gb2312_chinese_ci;
create table test11(s varchar(8))  ENGINE=InnoDB DEFAULT CHARSET=gbk; 

SHOW CREATE DATABASE test;
SHOW CREATE table test;
SHOW VARIABLES LIKE 'character_set%';
# 测试
'''测试'''

