# 云函数部署指南

## 腾讯云部署（推荐）

### 方式1：Web控制台上传

1. 压缩代码
```bash
cd serverless
zip -r tianji-serverless.zip .
```

2. 登录腾讯云控制台
3. 进入「云函数 SCF」
4. 新建函数
5. 上传 tianji-serverless.zip
6. 配置环境变量：
   - ZHIPUAI_API_KEY=你的密钥
7. 添加API网关触发器
8. 获取访问地址

### 方式2：使用Serverless Framework

```bash
# 安装
npm install -g serverless

# 部署
serverless deploy
```

## 阿里云部署

```bash
# 安装Fun工具
npm install -g @alicloud/fun

# 部署
fun deploy
```

## Vercel部署（最简单）

```bash
# 安装
npm install -g vercel

# 部署
vercel

# 完成！
```

## 成本预估

### 腾讯云
- 免费额度：100万次/月
- 超出后：¥0.00002/次
- 预计：10万用户 < ¥10/月

### 阿里云
- 免费额度：100万次/月
- 超出后：¥0.00003/次

### Vercel
- 完全免费（个人项目）
- 无限请求

## 修改iOS代码

```swift
// NetworkService.swift
private let baseURL = "https://你的云函数地址/v1"
```

部署完成！用户下载即用！

