## 使用方法

- 安装 requests 包
```
pip install requests
```
- 复制 `config-sample.json` 为 `config.json`，修改其中的微人大邮箱账户、邮箱密码以及邮件发送目标邮箱：`null` 代表发给自己微人大邮箱
- 运行 `main.py`
- 在浏览器中拿到 cookie，输入脚本
    - cookie 形如 `tiup_uid=XXXXXX; access_token=XXXXXX; session=XXXXXXXX`
    - 其中，`tiup_uid` 和 `access_token` 可以在 JS Console 用 `document.cookie` 拿到
    - session 为 httpOnly 只能从浏览器里直接拿，具体百度“怎么查看cookie”
    - 然后写成上面的形式输入脚本
    - 理论上来说你已经能收到第一封邮件了 -- 它包含你之前所有课程的学分绩
    - 之后每分钟刷新两次，有更新时会把更新内容发邮件
- 如果 token 会过期就提 issue，我把验证码识别塞进来
