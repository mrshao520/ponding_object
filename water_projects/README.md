# 大城市暴雨积水点可视化项目

## 打包

```
Pyinstaller -F -w -i xx.ico
```

* -F 制作可独立允许的可执行程序
* -w 不打开命令行
* -i xx.ico 设置图标图案



* 不带窗口

```
pyinstaller -F -w -i ./title.ico --name ponding main.py  -p ./src/widgets/QtContentWidget.py -p ./src/widgets/QtHeaderWidget.py -p ./src/widgets/QtMainWidget.py -p ./src/widgets/QtWebView.py -p ./src/widgets/Ui_content.py -p ./src/utils/JsonParser.py -p ./src/utils/LoginWeibo.py -p ./src/utils/Path.py -p ./src/utils/ReptilesProcess.py -p ./src/utils/Server.py -p ./src/utils/ServerThread.py -p ./src/pachong/douyin/douyin.py -p ./src/pachong/souhu/spiders/souhu_data.py -p ./src/pachong/souhu/items.py  -p  ./src/pachong/souhu/middlewares.py -p ./src/pachong/souhu/pipelines.py -p  ./src/pachong/souhu/settings.py -p  ./src/pachong/tengxun/spiders/tx_data.py -p  ./src/pachong/tengxun/items.py -p  ./src/pachong/tengxun/middlewares.py -p  ./src/pachong/tengxun/pipelines.py -p  ./src/pachong/tengxun/settings.py -p  ./src/pachong/weibo/spiders/weibo_data.py -p  ./src/pachong/weibo/items.py -p  ./src/pachong/weibo/middlewares.py -p  ./src/pachong/weibo/pipelines.py -p  ./src/pachong/weibo/settings.py -p ./src/pachong/baidu/baidu.py -p ./src/pachong/toutiao/toutiao.py -p  ./src/pachong/utils.py --hidden-import PyQt5.QtWebChannel --hidden-import chardet --hidden-import charset-normalizer --hidden-import lxml --hidden-import lxml.html --hidden-import lxml.etree
```



* 带窗口

```
pyinstaller -F -i ./title.ico --name ponding main.py  -p ./src/widgets/QtContentWidget.py -p ./src/widgets/QtHeaderWidget.py -p ./src/widgets/QtMainWidget.py -p ./src/widgets/QtWebView.py -p ./src/widgets/Ui_content.py -p ./src/utils/JsonParser.py -p ./src/utils/Path.py -p ./src/utils/ReptilesProcess.py -p ./src/utils/Server.py -p ./src/utils/ServerThread.py -p ./src/utils/LoginWeibo.py -p ./src/pachong/douyin/chaojiying.py -p ./src/pachong/douyin/douyin.py -p ./src/pachong/souhu/spiders/souhu_data.py -p ./src/pachong/souhu/items.py  -p  ./src/pachong/souhu/middlewares.py -p ./src/pachong/souhu/pipelines.py -p  ./src/pachong/souhu/settings.py -p  ./src/pachong/tengxun/spiders/tx_data.py -p  ./src/pachong/tengxun/items.py -p  ./src/pachong/tengxun/middlewares.py -p  ./src/pachong/tengxun/pipelines.py -p  ./src/pachong/tengxun/settings.py -p  ./src/pachong/weibo/spiders/weibo_data.py -p  ./src/pachong/weibo/items.py -p  ./src/pachong/weibo/middlewares.py -p  ./src/pachong/weibo/pipelines.py -p  ./src/pachong/weibo/settings.py -p  ./src/pachong/utils.py --hidden-import PyQt5.QtWebChannel --hidden-import chardet --hidden-import charset-normalizer --hidden-import lxml --hidden-import lxml.html --hidden-import lxml.etree
```





