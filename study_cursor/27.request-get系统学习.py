"""
requests 库常用用法示例（GET 为主，顺带演示其它常见用法）

【整体说明：如果你是完全小白，建议这么学】
1. 把这个文件从上往下简单看一遍，大致知道有哪几种用法。
2. 到下面的 main() 函数里，只保留一个你想看的函数，比如 basic_get()，然后运行文件，观察输出。
3. 对着输出 + 注释，慢慢体会“我发了什么 → 服务器收到了什么 → 返回了什么”。
4. 每次只学一个小点，比如“今天只搞懂 GET 带参数”，别一次性全记住，容易晕。

【这个文件里都演示了什么】
- 最简单 GET：只传一个网址过去，看服务器返回什么。
- GET 带参数：给网址后面加 ?key=value 的那种请求。
- 自定义请求头：比如伪装浏览器、带 token 等。
- 响应常用属性：状态码、最终 URL、响应头、文本内容、二进制内容、json() 等。
- 超时和异常处理：网不好时怎么避免程序一直卡着，怎么优雅打印错误。
- cookies：模拟浏览器那种“登录一次，后面自动携带登录状态”。
- Session：在多次请求之间“复用”连接和 cookies。
- POST 表单：传统网页登录表单那种请求方式。
- POST JSON：现在大部分接口都用的方式。
- 上传文件：上传头像、附件之类的场景。
- 其它 HTTP 方法：PUT / DELETE 等 REST 接口常用方法。

【关于 httpbin 网站】
- 我们统一使用 `https://httpbin.org` 这个专门用来练习 HTTP 的测试网站。
- 你发什么参数、请求头、cookies 给它，它就会原样再“回显”给你，方便你确认自己到底发出去的是什么。
"""

import json  # 用于演示手动处理 json
import requests  # 第三方 HTTP 库，需要先：pip install requests
from requests import RequestException  # requests 的异常基类


def basic_get():
    """
    最基础的 GET 请求

    场景（真实世界类比）：
    - 就像你在浏览器地址栏里直接输入一个网址，然后按回车。
    - 浏览器会帮你发一个“最普通的 GET 请求”，把网页内容拿回来展示给你。

    在代码里，我们做的事情是：
    1. 准备一个网址（url 字符串）。
    2. 用 requests.get(url) 把这个网址“访问”一下。
    3. 把服务器返回的“状态码、最终地址、部分头信息、正文内容”打印出来。

    关键点：
    - 这里只传了 url，没有额外参数（params）和请求头（headers），属于最简版用法。
    - 通过这个例子，你要认识 Response 对象上最常用的这几个属性：
      - status_code：请求结果是否成功的“信号灯”。
      - url：最终访问到的真实地址（有时会被重定向）。
      - headers：服务器返回的一些“元信息”（比如返回的是 JSON 还是 HTML）。
      - text：服务器返回的“正文内容”（已经帮你解码成字符串）。
    """
    # 要请求的目标地址（注意：必须以 http:// 或 https:// 开头，否则是无效网址）
    # 这里的 /get 是 httpbin 网站提供的一个“调试接口”，它不会真正做什么业务，只是把你发过去的信息再原样返回。
    url = "https://httpbin.org/get"

    # 第 1 步：发请求
    # 直接发送最简单的 GET 请求：只传一个 url。
    # requests.get(...) 会帮你：
    # - 建立网络连接
    # - 把 GET 请求发出去
    # - 把服务器返回的数据封装到一个 Response 对象里，然后返回给你
    resp = requests.get(url)

    print("【basic_get】")
    # 第 2 步：看结果 —— 状态码
    # resp.status_code：HTTP 状态码，常见含义：
    # - 200：成功
    # - 404：你访问的地址不存在（Not Found）
    # - 500：服务器内部错误（Internal Server Error）
    print("状态码：", resp.status_code)
    # 第 3 步：看结果 —— 最终 URL
    # resp.url：服务器最终处理的 URL（如果中间有跳转，这里会显示跳转后的地址）
    print("最终请求的 URL：", resp.url)
    # 第 4 步：看结果 —— 响应头
    # resp.headers：一个“类似字典”的对象，保存所有响应头信息。
    # 这里我们只拿一个最常用的字段：Content-Type（内容类型），看服务器返回的是：
    # - application/json（一般表示返回的是 JSON 数据）
    # - text/html（一般表示返回的是网页 HTML）
    print("部分响应头：", resp.headers.get("Content-Type"))
    # 第 5 步：看结果 —— 文本正文
    # resp.text：把响应体按正确的编码（比如 utf-8）解码成字符串。
    # 为了避免一次性打印太多，只截取前 100 个字符给你看一个大概。
    print("文本响应正文前 100 个字符：", resp.text[:100])
    print("-" * 60)


def get_with_params():
    """
    GET 携带查询参数（?key=value）

    场景（真实世界类比）：
    - 你在网站上“搜索商品”、“按条件筛选数据”、“翻页查看下一页列表”时，
      浏览器其实会在网址后面加上一堆 ?key=value&key2=value2 这样的内容。

    在代码里，我们做的事情是：
    1. 把这些“搜索条件 / 分页参数”放进一个 Python 字典里。
    2. 把这个字典通过 params= 传给 requests.get()。
    3. requests 会自动帮你把字典转成查询字符串拼到 URL 后面。

    关键点：
    - params 参数一定是一个“普通的 Python 字典”。
    - 最终实际访问的 URL 可以通过 resp.url 看到，非常直观。
    """
    url = "https://httpbin.org/get"  # 依旧使用 httpbin 的 /get 接口进行演示

    # params：查询参数字典，会被自动编码到 URL 查询字符串中。
    # 什么是“查询字符串”？就是在 URL 后面用 ? 开头，多个 key=value 用 & 连接的那段内容。
    # 例如最终会变成类似这样：
    # https://httpbin.org/get?name=侯金双&city=广东&page=1&size=10
    params = {
        "name": "侯金双",  # 普通字符串参数
        "city": "广东",  # 非 ASCII 字符（比如中文）会被自动进行 URL 编码，你不用手动处理
        "page": 1,  # 数字也可以，requests 会自动转为字符串
        "size": 10,  # 一般分页时用于“每页条数”
    }

    # 发送 GET 请求时，把 params=... 传进去即可，其他用法和最简单的 GET 完全一样
    resp = requests.get(url, params=params)

    print("【get_with_params】")
    # 最终 URL 中会包含编码之后的查询参数（你可以把这一行输出复制到浏览器里打开试试）
    print("最终 URL：", resp.url)
    # httpbin 会把“它解析出来的查询参数”放到 json 结果中的 args 字段里。
    # resp.json()：把响应体按 JSON 格式解析成 Python 字典：
    # - 用的时候就把它当成普通的 dict 操作就行，比如 data["args"]
    # - 如果服务器不是返回的 JSON（比如返回的是 HTML），这里会抛异常（ValueError）。
    print("JSON 形式返回的数据：", resp.json())
    print("-" * 60)


def get_with_headers():
    """
    GET 自定义请求头（headers）

    场景：
    - 模拟浏览器访问，需要带特定的 User-Agent
    - 调某些接口需要在请求头里带 Token / 版本号等信息
    """
    url = "https://httpbin.org/get"  # 依旧使用 /get 接口

    # 常见的自定义请求头写在一个普通字典里即可
    headers = {
        # User-Agent：告诉服务器“我是哪个客户端”，很多网站会根据这个做适配或限制
        "User-Agent": "MySimpleClient/1.0",
        # Accept：告诉服务器“我希望你返回哪种类型的数据”，比如 application/json、text/html 等
        "Accept": "application/json",
    }

    # 把 headers=... 传给 get 方法即可，requests 会自动带上这些请求头
    resp = requests.get(url, headers=headers)

    print("【get_with_headers】")
    # 本地打印一下我们设置的 User-Agent
    print("请求头中 User-Agent：", headers["User-Agent"])
    # httpbin 会把它“看到的请求头”放到 json 里的 headers 字段中，方便我们对比验证
    print("服务器看到的 headers（部分）：", resp.json().get("headers"))
    print("-" * 60)


def response_common_attrs():
    """
    常用响应属性演示：
    - status_code：状态码
    - ok：是否 200~399
    - url：最终访问地址
    - headers：响应头
    - text：按编码解码后的字符串
    - content：原始字节
    - json()：按 JSON 解析后的 Python 对象
    """
    url = "https://httpbin.org/get"
    # 这里额外带一个简单的查询参数 q=python，方便在结果中观察
    resp = requests.get(url, params={"q": "python"})

    print("【response_common_attrs】")
    # 状态码：int 类型，例如 200 / 404 / 500 等
    print("状态码：", resp.status_code)
    # resp.ok：requests 帮我们做的一个“语法糖”，200~399 返回 True，其它返回 False
    print("是否请求成功（requests 自带判断）：", resp.ok)
    # 最终访问的 URL，包含查询字符串
    print("最终 URL：", resp.url)
    # 响应头是一个类似字典的对象，包含服务器返回的各种元信息
    print("响应头：", resp.headers)
    # text：把响应体按推断出来的编码（或指定 encoding）解码成字符串
    print("文本内容 text（str）：", type(resp.text), resp.text[:80])
    # content：原始的字节数据，适合下载图片、文件等二进制内容
    print("二进制内容 content（bytes）：", type(resp.content), resp.content[:20])

    # 如果确定返回的是 json，可以直接 resp.json() 得到 Python 对象（通常是 dict）
    data = resp.json()
    print("json() 解析后类型：", type(data))
    # httpbin 会把解析到的查询参数放到 args 字段里，这里可以看到 {"q": "python"}
    print("json() 中 args 字段：", data.get("args"))
    print("-" * 60)


def get_timeout_and_error():
    """
    设置超时时间 + 基本异常处理

    场景：
    - 真实开发中，网络情况不稳定，有时候接口半天不返回。
    - 如果你不设置超时，程序可能会一直等，感觉像“卡死了”。
    - 所以我们要：
      1. 给请求设置一个“最长等待时间”（timeout）。
      2. 如果超时或其它错误发生，用 try/except 把它优雅地捕获并打印出来。
    """
    # /delay/3：httpbin 提供的一个接口，会故意延迟 3 秒再返回响应
    url = "https://httpbin.org/delay/3"

    try:
        # timeout=1 表示：
        # - 最多只愿意为这次请求等待 1 秒钟。
        # - 如果 1 秒内没连上 / 没拿到响应，就会抛出 requests.Timeout 异常。
        # 注意：timeout 控制的其实是“连接 + 读取”的时间，而不是程序总运行时间。
        resp = requests.get(url, timeout=1)
        print("【get_timeout_and_error】")
        print("请求成功，状态码：", resp.status_code)
    except requests.Timeout:
        # 捕获超时错误
        print("【get_timeout_and_error】请求超时（Timeout）")
    except RequestException as e:
        # 所有 requests 的异常基类，兜底处理
        print("【get_timeout_and_error】请求出错：", e)
    print("-" * 60)


def get_with_cookies():
    """
    发送和读取 cookies

    场景：
    - 模拟浏览器登录后带上 sessionid 等 cookie 访问页面
    - 有些简单接口会直接把用户信息放在 cookie 里
    """
    # httpbin 的 /cookies 接口会把它“看到的 cookies”原样返回，适合用来测试
    url = "https://httpbin.org/cookies"

    # cookies 参数同样传入一个字典即可，每个键值对就是一个 cookie 项
    cookies = {
        "sessionid": "abc123",  # 模拟一个 session id
        "user": "hjs",  # 模拟一个用户名
    }

    resp = requests.get(url, cookies=cookies)

    print("【get_with_cookies】")
    print("服务端返回的 cookies 字段：", resp.json().get("cookies"))
    print("-" * 60)


def use_session():
    """
    使用 Session 复用连接、自动携带 cookies

    场景：
    - 登录一次后，后续所有请求都自动带上 cookie / headers
    - 与服务器保持长连接，减少握手开销（比每次 new 一个 requests.get 更高效）
    """
    # Session 对象可以在多个请求之间共享：cookies、部分 headers、连接等
    session = requests.Session()

    # 为整个 session 设置默认请求头：之后 session.get / post 都会自动带上这个 User-Agent
    session.headers.update({"User-Agent": "SessionClient/1.0"})

    # 第一次请求：访问一个专门“设置 cookie”的接口，相当于登录行为
    session.get("https://httpbin.org/cookies/set?token=hello")

    # 第二次请求：查看当前携带的 cookie（注意，这里我们没有手动传 cookies 参数）
    resp = session.get("https://httpbin.org/cookies")

    print("【use_session】")
    print("Session 自动携带的 cookies：", resp.json().get("cookies"))
    print("-" * 60)


def post_form_data():
    """
    POST 表单（application/x-www-form-urlencoded）

    场景：
    - 传统网页表单提交，比如登录表单、注册表单
    - 很多老接口默认就是这种格式
    """
    url = "https://httpbin.org/post"  # httpbin 的 /post 接口会把各种请求体原样返回

    # data 字典会自动编码为 application/x-www-form-urlencoded 表单格式
    data = {
        "username": "hjs",  # 表单中“用户名”字段
        "password": "123456",  # 表单中“密码”字段（这里只是演示，真实场景不要明文）
    }

    resp = requests.post(url, data=data)

    print("【post_form_data】")
    json_data = resp.json()
    print("form 字段（服务器解析出来的表单数据）：", json_data.get("form"))
    print("-" * 60)


def post_json_data():
    """
    POST JSON 数据（application/json）

    场景：
    - 现在大部分“前后端分离”的接口，都约定用 JSON 来传输数据。
    - 你可以把 JSON 简单理解为“带双引号的字典格式”，前后端都能看懂。
    - 后端框架（Django / Flask / FastAPI 等）一般都会提供 request.json() 这种 API 来读取 JSON 请求体。
    """
    url = "https://httpbin.org/post"

    # 准备要发送的 Python 字典（requests 会帮我们把它“序列化”为 JSON 字符串）
    payload = {
        "name": "侯金双",  # 普通字符串字段
        "age": 18,  # 数字字段
        "skills": ["python", "requests"],  # 列表字段
    }

    # 使用 json= 参数更方便，requests 会自动：
    # 1. 把字典转成 JSON 字符串
    # 2. 加上 Content-Type: application/json 请求头
    resp = requests.post(url, json=payload)

    print("【post_json_data】")
    print("请求体（服务器看到的 json）：", resp.json().get("json"))

    # 等价的写法：手动 dumps + 指定 headers
    resp2 = requests.post(
        url,
        data=json.dumps(payload),  # 手动把字典转成 JSON 字符串
        headers={"Content-Type": "application/json"},
    )
    print("等价写法的 json 字段：", resp2.json().get("json"))
    print("-" * 60)


def file_upload_example():
    """
    演示文件上传（multipart/form-data）

    场景：
    - 常见的“上传头像”、“上传附件”等功能
    - 表单中既有普通字段，又有文件字段
    说明：
    - 这里只演示构造 files 参数的方式，不依赖真实文件，方便你直接运行
    """
    url = "https://httpbin.org/post"

    # 一般写法是：
    # with open("test.txt", "rb") as f:
    #     files = {"file": ("test.txt", f, "text/plain")}
    #     resp = requests.post(url, files=files)
    #
    # 这里用内存中的 bytes 模拟一个“文件”，避免必须存在真实文件
    # 第一个元素是文件名，第二个是二进制内容，第三个是 MIME 类型
    files = {
        "file": ("hello.txt", b"hello world", "text/plain"),
    }

    resp = requests.post(url, files=files)

    print("【file_upload_example】")
    print("服务器解析出的 files 字段：", resp.json().get("files"))
    print("-" * 60)


def other_http_methods():
    """
    PUT / DELETE 等其它常见 HTTP 方法

    场景：
    - RESTful 风格接口中：
      - GET    -> 查询
      - POST   -> 新增
      - PUT    -> 整体更新
      - PATCH  -> 部分更新
      - DELETE -> 删除
    """
    url = "https://httpbin.org/put"

    # PUT 请求
    put_resp = requests.put(url, json={"key": "value"})

    # DELETE 请求
    delete_resp = requests.delete("https://httpbin.org/delete")

    print("【other_http_methods】")
    print("PUT 状态码：", put_resp.status_code)
    print("DELETE 状态码：", delete_resp.status_code)
    print("-" * 60)


def main():
    """统一调用上面的演示函数，方便一次性运行查看效果"""
    # 你可以根据需要注释 / 取消注释某些函数调用
    # basic_get()
    # get_with_params()
    # get_with_headers()
    # response_common_attrs()
    get_timeout_and_error()
    # get_with_cookies()
    # use_session()
    # post_form_data()
    # post_json_data()
    # file_upload_example()
    # other_http_methods()


if __name__ == "__main__":
    # 运行 main()，依次演示上面所有函数的效果
    # 如果你只想看某一个功能，可以临时注释掉其他函数调用
    main()