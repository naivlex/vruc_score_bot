## 使用方法

- 安装 requests pillow 包
```
pip install requests pillow
```
- 复制 `config-sample.json` 为 `config.json`，修改其中的学号、微人大密码、人大邮箱账户、人大邮箱密码以及邮件发送目标邮箱：`null` 代表发给自己微人大邮箱
    - `captcha_on_ascii` 代表要不要在终端直接打印验证码图片
- 运行 `main.py`
- 输入弹出的验证码
- 理论上来说你已经能收到第一封邮件了
    - 它包含你之前所有课程的学分绩
- 之后每五分钟刷新一次，有更新时会把更新内容发邮件
- token 过期以后会自动重新登录
    - 需要重新输入验证码

- vruc.py 里有关于自动识别验证码的编写提示
    - 稳妥起见代码我应该还是不会放上来
