- 分词

  - 然后是分词得到要有的分类然后作为tag存到数据库
  - 分词得到关键词合成一个字符串存入数据库

- 页面ui

  - 分类展示（√）

    > ![image-20210923000752671](../../OneDrive/%E5%9B%BE%E7%89%87/typora/image-20210923000752671.png)

  - 所有的关键词作为一个页面展示

  - 首页也要有动态的分类树，添加基网址
  
    #### 								设计方案——爬虫功能

一、研究目标

> 

二、研究内容

三、方案设计

> 1. 爬虫对象
>    - 今日头条和网易新闻
>    
> 2. 编码工具及语言
>
>    - python语言
>    - 采用Pycharm或者Visual Studio Code
>    - 采用pipenv作为包管理器/或者直接使用requirement.txt管理包
>
> 3. 首先设计数据库
>    - 包括以下字段：`不同网站的结构不同，以下属性并不是所有的都要有`
>      > | Name          | Type     | Length | Not Null | Key  | Comment      |
>      > | ------------- | -------- | ------ | -------- | ---- | ------------ |
>      > | news_id       | int      | /      | √        | √    | 新闻编号     |
>      > | created       | datetime | /      | /        | /    | 爬取时间     |
>      > | title         | varchar  | 255    | /        | /    | 新闻标题     |
>      > | tag/category  | varchar  | 255    | √        | /    | 新闻分类     |
>      > | abstract      | varchar  | 1000   | /        | /    | 新闻概要     |
>      > | article_url   | varchar  | 1000   | /        | /    | 新闻链接     |
>      > | behot_time    | datetime | /      | /        | /    | 开始热门时间 |
>      > | publish_time  | datetime | /      | /        | /    | 发布时间     |
>      > | keyword_str   | varchar  | 255    | /        | /    | 新闻关键词   |
>      > | comment_count | int      | /      | /        | /    | 评论数       |
>      > | like_count    | int      | /      | /        | /    | 点赞数       |
>      > | read_count    | int      | /      | /        | /    | 阅读数       |
>      > | source        | varchar  | 255    | /        | /    | 来源/作者    |
>
> 4. 开始爬取
>
>    1. 今日头条
>    2. 网易新闻

四、系统实现

五、总结



#### 						设计方案——分类及URL管理

三、方案设计

> 1. 新闻分类
>    - 
> 2. URL管理

