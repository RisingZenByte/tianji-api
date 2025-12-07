# -*- coding: utf-8 -*-
"""
天机命理 - 云函数版本
适用于腾讯云SCF、阿里云FC、AWS Lambda、Vercel等
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os
from zhipuai import ZhipuAI
import json

app = FastAPI(title="天机命理API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化智谱AI客户端
zhipu_client = None
if os.getenv("ZHIPUAI_API_KEY"):
    zhipu_client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))


@app.get("/")
def root():
    return {"message": "🔮 天机命理API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "天机命理API"}


@app.post("/v1/analysis/mingli")
async def analyze_mingli(request: dict):
    """命理详批分析 - 使用AI生成个性化分析"""
    if not zhipu_client:
        return {
            "personality": "请在云函数中配置ZHIPUAI_API_KEY环境变量",
            "career": "访问 https://open.bigmodel.cn/ 获取免费API密钥",
            "wealth": "新用户赠送500万tokens免费额度",
            "marriage": "配置后即可获得AI个性化分析",
            "health": "每次分析都是根据八字实时生成",
            "luckyDirections": ["东方"],
            "luckyColors": ["绿色"],
            "suggestions": ["请配置ZHIPUAI_API_KEY以启用AI功能"]
        }
    
    bazi = request.get("bazi", {})
    gender = request.get("gender", "")
    
    prompt = f"""
根据以下八字信息进行专业命理分析：

年柱：{bazi.get('nian', '')}
月柱：{bazi.get('yue', '')}
日柱：{bazi.get('ri', '')}（日主）
时柱：{bazi.get('shi', '')}
性别：{gender}

请详细分析并以JSON格式输出（不要使用markdown格式）：
{{
  "personality": "性格特征分析，100-200字，要专业、准确、易懂",
  "career": "事业运势分析，100-200字，给出具体职业方向建议",
  "wealth": "财运分析，100-200字，理财建议和投资方向",
  "marriage": "婚姻感情分析，100-200字，配偶特征和建议",
  "health": "健康运势分析，100-200字，养生建议",
  "luckyDirections": ["吉利方位1", "吉利方位2"],
  "luckyColors": ["幸运颜色1", "幸运颜色2", "幸运颜色3"],
  "suggestions": ["实用建议1", "实用建议2", "实用建议3"]
}}

要求：
1. 分析要专业、准确，符合传统命理规则
2. 语言要温和、积极、鼓励性
3. 避免过于绝对化的表述
4. 多给实用建议，少用玄学术语
"""
    
    try:
        response = zhipu_client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": "你是一位精通中国传统命理学的专业大师，擅长八字分析、五行推算。你的回答专业、准确、易懂，善于用现代语言解释传统命理知识。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # 清理可能的markdown格式
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        return result
        
    except Exception as e:
        return {
            "personality": f"AI分析暂时失败，请稍后重试",
            "career": "事业运势需要详细分析",
            "wealth": "财运分析需要详细研究",
            "marriage": "婚姻运势需要全面考量",
            "health": "健康运势需要综合判断",
            "luckyDirections": ["东方", "南方"],
            "luckyColors": ["绿色", "红色"],
            "suggestions": ["请稍后重试", "确保网络连接正常"]
        }


@app.post("/v1/analysis/liunian")
async def analyze_liunian(request: dict):
    """流年运势分析"""
    year = request.get("year", 2025)
    
    # 计算流年干支
    gan_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    zhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    gan_zhi = f"{gan_list[gan_index]}{zhi_list[zhi_index]}"
    
    return {
        "year": year,
        "ganZhi": gan_zhi,
        "overall": f"{year}年整体运势平稳向上，把握机遇，稳中求进。",
        "career": "事业方面有发展机会，需要努力把握。",
        "wealth": "财运方面需要稳健理财，避免冒进。",
        "love": "感情运势良好，单身者有机会遇到良缘。",
        "health": "注意身体健康，保持良好作息。",
        "luckyMonths": [3, 6, 9],
        "attentionMonths": [2, 7],
        "suggestions": ["把握机遇，稳健前行", "保持积极心态", "注意身心健康"]
        }


@app.post("/v1/daily/yiji")
async def daily_yiji(request: dict):
    """每日宜忌 - 根据日期和八字动态生成"""
    date = request.get("date", "")[:10]
    
    # 计算日干支（简化版）
    from datetime import datetime
    try:
        date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
        day_of_year = date_obj.timetuple().tm_yday
        
        gan_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        zhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        gan_index = (day_of_year + 6) % 10
        zhi_index = (day_of_year + 4) % 12
        gan_zhi = f"{gan_list[gan_index]}{zhi_list[zhi_index]}"
        
    except:
        gan_zhi = "甲子"
    
    # 根据日期生成不同的宜忌（使用日期作为种子）
    import hashlib
    seed = int(hashlib.md5(date.encode()).hexdigest()[:8], 16)
    
    all_yi = ["祭祀", "祈福", "求嗣", "开光", "出行", "解除", "伐木", "造屋", "起基", "修造", "动土", "安床", "纳畜", "入宅", "移徙", "安葬", "破土", "启钻", "嫁娶", "订婚", "纳采", "问名", "纳财", "开市", "交易", "立券", "栽种"]
    all_ji = ["嫁娶", "动土", "安葬", "行丧", "破土", "修坟", "开市", "交易", "立券", "纳财", "出货财", "开仓", "栽种", "纳畜", "牧养", "伐木", "架马", "合脊", "入宅", "移徙", "安床", "开光", "造船", "治病", "安门", "作灶"]
    
    # 基于种子选择
    import random
    random.seed(seed)
    yi = random.sample(all_yi, 8)
    ji = random.sample([item for item in all_ji if item not in yi], 6)
    
    return {
        "date": date,
        "ganZhi": gan_zhi,
        "yi": yi,
        "ji": ji,
        "chongSha": "冲鼠煞北",
        "jiShen": ["天德", "月德", "天恩", "四相"],
        "xiongSha": ["月破", "大耗", "五虚"],
        "wuXing": "海中金",
        "pengZu": [f"{gan_zhi[0]}不开仓财物耗散", f"{gan_zhi[1]}不问卜自惹祸殃"]
    }


@app.post("/v1/daily/shichen")
async def daily_shichen(request: dict):
    """时辰吉凶 - 12时辰动态分析"""
    date = request.get("date", "")[:10]
    
    shichens = []
    names = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时"]
    jixiong_list = ["大吉", "吉", "凶", "吉", "小吉", "凶", "大吉", "吉", "小凶", "吉", "凶", "吉"]
    
    for i in range(12):
        hour = 23 if i == 0 else (i * 2 - 1)
        jixiong = jixiong_list[i]
        
        if "吉" in jixiong:
            yi = ["祈福", "求财", "出行", "开市", "订婚"]
            ji = ["安葬", "行丧"]
            analysis = f"{names[i]}{jixiong}，宜办要事，诸事顺遂，把握时机。"
        else:
            yi = ["祭祀", "修造"]
            ji = ["嫁娶", "动土", "出行", "开市"]
            analysis = f"{names[i]}{jixiong}，诸事不宜，宜静不宜动，谨慎行事。"
        
        shichens.append({
            "hour": hour,
            "name": names[i],
            "ganZhi": "甲子",
            "jiXiong": jixiong,
            "yi": yi[:3],
            "ji": ji[:3],
            "analysis": analysis
        })
    
    return {"date": date, "shiChens": shichens}


# 云函数Handler（用于AWS Lambda, 腾讯云SCF等）
handler = Mangum(app)

# Vercel Handler
app_handler = app

# 如果直接运行（本地测试）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
