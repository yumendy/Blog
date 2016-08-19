## 段喵的自用博客

### 简介

一直以来都有一个做自己博客的梦想。告别了WordPress果断的自己写了一个属于自己的博客。

自己用的博客，感觉最重要的莫过于用方便定制和用的开心。

所以在设计这个博客的时候花了很多的心血，在思考该怎么去设计一套耦合小，而且易于添加和删除功能的博客呢？

最后整个博客都是用组件化的方式完成的，这样最大的好处莫过于可以每次开发一个组件，而且不会影响到其他功能的使用。

与其说是设计了一套博客，不如说是制定了一套规范。在设计模式的选择上使用的是组合模式，归功于Python的多继承，可以很简单的完成这个工作。

后面会详细介绍该如何开发一个自己的博客组件并将其挂入这套博客系统。

本博客使用了`Djangoueditor`和`qiniustorage`两个开源项目，特此感谢。

为了速度考虑，所有静态文件和媒体文件都托管在七牛云上。

### 安装与部署

* python 2.7

依赖包(使用pip安装)：

* Django 1.10
* markdown
* qiniu
* qiniustorage

安装完依赖之后需要在Blog子目录下创建一个`local_settings.py`文件，里面包含如下内容：

```python
DB_USER = '' # 数据库用户名
DB_PASSWORD = '' # 数据库密码
QN_ACCESS_KEY = '' # 七牛的ACCESS_KEY
QN_SECRET_KEY = '' # 期内的SECRET_KEY
debug = True
```

数据库使用的是mysql，需要建立一个名为`yumendy_blog`的库，当然你也可以在settings里自己设置。

配置完成后可以使用`python manage.py createsuperuser`命令创建超级管理员。

同步数据库：

```bash
python manage.py makemigrations
python manage.py migrate
```

你可以直接克隆下来这个项目然后执行`python manage.py runserver`就可以了。

如果要部署在生产环境，可以使用nginx+uwsgi的部署方式，配置文件可以参考`blog.conf`和`blog.xml`

### 组件简介

* **article：** 文章模块，内含3个基本类，文章分类、博客和静态文章。文章分类用于目录。静态文章可以用来做一些介绍性页面。不会被和博客一起排在目录列表中。
* **authentication：** 认证模块，用于用户登录和登出，可以在此处对原有用户模块进行拓展。
* **link：** 友链模块，可以添加友情链接。
* **mood：** 碎碎念模块，包括一个时间轴可以在`/mood/timeline/`中查看。
* **navbar：** 导航栏模块，可以自定义展示的标签和顺序。

### 二次开发

完全组件化的架构设计就是为了方便往项目里添加组件，下面我将以mood模块为例讲讲该如何为这个blog添加一个组件。

#### 创建一个模块

1. 可以使用`python manage.py startapp mood`来新建碎碎念模块。
1. 在目录中额外创建`urls.py`和`mixin.py`两个文件备用。
1. 在`Blog/urls.py`的`urlpattern`中加入`url(r'^mood/', include('mood.urls'))`。
1. 在`Blog/settings.py`的`INSTALLED_APPS`中加入`'mood.apps.MoodConfig'`

#### 编写数据模型

1. 在mood/models.py中书写数据模型。
1. 在mood/admin.py中注册数据模型。

#### 编写视图处理函数

1. 编写MoodCreateView，MoodListView，MoodUpdateView，MoodDeleteView四个视图处理函数，注意这四个函数是用于后台界面，LoginRequiredMixin。其次，由于后台使用的都是ajax异步请求，所以需要添加AjaxableResponseMixin继承。对于ListView是一个展示视图，所以无需添加AjaxableResponseMixin。
1. 完成timeline视图，用于前段展示页面，需要继承FrontMixin，无需添加LoginRequiredMixin。

#### 编写url映射

1. 在urlpatterns中添加对应的url映射即可。

#### 编写模板文件

1. 完成后端模板文件，在templates文件夹里建立一个名为mood的文件夹。
1. 创建一个名为`mood_nav.html`的文件，用于作为后台导航栏，填写如下内容即可：
    ```html
    <ul class="nav nav-sidebar">
       <li id="mood-list"><a href="{% url 'mood-list' %}">碎碎念-列表</a></li>
       <li id="mood-add"><a href="{% url 'mood-add' %}">碎碎念-添加</a></li>
       <li id="mood-update"><a href="{% url 'mood-list' %}">碎碎念-更新</a></li>
    </ul>
    ```
    在templates/website/backend/nav.html中加入`{% include 'mood/mood_nav.html' %}`
1. 编写`mood_create_form.html`,`mood_update_form.html`,`mood_list`三个文件。在block的js中加入对应的提交方法，具体请参考其他项目。
1. 编写时间轴页面`mood_time_line.html`，继承模板`'website/frontend/frontend_base.html'`在block的external_header中加入独有的静态文件。left中可以加入article类以获取与其他模块一样的区块效果。
1. 编写侧边栏挂件`mood_weight.html`,直接写一个bootstrap的格就可以，添加article类以保证显示效果一致。
1. 修改`mixin.py`编写需要传递给侧边栏挂件的数据。
    ```python
    from models import Mood
    
    
    class LeastMoodMixin(object):
        def get_context_data(self, *args, **kwargs):
            context = super(LeastMoodMixin, self).get_context_data(*args, **kwargs)
            if Mood.objects.count() > 0:
                context['mood'] = Mood.objects.all()[0]
            else:
                pass
            return context
    ```
    这样就写好了一个插件所需要的mixin。
1. 把组件加入视图。修改`website/mixin.py`给`FrontMixin`类加一个LeastMoodMixin的继承即可。

至此，一个组件就开发完惹。

### 写在最后

这个博客项目酝酿了很久，终于算是完全完成了。开源出来也是为了可以让更多的人了解python-web的开发。同时也算是为开源事业做出一点微小的贡献。如果你觉得这个项目不错，不妨donate我一下w *支付宝* 账号：**yumendy@163.com**。

### 联系方式

* Email: yumendy@163.com
* QQ: 306359430

### 更新日志

2016-8-19

* 加入了rss-feed功能。

2016-8-18

* 第一次发布
