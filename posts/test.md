Title: 这是自动生成的
Tags: django
Category: 后端技术


## 什么是面向切面编程？
面向切面编程, Aspect Oriented Programming(AOP)。主要实现的是将业务逻辑处理过程以切面为维度进行提取，它所面对的是处理过程中的某个步骤或阶段，以获得逻辑过程中各部分之间低耦合性的隔离效果。也就是说，**在不修改函数A的前提下**，在函数A前后插入业务逻辑B, C, D..
<!--more-->


## 基于Python Decorator的切面编程
Python的decorator功能很强大，它能在<font color="red">**运行期间拿到函数的上下文**</font>，并且赋予你足够的权限去做很多事情。这恰恰符合面向切面编程的设计方式，你可以通过decorator方便的实现这个功能。


直接上代码：



**func_section decorator代码**

    def func_section(before_chain=[], after_chain=[]):
      def func_wrap(func):
        def wrap(*args, **kwargs):
          for before_func in before_chain:
            try:
              before_func(*args, **kwargs)
            except Exception:
              continue
          res = func(*args, **kwargs)

          for after_func in after_chain:
            try:
              after_func(*args, **kwargs)
            except Exception:
              continue
          return res
        return wrap
      return func_wrap


** 如何使用？**


    def example():
      def before_saying(self):
        print("I know your name %s" % self.name)

      def before_saving(self):
        print("I will notify your name %s" % self.name)

      def after_saving(self):
        print("After saving your name %s " % self.name)

      def done(self):
        print("Everything is ok %s " % self.name)

      class FuncTest():
        def __init__(self, name):
          self.name = name

        def __i_know_you(self):
          print("I know you guy %s " % self.name)

        @func_section(before_chain=[__i_know_you,
            before_saying, before_saving],
            after_chain=[after_saving, done])
        def save(self):
          print("Save name %s " % self.name)
          return self.name

      test = FuncTest(name=u'chenchiyuan')
      print(test.save())

    >>> example()
    I know you guy chenchiyuan
    I know your name chenchiyuan
    I will notify your name chenchiyuan
    Save name chenchiyuan
    After saving your name chenchiyuan
    Everything is ok chenchiyuan
    chenchiyuan



## 看了这么多，它能干什么？
<font color="red">**它的作用就是减少你的代码的耦合度**</font>


还不明白？我来举个最简单的例子。


现在有个函数叫做eat()，业务逻辑就是饿了要吃饭，而且已经很多地方调用它了。现在我有个需求，在每次吃饭之前我要吃点开胃菜before_eat()，吃饭之后，我要刷牙洗口after_eat()。怎么实现呢？


#### 1. 懒人的方法
管它三七二十一，直接修改eat(), 先加上before_eat(), 再加上after_eat()。


评价：确实完成了功能。但是违反了[开闭原则](http://baike.baidu.com/view/866233.htm)，而且函数耦合性很高，如果以后添加了更多需求，这段代码会臃肿不堪，业务逻辑复杂到一定规模的时候，你就祈祷神来解决你吧。


#### 2. 最笨的方法
全文搜索，找出所有用到eat()的地方，前面加上before_eat(),后面加上after_eat()。


评价：违反了[封装原则](http://baike.baidu.com/view/154910.htm#2)，这一系列操作对外应该是不可见的。我都懒得评价了。。


#### 3. 优雅的方法
使用面向切面编程的方法。
```
def before_eat():
    print(u'吃开胃菜')

def after_eat():
    print(u'刷牙')

@func_section(before_chain=[before_eat, ], after_chain=[after_eat, ])
def eat():
    print(u'吃饭')
```
这样，以后业务逻辑增加了，只需要将原子的业务逻辑加入函数执行链中即可。体验到它的强大了吧？



## 题外话
#### 1. Django中有没有类似的方式？
肯定是有的，最接近的其实是signal的实现。把model.save()比喻成eat(), 那么你可以通过Django自带的before_save, after_save来实现在save的切面前后添加业务逻辑。这样做远远比你重写save方法好得多。


#### 2. 还有什么注意的东西？
顺便提提对象的方法实现。instance.do_something(*args, **kwargs)。在切面编程拿到的形式是do_something(instance, *args, **kwargs)。这其实就是面向对象的最核心的实现技巧。