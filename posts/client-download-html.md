Title: client-download-html
Tags: 
Category: 
Type: 1


@
@@
## 浏览器工作过程

@@

1. 资源下载  HTML, CSS, JS，image文件
2. HTML解析 DOM树
3. CSS计算  渲染树
4. 布局     带位置和开关的树
5. 渲染     可见的图形
6. 优化


@
@@
## HTML文件下载

@@
## 如何下载？

1. DNS client 得到IP
2. web request 请求地址
3. networking steam 获取数据
4. HtmlParser  解析成dom树

@@
### 够了么？

@@
### 不仅仅是一个文件

1. <script src
2. <link href
3. <img src
4. <iframe src

@@
### 何时开始下载他们？是否有依赖关系？如何下载？

@@
### 哪些因素影响下载？

@@
### head中的script link
可能包含脚本和外部资源链接，一般是样式表。
一般head中的资源需要优先下载，默认认为head中的资源是body中的依赖文件。
特别是chrome中，head会单独下载，阻塞body。

@@
### 服务器端的Response.Flush()方法
facebook的bigpipe利用此原理。
当flush时，服务器会单独的把flush之前的内容给浏览器，并且告诉他这是一块内容。
下一块什么时候传出，是不确定的。
这时候client网络模块已经空闲。

@@
### body中的script标签

@@
### document.write
该方法会向浏览器的文档流中注入数据，这样会使得浏览器必须等待此过程。
这是一个阻塞的过程。

@@
### new Image().src = ...
Image不需要和dom树挂钩。没有任何资源非得依赖图片，所以图片一般是尽早的并行下载。

@@
### defer vs async(HTML5开始定义)
在dom树解析执行之后，开始下载解析资源，并执行。

@
@@
### [资源优先级问题](http://www.cnblogs.com/GrayZhang/archive/2011/03/08/browser-strategy-loading-external-resource.html)

@@
### 资源优先级
1 link(css,js)
2. object /img/ iframe
3. link[rel=prefetch]（预加载）

@@
### 脚本依赖
#### 方法: 下载阻塞 VS 执行阻塞
1. 下载阻塞 窜行的瀑布流下载。碰到阻塞资源会很慢
2. 执行阻塞（IE7之后）, 利用队列并行下载。碰到依赖时，等待依赖资源下载完。

脚本是可执行的，可执行意味着有执行依赖的问题。

@@
### 并行度
#### 考虑：服务器压力 VS 客户端效率

假设有56张图片，一万个用户同时下载。

1. 从客户端来考虑，肯定是并发越多越好。
2. 从服务器压力来考虑，并发一定要控制在某个阈值。不能太高，也不能太低。

浏览器有个并行度的设置，一般是6个。

@
@@
## Socket重用

@@
### Http走的是Tcp协议
tcp协议很大一个特点就是需要三次握手的过程。三次握手的三次通讯很消耗资源

@@
### Connection: keep-alive （长连接）
重用TCP链接，对下载的优化很显著。
当设置Connection时，TCP链接没有关闭。

@@
### 会带来什么问题？

@@
### 我怎么知道资源下载完成了呢？

@@
### 填充字节。(不靠谱）

@@
### Content-Length，显示的告诉你文件有多大。客户端接受同样大小的文件。

@@
### 碰到大文件怎么办？

@@
### Transfer-Encoding: chucked
分段下载，每段告诉浏览器有多长。最后一个chunk长度为0，显示告诉你结束。

@
@@
### 还有什么问题？

@@
### 正确性校验, Content-MD5

@@
### 断点续传
1. Accept-Range 请求头，请求时告诉服务器要哪一段。
2. Content-Range 接收头, 服务器告诉你现在属于哪一段。

@
@@
### BS vs CS 模型

@@
### 如何解决更新问题, 缓存模型

@@
### 验证性缓存 缺点，还是要请求。
1. Last-Modified & if-Modified-Since / if-Unmodified-Since
2. Etag & if-match / if-None-Match
3. if-range

@@
### 非验证性缓存
1. Cache-Control (max-age)指定缓存多少秒
2. Expires       指定缓存到什么时候

@@
### 缓存失效 服务器端想强制更新怎么办？
1. Vary
2. Via
3. Date
4. Age

@@
### 缓存年龄计算
1. age_value  Age响应头的值
2. date_value  Date响应头的值
3. request_time 发起请求的本地时间
4. response_time 收到相应的本地时间
5. now 当前本地时间

    apparent_age = max(0, response_time - date_value);
    corrected_received_age = max(apparent_age, age_value);
    response_delay = response_time - request_time;
    corrected_initial_age = corrected_received_age + response_delay;
    resident_time = now - response_time;
    current_age   = corrected_initial_age + resident_time;

@@
### 缓存过期计算
    fressness_lifetime =
    1. 使用max-age时为max-age的秒数
    2. 使用Expires时为(Expire-Date)

    response_is_fresh = (fressness_lifetime > current_age)

@@
### 总结
1. 起点，输入url。
2. 终点，HTML字符流。
3. Http特性注定资源之间有依赖。
4. 外部资源位置，类型不同影响下载时机。
5. response.flush()对下载的影响。
6. 缓存机制。

@end