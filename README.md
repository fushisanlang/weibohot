# weibohot

## 说明
用于抓取和展示微博热搜，

## 运行

```
docker run -d   --name weibohot-31000 -p 31000:31000   weibohot
```
## 访问地址
* `/weibo/<date>` : 分时动态前十名
* `/weibo/report/<date>` : 当日数据总结

## todo
1. 根据查询情况，给表加索引（node列）
2. 选用es作为数据库
3. 静态资源上cdn(后续考虑)
4. 定时任务时间放到数据库。可配置化