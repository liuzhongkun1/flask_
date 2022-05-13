from flask import (Flask, render_template
, request, redirect, session)

app = Flask(__name__)  # 创建一个服务器
app.secret_key = "ashdjhfcasjcvbgjs"  # 设置盐，对session信息进行加密，随机字符串
app.debug = True  # 当文件保存时，flask服务就重启
USER_DICT = {
    "1": {"name": "李华", "age": 12},
    "2": {"name": "李虎", "age": 13},
}  # 假设这个为用户数据，其为从数据库中读取出来的


@app.route('/login', methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":  # 如果请求方式为get请求
        return render_template("login.html")  # 对静态文件中的文件进行渲染
    user = request.form.get("user")  # 得到表单数据
    pwd = request.form.get("pwd")
    if user == "kun" and pwd == "123":  # 进行判断
        # 用户信息放入session中，默认放入浏览器的cookie中
        session["user_info"] = user
        return redirect("/index")  # 进行重定向
    return render_template("login.html", msg="账号或密码错误，登录失败")  # 如果登录失败，将失败信息传入前端页面中


@app.route("/detail")
def detail():
    user_info = session.get("user_info")
    if not user_info:  # 判断是否登录
        return redirect("/login")  # 如果没有登录，重定向到登录界面
    uid = request.args.get("uid")  # 获取传入的参数
    info = USER_DICT.get(uid)  # 获取人员信息
    return render_template("detail.html", info=info)  # 进行页面的渲染


@app.route("/index")
def index():
    user_info = session.get("user_info")
    if not user_info:  # 如果没有用户信息，则返回登录页面
        return redirect("/login")
    return render_template("index.html", user_dict=USER_DICT)


@app.route("/loginout")
def loginout():
    del session["user_info"]  # 删除cookies信息，进行注销操作
    return redirect("/login")  # 重定向到登录页面


@app.route("/")
def red():  # 如果直接访问的话，默认跳转到登录界面
    return redirect("/index")  # 进行url的跳转


if __name__ == '__main__':
    app.run()
