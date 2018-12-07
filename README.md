[TOC]

## 前言

[![build status](https://secure.travis-ci.org/maxcountryman/flask-login.png?branch=master)](https://travis-ci.org/#!/maxcountryman/flask-login)


用Flask框架，`SQLalchemy`,`SQlite` 和` Vertabelo` 搭建一个日程表，然后部署到`Heroku`云端。

这个并不是最终产品，目的是展示python web开发的流程


### 项目介绍

使用Flask开发一个增删改查(CRUD)应用程序:

- add/update    更新、添加一个类别
- delete/mark   标记或删除
- manage categories.    管理类别

三个视图：

1. 创建类别

![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207105951632-2058270291.png)

2. 创建待办事项

用户可以通过填写带有描述的表单，从现有优先级中选择优先级并从现有类别中选择类别来创建新待办事项。

![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207110104267-1894609166.png)

3. 管理视图

主视图列出了所有待办事项和可用类别，通过单击屏幕左侧类别菜单中的类别，将列出所选类别的待办事项列表。

![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207110154009-540803628.png)

### 技术栈

- 数据库：SQLite
- 数据库ORM：SQLAlchemy
- 路由框架：Flask
- CSS框架：Bootstrap

### Flask Web开发流程

- SQLAlchemy：获取数据库ORM对象
- Flask：Web服务器网关接口（WSGI）
- Bootstrap：组合HTML，CSS和JavaScript

> 注：ORM (Object-relational Mapping) ,关系模型映射到一个对象。pyrhon中最流行是SQLAlchemy;


![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207110341090-778186878.png)


## 一、搭建环境


### 1.1: 创建虚拟环境  

win系统
```
virtualenv venv
venv\Scripts\activate
```

### 1.2: 安装依赖包

- Flask：web骨架
- SQLAlchemy：数据库ORM框架


```
pip install Flask
pip install Flask-SQLAlchemy
```

### 1.3: 创建依赖包列表文件

`requirements.txt`
```
$ pip freeze > requirements.txt.
```

### 1.4: 测试hello word


`run.py`
```
from flask import Flask

app = Flask(__name__)

from app.views import *
if __name__ == '__main__':
    app.run()
```

`views.py`
```
from run import app
 
@app.route('/')
def index():
  return '<h1>Hello World!</h1>'
```

```
python .\run.py
```


![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181206202742061-1450095726.png)


## 二、应用程序开发

### 2.1：应用程序结构

```
|-- app/
|   |-- __init__.py
|   |-- data/
|   |   `-- todoapp.db
|   |-- models.py   # SQLAlchemy 数据库模型
|   |-- static/     #静态文件夹包含所有的CSS和JavaScript文件
|   |   |-- css/
|   |   |-- fonts/
|   |   `-- js/
|   |-- templates/  #该模板文件夹中包含Jinja2的模板
|   |   |-- layout.html
|   |   |-- list.html
|   |   |-- macros.html
|   |   |-- new-category.html
|   |   `-- new-task.html
|   `-- views.py    #视图函数
|-- config.py       #配置函数
|-- manage.py       #Flask-Script支持命令行选项
|-- readme.md       
`-- run.py  

```

### 2.2：数据库设计

业务逻辑：

- 将代办事项分类
- 待办事项按条记录在都将在todos表中
- 待办事项表将具有所需的id，description，creation_date等字段
- 代办事项有优先级，按照优先级排序

在线建模工具：[vertabelo](https://my.vertabelo.com/drive)

![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207111128548-284124233.png)


根据需求

`app\models.py`

```
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

app = Flask(__name__)
db = SQLAlchemy(app)
 
class Todo (db.Model):
    __tablename__ = "todo"
    id = db.Column('id', db.Integer, primary_key=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    priority_id = db.Column('priority_id', db.Integer, db.ForeignKey('priority.id'))
    description = db.Column('description', db.Unicode)
    creation_date = db.Column('creation_date', db.Date,default=datetime.utcnow)
    is_done = db.Column('is_done', db.Boolean, default=False)
 
    priority = db.relationship('Priority', foreign_keys=priority_id)
    category = db.relationship('Category', foreign_keys=category_id)
 
class Priority (db.Model):
    __tablename__ = "priority"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    value = db.Column('value', db.Integer)

class Category (db.Model):
    __tablename__ = "category"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
```


### 2.2：配置和初始文件

Flask-SQLAlchemy数据库URI格式：

| Database   engine  | URL                                              |
| ------------------ | ------------------------------------------------ |
| MySQL              | mysql://username:password@hostname/database      |
| Postgres           | postgresql://username:password@hostname/database |
| SQLite   (Unix)    | sqlite:////absolute/path/to/database             |
| SQLite   (Windows) | sqlite:///c:/absolute/path/to/database           |


`config.py`
```
class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/todoapp.db '
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

`app/__init__.py`

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import views, models
```

### 2.3: 创建数据库和表

- 安装`ipython`，创建初始数据库更加友好

```sh
pip install ipython
```

- 创建数据库和表。

```python
from models import db
from app.models import db
db.create_all()
```
- 插入数据分三步
    1. 创建一个Python对象
    2. 将其添加到会话中
    3. 提交会话
    
- 提交一些类别
```
from app.models import Category
work = Category(name=u'work')
home = Category(name=u'home')
db.session.add(work)
db.session.add(home)
db.session.commit()
```
- 创建优先级表
```
from models import Priority
high = Priority(name=u'high', value=3)
medium = Priority(name=u'medium', value=2)
low = Priority(name=u'low', value=1)
db.session.add(high)
db.session.add(medium)
db.session.add(low)
db.session.commit()
```

- 更多更改
```
db.session.add(object)
```
- 检查数据库

![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207103618953-224847409.png)


### 2.4：视图函数

视图函数是python脚本，接受一个http请求并返回一个http响应。此响应可以是HTML页面或重定向。

#### 2.4.1 `@app.route('/')`

- `@app.route('/')` 响应的路径
- `route`将函数注册为URL
- 函数的返回值叫做**响应**，是浏览器接收的值

`views.py`
```
from flask import render_template, request
from models import Category, Todo, Priority, db
# 列出我们按优先级值和所有类别降序排列的所有TODO项目。
@app.route('/')
def list_all():
   return render_template(
       'list.html',
       categories=Category.query.all(),
       todos=Todo.query.join(Priority).order_by(Priority.value.desc())

```

#### 2.4.2 `render_template`

Flask和Jinja2之间的集成是通过该`render_template`功能实现。

Jinja2 负责生成HTML，Flask提供模板的名称和参数作为Keyword，keyword是键值对

上面的函数中，`categories`和`todos`是在分配了当前值的模板中写入的占位符。这些当前值是从数据库中检索的准确值。


#### 2.4.3 创建代办事项

从数据库读取数据，在浏览器展现代办事项。

`@app.route('/new-task', methods=['POST'])`，函数响应一个`POST`请求

服务器从浏览器接收到POST后，将数据插入到数据库，操作成功重新定向页面；如果出现问题，将再次呈现新待办事项。

```
@app.route('/new-task', methods=['POST'])
def new():
   if request.method == 'POST':
       category = Category.query.filter_by(id=request.form['category']).first()
       priority = Priority.query.filter_by(id=request.form['priority']).first()
       todo = Todo(category, priority, request.form['description'])
       db.session.add(todo)
       db.session.commit()
       return redirect('/')
   else:
       return render_template(
           'new-task.html',
           page='new-task',
           categories=Category.query.all(),
           priorities=Priority.query.all()
       )
```
#### 2.4.4 更新代办事项

`@app.route('/<int:todo_id>', methods=['GET', 'POST'])`

`GET`:服务器收到浏览器`GET`请求，渲染模板，并检索数据库追加给新的页面
`POST`:如果浏览器输入值，服务器将更新数据库

浏览器
```
@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
   todo = Todo.query.get(todo_id)
   if request.method == 'GET':
       return render_template(
           'new-task.html',
           todo=todo,
           categories=Category.query.all(),
           priorities=Priority.query.all()
       )
   else:
       category = Category.query.filter_by(id=request.form['category']).first()
       priority = Priority.query.filter_by(id=request.form['priority']).first()
       description = request.form['description']
       todo.category = category
       todo.priority = priority
       todo.description = description
       db.session.commit()
       return redirect('/')
```

#### 2.4.5 视图完整代码

`app/views.py`
```python

from flask import render_template, request, redirect, flash,url_for
from app.models import Category, Todo, Priority, db
from app import app

@app.route('/')
def list_all():
    return render_template(
        'list.html',
        categories=Category.query.all(),
        todos=Todo.query.all(),#join(Priority).order_by(Priority.value.desc())
    )


@app.route('/<name>')
def list_todos(name):
    category = Category.query.filter_by(name=name).first()
    return render_template(
        'list.html',
        todos=Todo.query.filter_by(category=category).all(),# .join(Priority).order_by(Priority.value.desc()),
        categories=Category.query.all(),

    )


@app.route('/new-task', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        #priority = Priority.query.filter_by(id=request.form['priority']).first()
        #todo = Todo(category=category, priority=priority, description=request.form['description'])
        todo = Todo(category=category, description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('list_all'))
    else:
        return render_template(
            'new-task.html',
            page='new-task',
            categories=Category.query.all(),
            #priorities=Priority.query.all()
        )


@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'new-task.html',
            todo=todo,
            categories=Category.query.all(),
            #priorities=Priority.query.all()
        )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        #priority = Priority.query.filter_by(id=request.form['priority']).first()
        description = request.form['description']
        todo.category = category
        #todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect('/')


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-category.html',
            page='new-category.html')


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template(
            'new-category.html',
            category=category
        )
    else:
        category_name = request.form['category']
        category.name = category_name
        db.session.commit()
        return redirect('/')


@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        if not category.todos:
            db.session.delete(category)
            db.session.commit()
        else:
            flash('You have TODOs in that category. Remove them first.')
        return redirect('/')


@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')


@app.route('/mark-done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        todo.is_done = True
        db.session.commit()
        return redirect('/')
```




### 2.5：模板

#### 2.5.1 模板简介

模板能使前后端分开，是包含响应的HTML文件；文件包含的变量仅在请求的上下文有效；通过Jinja2模板引擎渲染

[Jinja2模板引擎官网](http://jinja.pocoo.org/docs/dev/)

2种分隔符：

- {{ variable }}  用于变量
- {% control structures %} 用于控制结构

#### 2.5.2 解析一个视图函数：

在主页上显示类别和代办事项,

为了获得所有类别和TODO，用for语句`{% ... %}`和特定类别的块内循环迭代，显示其名称。

```
@app.route('/')
def list_all():
   return render_template(
       'list.html',
       categories=Category.query.all(),
       todos=Todo.query.join(Priority).order_by(Priority.value.desc())
```
相应的模板如下所示。

```
<h3>Category</h3><font></font>
    <table><font></font>
    {%- for category in categories %}<font></font>
        <tr><font></font>
            <td>{{ category.name }}</td><font></font>
        </tr><font></font>
    {%- endfor %}<font></font>
</table><font></font>
```

#### 2.5.3 模板继承

在主页顶部有一个导航栏，其中包含指向`create_category`页面`和create_todo`页面以及页脚的链接。我希望在每个页面上重复这些组件。为了在所有页面上保留公共元素，我将使用模板继承。

继承是块控制语句。在此结构中，您可以定义派生模板可以插入其内容的位置。

layout.html负责一般结构。extends块建立三个模板之间的继承（它用于从另一个模板扩展模板）。
![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207105843378-429242058.png)

### 2.6：Bootstrap美化Web应用

Bootstrap是最流行的Web开发前端框架。

#### 2.6.1 下载插件

下载Bootstrap，解压到`/static`

[Bootstrap](https://getbootstrap.com/docs/3.3/components/)教程

[Navbar](https://getbootstrap.com/docs/3.3/components/)图标元素

#### 2.6.2 `Layout.html`基本模板


`layout.html`是其余模板的基本布局。用navbar元素构建一个漂亮的导航栏，`container-fluid`使页面全屏


```
Menu
<nav class="navbar navbar-inverse">
<div class="container-fluid">
<div class="navbar-header">
    <a class="navbar-brand" href="/">TODOapp</a>
</div>
            <ul class="nav navbar-nav">
            <li><a href="/new-task">New TODO</li>
            <li><a href="/new-category">New category</li>     
            </ul>
</div>
</nav>
 
<div class="container-fluid">
Messages
</div>
 
<div class="container-fluid">
    Footer
</div>
```
#### 2.6.3 `List.html`

`List.html`负责列出TODO和类别。此模板继承自layout.html。在这里，我添加了Bootstrap网格系统。

默认情况下，网格系统最多可扩展到12列，可以更改为四个设备(大屏台式机，台式机，平板电脑和手机) 。

由于每行有12个单元，我制作了两列，一个是3个单元，第二个是9个单元。

网格系统要求将行放在`.container`或`.container-fluid`中以进行正确的对齐和填充。

[Bootstrap网格系统的更多信息](https://scotch.io/tutorials/understanding-the-bootstrap-3-grid-system)

#### 2.6.4 基本结构

要创建布局：

- 创建一个容器 `<div class="container">`
- 创建一行 `<div class="row">`
- 在一行中添加所需的列数。

结构如下：

```
<div class="container">
    <div class="row">
        <div class="col-md-2">Table with categories</div>
        <div class="col-md-10">Table with TODOs</div>
    </div>
</div>
```

#### 2.6.5 `new-task.html`

使用自定义的`.selectpicker` 对类别表单和优先级表单进行简单的选择

- 下载[Bootstrap-select](http://silviomoreto.github.io/bootstrap-select/)，解压到`/static`
- 在`layout.html`启用  Bootstrap-Select via JavaScript
    ```
    $('.selectpicker').selectpicker();
    ```
## 三 、验证

```
python .\run.py
```
![](https://img2018.cnblogs.com/blog/720033/201812/720033-20181207105554370-1483268868.png)
