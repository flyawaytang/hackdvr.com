# Python Email Sender

一个简单但功能强大的Python邮件发送工具，支持以下功能：

- 支持SSL和TLS加密连接
- 支持端口25、465和587
- 支持可选的身份验证（某些服务器不需要认证）
- 支持HTML内容
- 支持多个附件
- 支持附件压缩（ZIP、TAR、TAR.GZ、TAR.BZ2）
- 支持抄送(CC)和密送(BCC)
- 命令行界面和Python库两种使用方式

## 安装

直接下载`email_sender.py`和`compression_utils.py`文件到您的项目中即可使用。

## 使用方法

### 作为Python库使用

#### 基本用法

```python
from email_sender import EmailSender

# 创建发送器
sender = EmailSender('smtp.example.com', 465)  # 使用SSL

# 认证
sender.authenticate('your.email@example.com', 'your-password')

# 创建并发送邮件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='测试邮件',
    body='这是一封测试邮件。'
)
sender.send_email(message)

# 关闭连接
sender.close()
```

#### 使用HTML内容

```python
html_body = """
<html>
<body>
    <h1>HTML邮件测试</h1>
    <p>这是一封<b>HTML格式</b>的邮件。</p>
</body>
</html>
"""

message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='HTML测试',
    body=html_body,
    is_html=True  # 指定使用HTML内容
)
```

#### 添加附件

```python
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='附件测试',
    body='请查看附件。',
    attachments=[
        './document.pdf',
        './image.jpg',
        './spreadsheet.xlsx'
    ]
)
```

#### 使用端口25（STARTTLS）

```python
# 使用端口25并启用STARTTLS
sender = EmailSender('smtp.example.com', 25, use_ssl=False)
sender.authenticate('your.email@example.com', 'your-password')

# 创建并发送邮件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='端口25测试',
    body='这是通过端口25发送的邮件。'
)
sender.send_email(message)
```

#### 不需要认证的服务器

```python
# 连接到不需要认证的SMTP服务器
sender = EmailSender('smtp.example.com', 25, use_ssl=False)
sender.connect(require_auth=False)  # 指定不需要认证

# 创建并发送邮件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='无认证测试',
    body='这是通过不需要认证的服务器发送的邮件。'
)
sender.send_email(message)
```

#### 使用压缩附件

```python
# 使用ZIP压缩多个附件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='压缩附件测试',
    body='这封邮件包含一个ZIP压缩包，里面有多个文件。',
    attachments=[
        './document1.pdf',
        './image.jpg',
        './spreadsheet.xlsx',
        './report.docx'
    ],
    compress_attachments={
        'archive_type': 'zip',
        'archive_name': 'all_documents.zip',
        'compression_level': 9  # 最大压缩率
    }
)
```

```python
# 使用TAR.GZ压缩目录和文件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='TAR.GZ压缩测试',
    body='这封邮件包含一个TAR.GZ压缩包。',
    attachments=[
        './logs/',  # 一个目录
        './config.ini',
        './data.csv'
    ],
    compress_attachments={
        'archive_type': 'tar.gz',
        'archive_name': 'project_files.tar.gz'
    }
)
```

### 作为命令行工具使用

#### 基本用法

```bash
python email_sender.py --server smtp.gmail.com --port 465 \
    --username your.email@gmail.com --to recipient@example.com \
    --subject "测试邮件" --body "这是一封测试邮件。"
```

#### 使用HTML内容

```bash
python email_sender.py --server smtp.gmail.com --port 465 \
    --username your.email@gmail.com --to recipient@example.com \
    --subject "HTML测试" --body "<h1>你好</h1><p>这是HTML内容。</p>" --html
```

#### 添加附件

```bash
python email_sender.py --server smtp.gmail.com --port 465 \
    --username your.email@gmail.com --to recipient@example.com \
    --subject "附件测试" --body "请查看附件。" \
    --attach ./document.pdf --attach ./image.jpg
```

#### 使用端口25（STARTTLS）

```bash
python email_sender.py --server smtp.example.com --port 25 --use-tls \
    --username your.email@example.com --to recipient@example.com \
    --subject "端口25测试" --body "这是通过端口25发送的邮件。"
```

#### 不需要认证的服务器

```bash
python email_sender.py --server smtp.example.com --port 25 --use-tls --no-auth \
    --to recipient@example.com --subject "无认证测试" \
    --body "这是通过不需要认证的服务器发送的邮件。"
```

#### 使用压缩附件

```bash
# 使用ZIP压缩多个附件
python email_sender.py --server smtp.gmail.com --port 465 \
    --username your.email@gmail.com --to recipient@example.com \
    --subject "压缩附件测试" --body "请查看ZIP压缩包。" \
    --attach ./document.pdf --attach ./image.jpg --attach ./data.csv \
    --compress zip
```

```bash
# 使用TAR.GZ压缩多个附件
python email_sender.py --server smtp.gmail.com --port 465 \
    --username your.email@gmail.com --to recipient@example.com \
    --subject "TAR.GZ压缩测试" --body "请查看TAR.GZ压缩包。" \
    --attach ./logs/ --attach ./config.ini \
    --compress tar.gz
```

## 命令行参数

```
--server SMTP服务器地址
--port SMTP服务器端口
--use-tls 使用TLS而不是SSL（适用于端口25、587）
--no-auth 跳过认证（适用于不需要认证的服务器）
--username 邮箱用户名/地址
--to 收件人邮箱地址，多个地址用逗号分隔
--cc 抄送收件人，多个地址用逗号分隔
--bcc 密送收件人，多个地址用逗号分隔
--subject 邮件主题
--body 邮件正文内容
--body-file 包含邮件正文的文件
--html 将正文视为HTML内容
--attach 要附加的文件（可多次使用）
--compress 压缩附件的格式（zip、tar、tar.gz、tar.bz2）
```

## 安全注意事项

1. 端口25是标准SMTP端口，但许多ISP会封锁此端口以防止垃圾邮件
2. 强烈建议使用STARTTLS或SSL加密连接，以保护您的凭据和邮件内容
3. 如果您的ISP封锁了端口25，可以尝试使用端口465（SSL）或587（TLS）
4. 企业网络环境通常允许端口25通信
5. 使用不需要认证的服务器时要特别小心，这可能会被滥用于发送垃圾邮件

## 常见邮件服务器设置

### Gmail
- 服务器: smtp.gmail.com
- 端口: 465 (SSL) 或 587 (TLS)
- 认证: 必需
- 注意: 如果启用了两步验证，需要使用应用专用密码

### QQ邮箱
- 服务器: smtp.qq.com
- 端口: 465 (SSL) 或 587 (TLS)
- 认证: 必需
- 注意: 需要在QQ邮箱设置中启用SMTP并获取授权码

### 163邮箱
- 服务器: smtp.163.com
- 端口: 465 (SSL) 或 25 (STARTTLS)
- 认证: 必需
- 注意: 需要在163邮箱设置中启用SMTP并获取授权码

### 企业邮件服务器
- 服务器: 根据企业设置
- 端口: 通常为25、465或587
- 认证: 根据企业设置，可能需要也可能不需要
- 注意: 请咨询您的IT部门获取正确的设置

