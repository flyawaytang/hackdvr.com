# Python 邮件发送工具

这是一个功能完整的 Python 3 邮件发送工具，支持：

- SMTP 服务器认证
- 纯文本和 HTML 邮件格式
- 添加多个附件
- 支持抄送 (CC) 和密送 (BCC)
- 命令行界面和 Python 类库两种使用方式

## 功能特点

- 支持 SSL 和 TLS 加密连接
- 支持多种邮件服务提供商 (Gmail, QQ邮箱, 163邮箱等)
- 灵活的 API 设计，易于集成到其他项目中
- 详细的错误处理和日志输出
- 支持中文主题和内容

## 安装

此工具只使用 Python 标准库，无需安装额外依赖。

要求：
- Python 3.6 或更高版本

## 使用方法

### 作为命令行工具

```bash
python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com \
    --to recipient@example.com --subject "测试邮件" \
    --body "这是一封测试邮件。" --attach document.pdf
```

### 作为 Python 库

```python
from email_sender import EmailSender

# 创建发送器实例
sender = EmailSender('smtp.gmail.com', 465)  # 使用 SSL

# 认证
sender.authenticate('your.email@gmail.com', 'your-password-or-app-password')

# 创建邮件
message = sender.create_message(
    to_addresses='recipient@example.com',
    subject='测试邮件',
    body='这是一封测试邮件，带有附件。',
    attachments=['./document.pdf']
)

# 发送邮件
sender.send_email(message)

# 关闭连接
sender.close()
```

## 常见邮件服务商设置

### Gmail

- SMTP 服务器: `smtp.gmail.com`
- SSL 端口: `465`
- TLS 端口: `587`
- 注意: 如果启用了两步验证，需要使用应用专用密码

### QQ 邮箱

- SMTP 服务器: `smtp.qq.com`
- SSL 端口: `465`
- TLS 端口: `587`
- 注意: 需要在 QQ 邮箱设置中开启 SMTP 服务并获取授权码

### 163 邮箱

- SMTP 服务器: `smtp.163.com`
- SSL 端口: `465`
- TLS 端口: `25` (部分 ISP 可能会封锁此端口)
- 注意: 需要在 163 邮箱设置中开启 SMTP 服务并获取授权码

## 命令行参数

```
--server SMTP服务器地址 (必需)
--port SMTP服务器端口 (必需)
--use-tls 使用TLS而非SSL (可选)
--username 邮箱用户名/地址 (可选，未提供时会提示输入)
--to 收件人邮箱地址，多个地址用逗号分隔 (必需)
--cc 抄送地址，多个地址用逗号分隔 (可选)
--bcc 密送地址，多个地址用逗号分隔 (可选)
--subject 邮件主题 (必需)
--body 邮件正文内容 (与--body-file二选一)
--body-file 包含邮件正文的文件路径 (与--body二选一)
--html 指定正文为HTML格式 (可选)
--attach 附件文件路径，可多次使用添加多个附件 (可选)
```

## 示例

查看 `email_example.py` 文件获取更多使用示例，包括：

1. Gmail 发送示例
2. QQ邮箱发送示例
3. 发送带多个附件的邮件示例
4. 命令行使用示例

## 注意事项

1. 对于 Gmail，如果启用了两步验证，需要使用应用专用密码而非账户密码
2. 对于 QQ 邮箱和 163 邮箱，需要在邮箱设置中开启 SMTP 服务并获取授权码
3. 某些 ISP 可能会封锁特定的 SMTP 端口，特别是 25 端口
4. 密码在命令行中不会显示，会安全地提示输入
5. 附件文件必须存在且可读，否则会跳过并显示警告

