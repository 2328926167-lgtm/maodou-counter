import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import random
from datetime import datetime

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

# 毛豆语录
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

class MaodouWordCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("🫘 毛豆字数统计")
        self.root.geometry("750x700")
        self.root.configure(bg='#e8f5e9')
        
        # 窗口居中
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 750) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"750x700+{x}+{y}")
        
        # 低饱和度毛豆配色 - 莫兰迪色系
        self.colors = {
            'bg_light': '#e8f5e9',      # 淡绿背景
            'bg_card': '#ffffff',        # 卡片白
            'primary': '#5a8f5a',        # 灰绿（主色）- 降低饱和度
            'primary_light': '#8fb98f',  # 浅灰绿
            'accent': '#c4a574',         # 卡其/豆黄（代替亮橙）
            'text': '#4a6b4a',           # 深灰绿文字
            'text_secondary': '#7a8f7a', # 次要文字
            'border': '#c8d6c8',         # 边框绿
            'highlight': '#f5f0e6',      # 米黄高亮
            'blue_gray': '#7a8fa6',      # 灰蓝
            'warm_gray': '#b8a89a',      # 暖灰
            'english_blue': '#6b8e9f'    # 英文蓝灰
        }
        
        # 创建带滚动条的主画布
        self.setup_scrollable_frame()
        
        # 内容区域
        self.create_header()
        self.create_quote_section()
        self.create_input_section()
        self.create_buttons()
        self.create_progress_section()
        self.create_result_section()
        self.create_footer()
        
        # 绑定鼠标滚轮
        self.bind_mousewheel()
        
        # 绑定快捷键
        self.text_area.bind('<Control-Return>', lambda e: self.count_now())
        self.text_area.bind('<Control-o>', lambda e: self.open_file())
    
    def setup_scrollable_frame(self):
        """设置可滚动框架"""
        # 创建画布和滚动条
        self.main_canvas = tk.Canvas(self.root, bg=self.colors['bg_light'], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        
        # 创建可滚动框架
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.colors['bg_light'])
        
        # 配置画布滚动区域
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        # 在画布上创建窗口
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=730)
        
        # 配置画布和滚动条
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定画布大小变化
        self.main_canvas.bind('<Configure>', self.on_canvas_configure)
    
    def on_canvas_configure(self, event):
        """画布大小变化时调整内部框架宽度"""
        self.main_canvas.itemconfig(self.canvas_window, width=event.width-5)
    
    def bind_mousewheel(self):
        """绑定鼠标滚轮事件"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Windows鼠标滚轮
        self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux鼠标滚轮
        self.main_canvas.bind_all("<Button-4>", lambda e: self.main_canvas.yview_scroll(-1, "units"))
        self.main_canvas.bind_all("<Button-5>", lambda e: self.main_canvas.yview_scroll(1, "units"))
    
    def create_header(self):
        """创建标题区域"""
        header_frame = tk.Frame(self.scrollable_frame, bg=self.colors['primary'], 
                               relief='flat', bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        header_frame.pack_propagate(False)
        header_frame.configure(height=110)
        
        title_inner = tk.Frame(header_frame, bg=self.colors['primary'])
        title_inner.pack(expand=True)
        
        # 毛豆图标
        tk.Label(title_inner, text="🫘", font=("Segoe UI Emoji", 36), 
                bg=self.colors['primary']).pack()
        
        tk.Label(title_inner, text="毛豆字数统计", 
                font=("微软雅黑", 24, "bold"), 
                bg=self.colors['primary'], 
                fg='#f1f8e9').pack()
        
        tk.Label(title_inner, text="一颗一颗数清楚，一粒一粒算明白", 
                font=("微软雅黑", 11), 
                bg=self.colors['primary'], 
                fg='#c8e6c9').pack()
    
    def create_quote_section(self):
        """创建语录区域"""
        self.quote_frame = tk.Frame(self.scrollable_frame, bg=self.colors['primary_light'], 
                                   relief='flat', bd=0)
        self.quote_frame.pack(fill=tk.X, padx=5, pady=(0, 15))
        
        self.quote_label = tk.Label(self.quote_frame, 
                                   text=random.choice(maodou_quotes),
                                   font=("微软雅黑", 11), 
                                   bg=self.colors['primary_light'], 
                                   fg=self.colors['text'],
                                   wraplength=680,
                                   pady=10)
        self.quote_label.pack()
    
    def create_input_section(self):
        """创建输入区域"""
        input_card = tk.Frame(self.scrollable_frame, bg=self.colors['bg_card'], 
                             relief='solid', bd=1)
        input_card.pack(fill=tk.X, padx=5, pady=(0, 12))
        
        # 标题
        tk.Label(input_card, text="📝 把文字倒进毛豆碗里：", 
                font=("微软雅黑", 12, "bold"), 
                bg=self.colors['bg_card'], 
                fg=self.colors['text']).pack(anchor='w', padx=15, pady=(12, 8))
        
        # 文本输入框
        self.text_area = scrolledtext.ScrolledText(
            input_card, 
            width=65, 
            height=10, 
            font=("微软雅黑", 11),
            bg='#fafafa',
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            insertbackground=self.colors['primary']
        )
        self.text_area.pack(fill=tk.X, padx=15, pady=(0, 12))
    
    def create_buttons(self):
        """创建按钮区域"""
        btn_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_light'])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 12))
        
        # 按钮配置
        btn_configs = [
            ("📊 数豆子", self.count_now, self.colors['primary']),
            ("📁 倒豆子", self.open_file, self.colors['blue_gray']),
            ("📋 示例", self.load_example, self.colors['accent']),
            ("🧹 清空", self.clear, self.colors['warm_gray'])
        ]
        
        for text, cmd, bg in btn_configs:
            btn = tk.Button(
                btn_frame, 
                text=text, 
                command=cmd,
                font=("微软雅黑", 10, "bold"),
                bg=bg, 
                fg='white',
                activebackground=self.darken_color(bg),
                activeforeground='white',
                width=11,
                height=2,
                relief='flat',
                cursor='hand2',
                borderwidth=0
            )
            btn.pack(side=tk.LEFT, padx=6, expand=True, fill=tk.X)
            self.add_hover_effect(btn, bg, self.darken_color(bg))
    
    def create_progress_section(self):
        """创建进度条区域"""
        self.progress_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_light'])
        
        self.progress_var = tk.DoubleVar()
        self.progress_canvas = tk.Canvas(self.progress_frame, bg='#e0e0e0', 
                                        height=18, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)
        
        self.progress_text = tk.Label(self.progress_frame, 
                                     text="", 
                                     font=("微软雅黑", 10),
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['text_secondary'])
        self.progress_text.pack(pady=(4, 0))
    
    def create_result_section(self):
        """创建结果区域"""
        self.result_card = tk.Frame(self.scrollable_frame, bg=self.colors['bg_card'], 
                                   relief='solid', bd=1)
        
        # 结果标题
        result_header = tk.Frame(self.result_card, bg=self.colors['primary'])
        result_header.pack(fill=tk.X)
        
        tk.Label(result_header, text="📊 毛豆数好了：", 
                font=("微软雅黑", 13, "bold"), 
                bg=self.colors['primary'], 
                fg='#f1f8e9').pack(anchor='w', padx=12, pady=8)
        
        # 优先显示区域 - 中文字数和英文单词数
        self.priority_frame = tk.Frame(self.result_card, bg=self.colors['highlight'])
        
        # 中文字数大显示
        self.chinese_big = tk.Frame(self.priority_frame, bg=self.colors['highlight'])
        self.chinese_big.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        # 英文单词数大显示
        self.english_big = tk.Frame(self.priority_frame, bg=self.colors['highlight'])
        self.english_big.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        # 分隔线
        self.separator = tk.Frame(self.result_card, bg=self.colors['border'], height=2)
        
        # 次要统计内容
        self.result_content = tk.Frame(self.result_card, bg=self.colors['bg_card'])
        self.result_content.pack(fill=tk.X, padx=12, pady=12)
        
        # 两列统计
        self.left_stats = tk.Frame(self.result_content, bg=self.colors['bg_card'])
        self.left_stats.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        self.right_stats = tk.Frame(self.result_content, bg=self.colors['bg_card'])
        self.right_stats.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        # 毛豆特色统计
        self.maodou_feature = tk.Frame(self.result_card, bg=self.colors['highlight'])
        
        self.maodou_label = tk.Label(self.maodou_feature, 
                                    text="", 
                                    font=("微软雅黑", 13, "bold"),
                                    bg=self.colors['highlight'],
                                    fg=self.colors['accent'])
        self.maodou_label.pack(pady=12)
        
        # 评价区域
        self.comment_frame = tk.Frame(self.result_card, bg=self.colors['bg_card'])
        
        self.comment_label = tk.Label(self.comment_frame, 
                                     text="", 
                                     font=("微软雅黑", 11),
                                     bg=self.colors['bg_card'],
                                     fg=self.colors['text'],
                                     wraplength=680)
        self.comment_label.pack()
        
        # 详细数据
        self.detail_frame = tk.Frame(self.result_card, bg=self.colors['bg_card'])
        
        tk.Label(self.detail_frame, text="📋 详细数据：", 
                font=("微软雅黑", 10, "bold"),
                bg=self.colors['bg_card'],
                fg=self.colors['text']).pack(anchor='w', pady=(0, 8))
        
        self.detail_text = tk.Text(self.detail_frame, 
                                  width=75, 
                                  height=10, 
                                  font=("Consolas", 10),
                                  bg='#fafafa',
                                  fg=self.colors['text'],
                                  relief='solid',
                                  borderwidth=1,
                                  padx=8,
                                  pady=8)
        self.detail_text.pack(fill=tk.X)
        self.detail_text.config(state='disabled')
    
    def create_footer(self):
        """创建底部"""
        footer = tk.Frame(self.scrollable_frame, bg=self.colors['bg_light'])
        footer.pack(fill=tk.X, padx=5, pady=15)
        
        tk.Label(footer, text="🫘 毛豆字数统计 · 一颗一颗数清楚 · 永远免费", 
                font=("微软雅黑", 10),
                bg=self.colors['bg_light'],
                fg=self.colors['text_secondary']).pack()
        
        tk.Label(footer, text="Made with 💚 by 毛豆爸爸——吴宇阳", 
                font=("微软雅黑", 9),
                bg=self.colors['bg_light'],
                fg=self.colors['warm_gray']).pack(pady=(4, 0))
    
    def darken_color(self, hex_color, factor=0.85):
        """加深颜色"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darkened)
    
    def add_hover_effect(self, widget, normal_bg, hover_bg):
        """添加悬停效果"""
        def on_enter(e):
            widget['bg'] = hover_bg
        def on_leave(e):
            widget['bg'] = normal_bg
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def update_progress(self, value, text):
        """更新进度条"""
        self.progress_frame.pack(fill=tk.X, padx=5, pady=(0, 12))
        self.progress_var.set(value)
        self.progress_text.config(text=text)
        
        # 绘制进度条
        self.progress_canvas.delete('all')
        width = self.progress_canvas.winfo_width()
        if width < 50:
            width = 700
        
        fill_width = int(width * value)
        
        # 绘制背景
        self.progress_canvas.create_rectangle(0, 0, width, 18, 
                                             fill='#e8e8e8', 
                                             outline='', width=0)
        
        # 绘制填充
        if fill_width > 0:
            self.progress_canvas.create_rectangle(0, 0, fill_width, 18, 
                                                 fill=self.colors['primary_light'], 
                                                 outline='', width=0)
        
        # 绘制边框
        self.progress_canvas.create_rectangle(0, 0, width, 18, 
                                             outline=self.colors['border'], 
                                             width=1)
    
    def create_big_stat(self, parent, icon, label, value, color):
        """创建大字号统计项"""
        frame = tk.Frame(parent, bg=self.colors['highlight'])
        frame.pack(fill=tk.X, pady=3)
        
        left = tk.Frame(frame, bg=self.colors['highlight'])
        left.pack(side=tk.LEFT)
        
        tk.Label(left, text=icon, font=("Segoe UI Emoji", 24), 
                bg=self.colors['highlight']).pack(side=tk.LEFT)
        
        tk.Label(left, text=label, font=("微软雅黑", 12), 
                bg=self.colors['highlight'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Label(frame, text=str(value), font=("微软雅黑", 28, "bold"), 
                bg=self.colors['highlight'],
                fg=color).pack(side=tk.RIGHT)
    
    def count_now(self):
        """执行统计"""
        text = self.text_area.get(1.0, tk.END)
        stats = count_text_stats(text)
        
        if not stats:
            messagebox.showwarning("提示", "🫘 毛豆提醒：先放点文字进来呀！")
            return
        
        # 更新语录
        self.quote_label.config(text=random.choice(maodou_quotes))
        
        # 显示进度条
        progress = min(stats["总字符数（不含空格）"] / 500, 1.0)
        self.update_progress(progress, f"文字密度：{int(progress*100)}%")
        
        # 显示结果卡片
        self.result_card.pack(fill=tk.X, padx=5, pady=(0, 12))
        
        # 显示优先统计区域
        self.priority_frame.pack(fill=tk.X, padx=12, pady=(12, 0))
        
        # 清空旧的大统计
        for widget in self.chinese_big.winfo_children():
            widget.destroy()
        for widget in self.english_big.winfo_children():
            widget.destroy()
        
        # 创建大字显示 - 中文字数
        self.create_big_stat(
            self.chinese_big, 
            "🌱", 
            "中文字数", 
            stats["中文字数 🌱"],
            self.colors['primary']
        )
        
        # 创建大字显示 - 英文单词数
        self.create_big_stat(
            self.english_big, 
            "🔤", 
            "英文单词数", 
            stats["英文单词数 🔤"],
            self.colors['english_blue']
        )
        
        # 显示分隔线
        self.separator.pack(fill=tk.X, padx=12, pady=10)
        
        # 清空旧数据
        for widget in self.left_stats.winfo_children():
            widget.destroy()
        for widget in self.right_stats.winfo_children():
            widget.destroy()
        
        # 左侧次要统计
        left_items = [
            ("总字符数（含空格）", stats["总字符数（含空格）"]),
            ("总字符数（不含空格）", stats["总字符数（不含空格）"]),
            ("纯文字数", stats["纯文字数"]),
            ("数字个数", stats["数字个数"])
        ]
        
        for label, value in left_items:
            frame = tk.Frame(self.left_stats, bg=self.colors['bg_card'])
            frame.pack(fill=tk.X, pady=2)
            tk.Label(frame, text=f"{label}:", 
                    font=("微软雅黑", 10),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_secondary']).pack(side=tk.LEFT)
            tk.Label(frame, text=str(value), 
                    font=("微软雅黑", 10, "bold"),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text']).pack(side=tk.RIGHT)
        
        # 右侧次要统计
        right_items = [
            ("标点符号数", stats["标点符号数"]),
            ("段落数", stats["段落数"]),
            ("句子数", stats["句子数"]),
            ("行数", stats["行数"])
        ]
        
        for label, value in right_items:
            frame = tk.Frame(self.right_stats, bg=self.colors['bg_card'])
            frame.pack(fill=tk.X, pady=2)
            tk.Label(frame, text=f"{label}:", 
                    font=("微软雅黑", 10),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_secondary']).pack(side=tk.LEFT)
            tk.Label(frame, text=str(value), 
                    font=("微软雅黑", 10, "bold"),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text']).pack(side=tk.RIGHT)
        
        # 毛豆特色统计
        self.maodou_feature.pack(fill=tk.X, padx=12, pady=12)
        self.maodou_label.config(
            text=f"🫘 这些文字大约相当于 {stats['≈ 相当于多少颗毛豆 🫘']} 颗毛豆"
        )
        
        # 评价
        total = stats["总字符数（不含空格）"]
        chinese = stats["中文字数 🌱"]
        english = stats["英文单词数 🔤"]
        
        # 根据中英文比例给出不同评价
        if chinese > 0 and english > 0:
            if chinese > english * 3:
                comment = f"🌱 中文为主（{chinese}字），夹杂{english}个英文单词"
                comment_color = self.colors['primary']
            elif english > chinese:
                comment = f"🔤 英文为主（{english}词），夹杂{chinese}个汉字"
                comment_color = self.colors['english_blue']
            else:
                comment = f"🌏 中英混合，中文{chinese}字 + 英文{english}词，像毛豆炒肉"
                comment_color = self.colors['accent']
        elif chinese > 0:
            comment = "🌱 纯正中文，像一盘清炒毛豆"
            comment_color = self.colors['primary']
        elif english > 0:
            comment = "🔤 纯英文文本，毛豆在学外语"
            comment_color = self.colors['english_blue']
        else:
            comment = "🫘 只有数字和符号，毛豆有点懵"
            comment_color = self.colors['warm_gray']
        
        # 根据总量调整评价
        if total < 50:
            size_comment = "一小撮"
        elif total < 200:
            size_comment = "一小盘"
        elif total < 500:
            size_comment = "一大碗"
        else:
            size_comment = "一麻袋"
        
        self.comment_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        self.comment_label.config(
            text=f"{comment}，共{size_comment}（{total}字符）",
            fg=comment_color
        )
        
        # 详细数据
        self.detail_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        self.detail_text.config(state='normal')
        self.detail_text.delete(1.0, tk.END)
        
        # 优先显示中英文
        self.detail_text.insert(tk.END, f"{'中文字数 🌱':25s}: {stats['中文字数 🌱']:>8}\n")
        self.detail_text.insert(tk.END, f"{'英文单词数 🔤':25s}: {stats['英文单词数 🔤']:>8}\n")
        self.detail_text.insert(tk.END, "-" * 40 + "\n")
        
        # 其他数据
        for key, value in stats.items():
            if key not in ["中文字数 🌱", "英文单词数 🔤"]:
                self.detail_text.insert(tk.END, f"{key:25s}: {value:>8}\n")
        
        self.detail_text.config(state='disabled')
        
        # 滚动到结果区域
        self.main_canvas.update_idletasks()
        self.main_canvas.yview_moveto(0.4)
    
    def open_file(self):
        """打开文件"""
        file_path = filedialog.askopenfilename(
            title="🫘 选择文本文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.quote_label.config(text=f"🫘 成功倒入 {len(content)} 颗文字豆！")
                self.count_now()
            except Exception as e:
                messagebox.showerror("错误", f"🫘 毛豆读不懂这个文件：{str(e)}")
    
    def load_example(self):
        """加载示例"""
        example = """毛豆，学名大豆，是黄豆的嫩荚。
Edamame is the young pod of soybean.
毛豆炒肉、盐水毛豆、毛豆炖排骨...
每一个字都是一颗小毛豆，数一数这里有多少颗？

毛豆营养丰富，含有优质蛋白质。
Edamame is rich in protein and delicious!
夏天来一盘冰镇毛豆，配上啤酒，简直是人间美味！"""
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, example)
        self.quote_label.config(text="🫘 示例已填入（中英混合），点击'数豆子'看看吧")
    
    def clear(self):
        """清空"""
        self.text_area.delete(1.0, tk.END)
        self.result_card.pack_forget()
        self.progress_frame.pack_forget()
        self.quote_label.config(text=random.choice(maodou_quotes))

def main():
    try:
        root = tk.Tk()
        app = MaodouWordCounter(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"🫘 程序启动失败：\n{str(e)}\n\n{traceback.format_exc()}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()