Title: 比价接口分享
Tags: 
Category: 
Type: 1

@
@@
## 比价接口分享

@
@@
## 比价接口做什么？

@@
### 1. 展示多个合作方的订座信息
### 并按照我们制定的策略排列

@@
### 2. 根据来源展示不同的策略。
### 目前支持pc，WebView，Webapp

@
@@
## 过程

@@

1. 数据判重入库
2. 获取数据
3. 数据格式化
4. 数据过滤
5. 数据合并

@
@@
## 数据判重入库

@@
## 使用百度视频的服务
#### [怪兽大学](http://open.video.baidu.com:8088/v?wd=%E6%80%AA%E5%85%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&fr=lbs&token=1e4d864207b1a3ee64271dd2ddcb64ee)
#### [视频线上效果](http://v.baidu.com/v?word=%B9%D6%CA%DE%B4%F3%D1%A7&ct=301989888&rn=20&pn=0&db=0&s=0&fbl=800)

@@
## 代码

        private function get_from_video($name) {
            // 成功返回video_id的md5
            // 失败返回名字的md5
            // 之后根据返回值做merge，认为id相同的电影相同。
            if(array_key_exists($name, $this->names)){
                $name = $this->names[$name];
            }

            $url = $this->get_api_url($name);
            $content = $this->get_content($url);
            $data = json_decode($content, TRUE);
            $status = $data['status'];
            $video_id = md5($name); // 缺省值为md5(name)

            if (!$status == "200") {
                return $video_id;
            }

            // 找到第一个type是movie的影片返回
            foreach($data['rsp']['list'] as $data){
                if($data['video_type'] == "movie"){
                    $video_id = md5($data['id']);
                    break;
                }
            }
            return $video_id;
        }

@@
## 还不能判重怎么办？

@@
## 上线rename.conf人工修正

    [data]
    [.name]
    from:侏罗纪公园（3D版）
    to:侏罗纪公园

    [.name]
    from:摩登时代
    to:摩登年代

    [.name]
    from:西柏坡2 英雄王二小
    to:西柏坡2：英雄王二小

    [.name]
    from:西柏坡2——英雄王二小
    to:西柏坡2：英雄王二小

@
@@
## 获取数据

@@
### 通过di接口获取instant_flags, 直接从库里取数据

@@
### 存在的问题以及如何优化
1. Redis数据不一致，造成数据获取不稳定。
2. 可以并发。
3. 可以根据参数过滤部分来源。

@
@@
## 数据格式化

@@
## 通用格式化

    $timetable = array(
        "lan" => $lan,
        "time" => $time,
        "date" => $date,
        "type" => $type,
        "price" => $price,
        "theater" => $theater,
        "origin_price" => $origin_price,
        "movie_id" => $video_id, // 用于判重
        "url" => $url,
        "wap_url" => $wap_url,
        "cinema_id" => $cinema_id,
        "third_id" => $third_id, // 第三方id，用于购票
        "src_name" => Info_Price_Third::get_third_name($third_from),
        "seq_no" => $seq_no,
    );

@@
## 定制化需求
#### 比如万达需要做时间处理，万达的特价活动。

    // 寻找是否有各来源的定制化方法
    if (method_exists(__CLASS__, $third_from)) {
        $result = self::$third_from($item);
    }else{
        $result = self::common($item);
    }

@@
## 处理之后的结果
    movies: {
        wanda: [],
        wangpiao: [],
        gewala: [],
        maizuo: [...],
        spider: [...],
        dbmovie: [],
        mtime: []
    },
    timetables: {
        wanda: [],
        wangpiao: [],
        gewala: [],
        maizuo: [...],
        spider: [...],
        dbmovie: [],
        mtime: []
    }

@
@@
## 数据过滤

@@
## 干什么?
1. 过滤掉过期的时间。
2. 根据PM需求，过滤掉一些数据。
3. 根据来源，过滤掉一些数据。

@@
## 代码
    $result = $this->check_datetime($data);
    $result = $this->only_wanda($result);

    if($send_from != "pc"){
        // 只有PC端的请求展示maizuo
        $result = $this->filter_maizuo($result);
        $result = $this->filter_spider($result);
    }

    if($send_from == "webview" || $send_from == "webapp"){
        $result = $this->show_info($result);
    }else{
        $result = $this->only_price($result);
    }
    return $result;

@@
## 过滤之后的结果
    movies: {
        wanda: [],
        wangpiao: [],
        gewala: [],
        maizuo: [...],
        spider: [...],
        dbmovie: [],
        mtime: []
    },
    timetables: {
        wanda: [],
        wangpiao: [],
        gewala: [],
        maizuo: [...],
        spider: [],
        dbmovie: [],
        mtime: []
    }

@
@@
## 整合

@@
## 做什么？
1. 不同来源的数据整合。
2. 根据策略对数据排序。

@@
## 合并的过程
    $video_id = $timetable['movie_id'];
    $date = $timetable['date'];
    $time = $timetable['time'];
    $key = sprintf("%s&&%s&&%s",  $date, $time, $video_id);
    $timetable['src'] = $src;
    if (array_key_exists($key, $container)){
        array_push($container[$key], $timetable);
    }else{
        $container[$key] = array($timetable);
    }

@@
## 排序的过程

    private function sort($a, $b){
        $price_a = empty($a['price']) ? 100000 : floatval($a['price']);
        $price_b = empty($b['price']) ? 100000 : floatval($b['price']);

        if ($price_a != $price_b){
            // 价格不相等，优先展示价格低的
            return $price_a < $price_b ? -1: 1;
        }else{
            // 价格相等，比较来源优先级
            $priority_a = $this->DISPLAY_PRIORITY[$a['src']];
            $priority_b = $this->DISPLAY_PRIORITY[$b['src']];
            if ($priority_a == $priority_b){
                return 0;
            }else{
                // 优先级大的排在前面
                return $priority_a > $priority_b ? -1 : 1;
            }
        }
    }

@@
## [最后的结果](http://yf-map-other02.yf01.baidu.com:8111/info/api/price?uid=d480a7cfffd171b4e5073800)

@
@@
## 如何做到只需要配置？

@@
### 所有的数据从配置文件中读就可以了

    [.third]
    name: wanda
    alias: 万达电影
    seat: 1
    display: 4
    merge: 16

    [.third]
    name: wangpiao
    alias: 网票网
    seat: 1
    display: 64
    merge: 64

    [.third]
    name: gewala
    alias: 格瓦拉
    seat: 1
    display: 8
    merge: 32

@
@@
## Q&A

@end

