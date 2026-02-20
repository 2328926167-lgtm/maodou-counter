import streamlit as st
import re
import pandas as pd
import random

# 页面配置
st.set_page_config(
    page_title="毛豆字数统计",
    page_icon="🫘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 毛豆配色（保留您的莫兰迪色系）
colors = {
    'bg_light': '#e8f5e9',      # 淡绿背景
    'bg_card': '#ffffff',        # 卡片白
    'primary': '#5a8f5a',        # 灰绿（主色）
    'primary_light': '#8fb98f',  # 浅灰绿
    'accent': '#c4a574',         # 卡其/豆黄
    'text': '#4a6b4a',           # 深灰绿文字
    'text_secondary': '#7a8f7a', # 次要文字
    'border': '#c8d6c8',         # 边框绿
    'highlight': '#f5f0e6',      # 米黄高亮
    'blue_gray': '#7a8fa6',      # 灰蓝
    'warm_gray': '#b8a89a',      # 暖灰
    'english_blue': '#6b8e9f'    # 英文蓝灰
}

# 毛豆语录（保留您的）
maodou_quotes = [
    "毛豆说：每个字都是一颗饱满的豆子 🌱",
    "今天也要像毛豆一样，颗颗分明！",
    "毛豆小贴士：标点符号也是豆子哦~",
    "青色的毛豆，绿色的希望 💚",
    "毛豆陪你一起数清楚每个字",
    "一颗毛豆一粒字，数着数着就饿了",
    "毛豆：我是蔬菜还是豆类？不重要！",
    "饱满的文字，像成熟的毛豆荚 🫛"
]

# 自定义CSS（模拟您的桌面版风格）
st.markdown(f"""
<style>
    .stApp {{
        background-color: {colors['bg_light']};
    }}
    .main-header {{
        background: linear-gradient(135deg, {colors['primary']}, {colors['primary_light']});
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .main-header h1 {{
        font-size: 42px;
        margin: 0;
        font-weight: bold;
    }}
    .main-header p {{
        font-size: 16px;
        margin: 5px 0 0 0;
        opacity: 0.9;
    }}
    .quote-box {{
        background-color: {colors['primary_light']};
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 16px;
        color: {colors['text']};
        font-weight: 500;
        border-left: 5px solid {colors['accent']};
    }}
    .card {{
        background-color: {colors['bg_card']};
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid {colors['border']};
    }}
    .big-stat {{
        background-color: {colors['highlight']};
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .big-stat-left {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .big-stat-icon {{
        font-size: 36px;
    }}
    .big-stat-label {{
        font-size: 18px;
        color: {colors['text_secondary']};
    }}
    .big-stat-value {{
        font-size: 48px;
        font-weight: bold;
        color: {colors['primary']};
    }}
    .english-value {{
        color: {colors['english_blue']};
    }}
    .separator {{
        height: 2px;
        background-color: {colors['border']};
        margin: 20px 0;
    }}
    .footer {{
        text-align: center;
        padding: 20px;
        color: {colors['text_secondary']};
        font-size: 14px;
        border-top: 1px solid {colors['border']};
        margin-top: 30px;
    }}
    .maodou-feature {{
        background-color: {colors['highlight']};
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
        font-size: 20px;
        font-weight: bold;
        color: {colors['accent']};
    }}
    .comment-box {{
        padding: 10px 0;
        font-size: 16px;
    }}
    .stButton > button {{
        background-color: {colors['primary']};
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 0;
        transition: all 0.3s;
    }}
    .stButton > button:hover {{
        background-color: {colors['primary_light']};
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .upload-text {{
        color: {colors['blue_gray']};
        font-size: 14px;
    }}
    .metric-box {{
        background-color: {colors['bg_card']};
        padding: 15px;
        border-radius: 10px;
        border: 1px solid {colors['border']};
        text-align: center;
    }}
    .metric-label {{
        color: {colors['text_secondary']};
        font-size: 14px;
    }}
    .metric-value {{
        color: {colors['primary']};
        font-size: 24px;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# 统计函数（完全保留您的逻辑）
def count_text_stats(text):
    """全面的文本统计工具（毛豆版）"""
    if not text or not text.strip():
        return None
        
    total_chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))
    chars_no_punct = len([c for c in text if '\u4e00' <= c <= '\u9fff' or c.isalnum()])
    chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    numbers = len(re.findall(r'\d+', text))
    punctuation = len(re.findall(r'[^\w\s\u4e00-\u9fff]', text))
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    sentences = len([s for s in re.split(r'[。！？.!?]', text) if s.strip()])
    lines = text.count('\n') + 1
    
    # 毛豆特色：计算大概需要多少颗毛豆（按每颗毛豆平均2个字计算）
    maodou_count = chars_no_space // 2
    if chars_no_space % 2 != 0:
        maodou_count += 1
    
    return {
        "中文字数 🌱": chinese_chars,
        "英文单词数 🔤": english_words,
        "总字符数（不含空格）": chars_no_space,
        "总字符数（含空格）": total_chars,
        "纯文字数": chars_no_punct,
        "数字个数": numbers,
        "标点符号数": punctuation,
        "段落数": paragraphs,
        "句子数": sentences,
        "行数": lines,
        "≈ 相当于多少颗毛豆 🫘": maodou_count
    }

# ========== 页面布局 ==========

# 毛豆标题（模拟您的header）
st.markdown(f"""
<div class="main-header">
    <h1>🫘 毛豆字数统计</h1>
    <p>一颗一颗数清楚，一粒一粒算明白</p>
</div>
""", unsafe_allow_html=True)

# 毛豆语录（随机显示）
if 'quote' not in st.session_state:
    st.session_state.quote = random.choice(maodou_quotes)

st.markdown(f'<div class="quote-box">{st.session_state.quote}</div>', unsafe_allow_html=True)

# 输入卡片
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("##### 📝 把文字倒进毛豆碗里：")

# 文本输入
text_input = st.text_area("", height=200, label_visibility="collapsed", 
                          placeholder="在这里粘贴或输入要统计的文字...")

# 按钮行
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 数豆子", use_container_width=True):
        if text_input and text_input.strip():
            stats = count_text_stats(text_input)
            st.session_state['stats'] = stats
            st.session_state['show_result'] = True
            st.session_state.quote = random.choice(maodou_quotes)
            st.rerun()
        else:
            st.warning("毛豆提醒：先放点文字进来呀！")

with col2:
    uploaded_file = st.file_uploader("📁 倒豆子", type=['txt'], label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            stringio = uploaded_file.getvalue().decode("utf-8")
            st.session_state['uploaded_text'] = stringio
            st.success(f"成功倒入 {len(stringio)} 颗文字豆！")
            st.rerun()
        except:
            st.error("毛豆读不懂这个文件，试试别的吧~")

with col3:
    if st.button("📋 示例", use_container_width=True):
        example_text = """毛豆，学名大豆，是黄豆的嫩荚。
Edamame is the young pod of soybean.
毛豆炒肉、盐水毛豆、毛豆炖排骨...
每一个字都是一颗小毛豆，数一数这里有多少颗？

毛豆营养丰富，含有优质蛋白质。
Edamame is rich in protein and delicious!
夏天来一盘冰镇毛豆，配上啤酒，简直是人间美味！"""
        st.session_state['example_text'] = example_text
        st.rerun()

with col4:
    if st.button("🧹 清空", use_container_width=True):
        for key in ['stats', 'show_result', 'uploaded_text', 'example_text']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.quote = random.choice(maodou_quotes)
        st.rerun()

# 显示示例或上传的文本
if 'example_text' in st.session_state:
    text_input = st.session_state['example_text']
    st.info("📋 示例文字已填入，点击'数豆子'看看吧")
elif 'uploaded_text' in st.session_state:
    text_input = st.session_state['uploaded_text']

st.markdown('</div>', unsafe_allow_html=True)

# ========== 统计结果 ==========
if 'show_result' in st.session_state and 'stats' in st.session_state:
    stats = st.session_state['stats']
    
    # 进度条（模拟桌面版）
    progress_value = min(stats["总字符数（不含空格）"] / 500, 1.0)
    st.progress(progress_value, text=f"文字密度：{int(progress_value*100)}%")
    
    # 结果卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 📊 毛豆数好了：")
    
    # 大字显示 - 中文字数
    st.markdown(f"""
    <div class="big-stat">
        <div class="big-stat-left">
            <span class="big-stat-icon">🌱</span>
            <span class="big-stat-label">中文字数</span>
        </div>
        <div class="big-stat-value">{stats['中文字数 🌱']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 大字显示 - 英文单词数
    st.markdown(f"""
    <div class="big-stat">
        <div class="big-stat-left">
            <span class="big-stat-icon">🔤</span>
            <span class="big-stat-label">英文单词数</span>
        </div>
        <div class="big-stat-value english-value">{stats['英文单词数 🔤']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # 两列统计
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">总字符数（含空格）</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["总字符数（含空格）"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">总字符数（不含空格）</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["总字符数（不含空格）"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">纯文字数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["纯文字数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">数字个数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["数字个数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">标点符号数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["标点符号数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">段落数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["段落数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">句子数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["句子数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">行数</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["行数"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 毛豆特色统计
    st.markdown(f"""
    <div class="maodou-feature">
        🫘 这些文字大约相当于 {stats['≈ 相当于多少颗毛豆 🫘']} 颗毛豆
    </div>
    """, unsafe_allow_html=True)
    
    # 评价
    total = stats["总字符数（不含空格）"]
    chinese = stats["中文字数 🌱"]
    english = stats["英文单词数 🔤"]
    
    if chinese > 0 and english > 0:
        if chinese > english * 3:
            comment = f"🌱 中文为主（{chinese}字），夹杂{english}个英文单词"
            comment_color = colors['primary']
        elif english > chinese:
            comment = f"🔤 英文为主（{english}词），夹杂{chinese}个汉字"
            comment_color = colors['english_blue']
        else:
            comment = f"🌏 中英混合，中文{chinese}字 + 英文{english}词，像毛豆炒肉"
            comment_color = colors['accent']
    elif chinese > 0:
        comment = "🌱 纯正中文，像一盘清炒毛豆"
        comment_color = colors['primary']
    elif english > 0:
        comment = "🔤 纯英文文本，毛豆在学外语"
        comment_color = colors['english_blue']
    else:
        comment = "🫘 只有数字和符号，毛豆有点懵"
        comment_color = colors['warm_gray']
    
    if total < 50:
        size_comment = "一小撮"
    elif total < 200:
        size_comment = "一小盘"
    elif total < 500:
        size_comment = "一大碗"
    else:
        size_comment = "一麻袋"
    
    st.markdown(f'<div class="comment-box" style="color:{comment_color}">{comment}，共{size_comment}（{total}字符）</div>', unsafe_allow_html=True)
    
    # 详细数据
    with st.expander("📋 查看详细数据"):
        df_data = []
        for key, value in stats.items():
            df_data.append({"统计项": key, "数量": value})
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 底部（保留您的署名）
st.markdown(f"""
<div class="footer">
    <p>🫘 毛豆字数统计 · 一颗一颗数清楚 · 永远免费</p>
    <p style="color:{colors['warm_gray']}">Made with 💚 by 毛豆爸爸——吴宇阳</p>
</div>
""", unsafe_allow_html=True)