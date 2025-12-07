# 🔮 天机命理 - Vercel API

基于智谱AI GLM-4的命理分析API，专为Vercel Serverless平台优化。

> 已成功配置环境变量，准备部署！

## ✨ 特性

- ✅ **完全免费** - Vercel个人版无限制
- ✅ **全球CDN** - 自动HTTPS + CDN加速
- ✅ **智能分析** - 集成智谱AI大模型
- ✅ **零运维** - 自动扩容，无需管理服务器
- ✅ **即时部署** - Git推送自动部署

## 📦 文件说明

```
serverless/
├── main.py           # FastAPI应用主文件
├── requirements.txt  # Python依赖
├── vercel.json      # Vercel配置
├── .gitignore       # Git忽略文件
└── README.md        # 本文件
```

## 🚀 部署到Vercel

### 1. 推送代码到GitHub

```bash
git add .
git commit -m "Update API"
git push origin main
```

### 2. 在Vercel导入项目

1. 访问 https://vercel.com
2. 点击 "Import Project"
3. 选择GitHub仓库
4. 配置环境变量：
   - `ZHIPUAI_API_KEY` = 你的智谱AI密钥
5. 点击 "Deploy"

### 3. 获取API地址

部署成功后，Vercel会提供：
```
https://your-project.vercel.app
```

## 📡 API端点

### 1. 命理详批
```
POST /v1/analysis/mingli
```

### 2. 流年运势
```
POST /v1/analysis/liunian
```

### 3. 每日宜忌
```
POST /v1/daily/yiji
```

### 4. 时辰吉凶
```
POST /v1/daily/shichen
```

### 5. API文档
```
GET /docs
```

## 🔑 获取智谱AI密钥

1. 访问 https://open.bigmodel.cn/
2. 微信扫码登录
3. 进入「API密钥」页面
4. 创建新密钥
5. 复制密钥（格式：`xxxxxx.xxxxxx`）

**免费额度：** 500万tokens（约1万次分析）

## 📱 在iOS APP中使用

修改 `NetworkService.swift`：

```swift
private let baseURL = "https://your-project.vercel.app/v1"
```

## 💡 成本说明

### Vercel
- ✅ 完全免费（个人项目）
- ✅ 无请求次数限制
- ✅ 100GB带宽/月

### 智谱AI
- ✅ 500万tokens免费
- ✅ 超出后：¥0.005/千tokens
- ✅ 1次分析≈500tokens ≈ ¥0.0025

**预估：** 支持1万次免费分析，之后每万次约 ¥25

## 🛠️ 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ZHIPUAI_API_KEY=your_key_here

# 运行服务
python main.py

# 访问
open http://localhost:8000/docs
```

## 📊 监控

在Vercel Dashboard可以查看：
- 请求统计
- 错误日志
- 性能指标
- 使用情况

## 🔄 更新代码

只需推送到GitHub，Vercel会自动重新部署：

```bash
git add .
git commit -m "Update"
git push
```

## ❓ 常见问题

### Q: API返回错误？
A: 检查Vercel环境变量中的`ZHIPUAI_API_KEY`是否正确设置

### Q: 如何查看日志？
A: 在Vercel Dashboard的Deployments页面查看实时日志

### Q: 支持其他AI模型吗？
A: 可以修改`main.py`中的模型配置，支持任何OpenAI兼容接口

---

**部署完成后，您的iOS APP即可直接使用！** 🎉
