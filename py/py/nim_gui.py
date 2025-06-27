import tkinter as tk
from tkinter import messagebox
import random
from nim import Nim, NimAI, train
import os
import pickle
# 新增导入playsound
try:
    import pygame
    pygame.mixer.init()
except ImportError:
    pygame = None

class NimGUI:
    def __init__(self, root):
        self.ai_after_id = None  # 必须在main_menu之前初始化
        self.root = root
        self.root.title("Nim吃汉堡 游戏 - Tkinter 版")
        from PIL import Image, ImageTk
        # 画布尺寸严格等于table.png原始尺寸
        self.table_img = Image.open("picture/table.png")
        self.table_width, self.table_height = self.table_img.size
        self.canvas_width = self.table_width
        self.canvas_height = self.table_height
        self.table_photo = ImageTk.PhotoImage(self.table_img)
        self.main_menu()
        self.last_spinbox_value = None

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def stop_music(self):
        if pygame:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"停止背景音乐失败: {e}")

    def main_menu(self):
        self.cancel_ai_timer()
        self.stop_music()  # 回到主界面时停止背景音乐
        self.clear_window()
        from PIL import Image, ImageTk
        cover_width, cover_height = 1600, 700
        cover_img = Image.open("picture/store.jpeg")
        cover_img.thumbnail((cover_width, cover_height), Image.LANCZOS)
        self.cover_photo = ImageTk.PhotoImage(cover_img)
        self.cover_canvas = tk.Canvas(self.root, width=cover_width, height=cover_height, highlightthickness=0)
        self.cover_canvas.pack()
        img_x = (cover_width - self.cover_photo.width()) // 2
        img_y = (cover_height - self.cover_photo.height()) // 2
        self.cover_canvas.create_image(img_x, img_y, anchor=tk.NW, image=self.cover_photo)
        title = tk.Label(self.root, text="吃汉堡", font=("微软雅黑", 32, "bold"), fg="#e17055", bg="#ffffff", bd=0)
        title.place(x=cover_width//2-60, y=60)
        # 难度选择区域底色（拉长1.5倍）
        diff_bg_x = cover_width//2-180
        diff_bg_y = 150
        diff_bg_w = 360
        diff_bg_h = 40
        self.cover_canvas.create_rectangle(diff_bg_x, diff_bg_y, diff_bg_x+diff_bg_w, diff_bg_y+diff_bg_h, fill="#f7f7fa", outline="#cccccc", width=2)
        self.difficulty = tk.StringVar(value="medium")
        diff_frame = tk.Frame(self.root, bg="#f7f7fa")
        diff_frame.place(x=diff_bg_x+10, y=diff_bg_y+7, width=diff_bg_w-20, height=diff_bg_h-14)
        tk.Label(diff_frame, text="选择难度：", font=("微软雅黑", 12, "bold"), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=(0,6))
        tk.Radiobutton(diff_frame, text="简单", variable=self.difficulty, value="easy", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="中等", variable=self.difficulty, value="medium", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="困难", variable=self.difficulty, value="hard", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="自定义", variable=self.difficulty, value="custom", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222", command=self.custom_mode_sequence).pack(side=tk.LEFT, padx=2)
        # 先手选择区域（拉长1.5倍）
        first_bg_x = cover_width//2-150
        first_bg_y = 210
        first_bg_w = 300
        first_bg_h = 36
        self.cover_canvas.create_rectangle(first_bg_x, first_bg_y, first_bg_x+first_bg_w, first_bg_y+first_bg_h, fill="#ffffff", outline="#cccccc", width=1)
        self.first_player = tk.StringVar(value="human")
        first_frame = tk.Frame(self.root, bg="#ffffff")
        first_frame.place(x=first_bg_x+10, y=first_bg_y+5, width=first_bg_w-20, height=first_bg_h-10)
        tk.Label(first_frame, text="选择先手：", font=("微软雅黑", 12, "bold"), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=(0,6))
        tk.Radiobutton(first_frame, text="玩家先手", variable=self.first_player, value="human", font=("微软雅黑", 11), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(first_frame, text="AI先手", variable=self.first_player, value="ai", font=("微软雅黑", 11), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=2)
        start_btn = tk.Button(self.root, text="开始游戏", font=("微软雅黑", 18), width=12, command=self.start_game)
        start_btn.place(x=cover_width//2-100, y=300)
        # 规则说明按钮恢复原大小和原位置
        rule_btn = tk.Button(self.root, text="规则说明", font=("微软雅黑", 7), width=5, command=self.show_rules)
        rule_btn.place(x=cover_width//2+120, y=305)
        exit_btn = tk.Button(self.root, text="退出", font=("微软雅黑", 18), width=12, command=self.root.quit)
        exit_btn.place(x=cover_width//2-100, y=380)
        self.custom_piles = None
        self.custom_stones = None
        self.custom_level = None

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def stop_music(self):
        if pygame:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"停止背景音乐失败: {e}")

    def main_menu(self):
        self.cancel_ai_timer()
        self.stop_music()  # 回到主界面时停止背景音乐
        self.clear_window()
        from PIL import Image, ImageTk
        cover_width, cover_height = 1600, 700
        cover_img = Image.open("picture/store.jpeg")
        cover_img.thumbnail((cover_width, cover_height), Image.LANCZOS)
        self.cover_photo = ImageTk.PhotoImage(cover_img)
        self.cover_canvas = tk.Canvas(self.root, width=cover_width, height=cover_height, highlightthickness=0)
        self.cover_canvas.pack()
        img_x = (cover_width - self.cover_photo.width()) // 2
        img_y = (cover_height - self.cover_photo.height()) // 2
        self.cover_canvas.create_image(img_x, img_y, anchor=tk.NW, image=self.cover_photo)
        title = tk.Label(self.root, text="吃汉堡", font=("微软雅黑", 32, "bold"), fg="#e17055", bg="#ffffff", bd=0)
        title.place(x=cover_width//2-60, y=60)
        # 难度选择区域底色（拉长1.5倍）
        diff_bg_x = cover_width//2-180
        diff_bg_y = 150
        diff_bg_w = 360
        diff_bg_h = 40
        self.cover_canvas.create_rectangle(diff_bg_x, diff_bg_y, diff_bg_x+diff_bg_w, diff_bg_y+diff_bg_h, fill="#f7f7fa", outline="#cccccc", width=2)
        self.difficulty = tk.StringVar(value="medium")
        diff_frame = tk.Frame(self.root, bg="#f7f7fa")
        diff_frame.place(x=diff_bg_x+10, y=diff_bg_y+7, width=diff_bg_w-20, height=diff_bg_h-14)
        tk.Label(diff_frame, text="选择难度：", font=("微软雅黑", 12, "bold"), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=(0,6))
        tk.Radiobutton(diff_frame, text="简单", variable=self.difficulty, value="easy", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="中等", variable=self.difficulty, value="medium", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="困难", variable=self.difficulty, value="hard", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(diff_frame, text="自定义", variable=self.difficulty, value="custom", font=("微软雅黑", 11), bg="#f7f7fa", fg="#222222", command=self.custom_mode_sequence).pack(side=tk.LEFT, padx=2)
        # 先手选择区域（拉长1.5倍）
        first_bg_x = cover_width//2-150
        first_bg_y = 210
        first_bg_w = 300
        first_bg_h = 36
        self.cover_canvas.create_rectangle(first_bg_x, first_bg_y, first_bg_x+first_bg_w, first_bg_y+first_bg_h, fill="#ffffff", outline="#cccccc", width=1)
        self.first_player = tk.StringVar(value="human")
        first_frame = tk.Frame(self.root, bg="#ffffff")
        first_frame.place(x=first_bg_x+10, y=first_bg_y+5, width=first_bg_w-20, height=first_bg_h-10)
        tk.Label(first_frame, text="选择先手：", font=("微软雅黑", 12, "bold"), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=(0,6))
        tk.Radiobutton(first_frame, text="玩家先手", variable=self.first_player, value="human", font=("微软雅黑", 11), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(first_frame, text="AI先手", variable=self.first_player, value="ai", font=("微软雅黑", 11), bg="#ffffff", fg="#222222").pack(side=tk.LEFT, padx=2)
        start_btn = tk.Button(self.root, text="开始游戏", font=("微软雅黑", 18), width=12, command=self.start_game)
        start_btn.place(x=cover_width//2-100, y=300)
        # 规则说明按钮恢复原大小和原位置
        rule_btn = tk.Button(self.root, text="规则说明", font=("微软雅黑", 7), width=5, command=self.show_rules)
        rule_btn.place(x=cover_width//2+120, y=305)
        exit_btn = tk.Button(self.root, text="退出", font=("微软雅黑", 18), width=12, command=self.root.quit)
        exit_btn.place(x=cover_width//2-100, y=380)
        self.custom_piles = None
        self.custom_stones = None
        self.custom_level = None

    def custom_mode_sequence(self):
        # 依次弹出堆数、棋子数、AI等级输入框
        self.get_custom_pile_count()

    def get_custom_pile_count(self):
        def on_ok():
            try:
                pile_count = int(entry.get())
                if pile_count < 1 or pile_count > 5:
                    raise ValueError
                self.custom_piles = pile_count
                popup.destroy()
                self.get_custom_stones()
            except:
                messagebox.showerror("错误", "请输入1-5之间的整数作为堆数")
        popup = tk.Toplevel(self.root)
        popup.title("自定义堆数")
        tk.Label(popup, text="请输入堆数(1-5)：", font=("微软雅黑", 14)).pack(padx=20, pady=10)
        entry = tk.Entry(popup, width=6)
        entry.pack(padx=20, pady=5)
        entry.focus()
        tk.Button(popup, text="确定", command=on_ok).pack(pady=10)

    def get_custom_stones(self):
        def on_ok():
            try:
                stones = [int(x) for x in entry.get().split(",") if x.strip()]
                if len(stones) != self.custom_piles:
                    raise ValueError
                if any(s < 1 or s > 30 for s in stones):
                    raise ValueError
                self.custom_stones = stones
                popup.destroy()
                self.get_custom_level()
            except:
                messagebox.showerror("错误", f"请输入{self.custom_piles}个1-30之间的整数，用逗号分隔")
        popup = tk.Toplevel(self.root)
        popup.title("自定义棋子数")
        tk.Label(popup, text=f"请输入每堆棋子数(共{self.custom_piles}堆，逗号分隔)：", font=("微软雅黑", 14)).pack(padx=20, pady=10)
        entry = tk.Entry(popup, width=20)
        entry.pack(padx=20, pady=5)
        entry.focus()
        tk.Button(popup, text="确定", command=on_ok).pack(pady=10)

    def get_custom_level(self):
        def on_ok():
            try:
                level = int(entry.get())
                if level < 1 or level > 20:
                    raise ValueError
                self.custom_level = level
                popup.destroy()
            except:
                messagebox.showerror("错误", "请输入1-20之间的整数作为AI等级")
        popup = tk.Toplevel(self.root)
        popup.title("自定义AI等级")
        tk.Label(popup, text="请输入AI等级(1-20)：", font=("微软雅黑", 14)).pack(padx=20, pady=10)
        entry = tk.Entry(popup, width=6)
        entry.pack(padx=20, pady=5)
        entry.focus()
        tk.Button(popup, text="确定", command=on_ok).pack(pady=10)

    def start_game(self):
        self.cancel_ai_timer()
        self.clear_window()
        # 播放并循环背景音乐（每次进入游戏界面都重新播放）
        if pygame:
            try:
                pygame.mixer.music.load("music/back.MP3")
                pygame.mixer.music.play(loops=-1)
            except Exception as e:
                print(f"播放背景音乐失败: {e}")
        difficulty = self.difficulty.get()
        if difficulty == "custom":
            # 检查自定义参数
            if not (self.custom_piles and self.custom_stones and self.custom_level):
                messagebox.showerror("错误", "请先输入自定义参数！")
                self.main_menu()
                return
            train_times = max(1000, 1000 * self.custom_level)
            piles = self.custom_stones
            self.ai = train(train_times, difficulty="custom", initial=piles)
            self.human_player = 0 if self.first_player.get() == "human" else 1
            self.selected_pile = None
            self.selected_count = 1
            self.game = Nim(initial=piles)
        else:
            qfile = f"ai_{difficulty}.pkl"
            if difficulty == "easy":
                train_times = 3000
            elif difficulty == "hard":
                train_times = 20000
            else:
                train_times = 5000
            self.ai = train(train_times, difficulty=difficulty)
            with open(qfile, "wb") as f:
                pickle.dump(self.ai, f)
            self.human_player = 0 if self.first_player.get() == "human" else 1
            self.selected_pile = None
            self.selected_count = 1
            self.init_random_game()
        self.status_label = tk.Label(self.root, text="你的回合，请点击棋堆", font=("微软雅黑", 16))
        self.status_label.pack(pady=10)
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#f5f6fa")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)
        self.count_label = tk.Label(self.action_frame, text="取走数量：", font=("微软雅黑", 18))
        self.count_label.pack(side=tk.LEFT)
        # 新的数量选择区：大号-按钮、Entry、大号+按钮
        self.minus_btn = tk.Button(self.action_frame, text="-", font=("微软雅黑", 18), width=2, command=self.decrease_count)
        self.minus_btn.pack(side=tk.LEFT, padx=2)
        self.count_var = tk.StringVar(value="1")
        self.count_entry = tk.Entry(self.action_frame, textvariable=self.count_var, font=("微软雅黑", 18), width=4, justify='center')
        self.count_entry.pack(side=tk.LEFT, padx=2)
        self.count_entry.bind('<KeyRelease>', lambda e: self.on_spin_change())
        self.count_entry.bind('<FocusOut>', lambda e: self.on_spin_change())
        self.plus_btn = tk.Button(self.action_frame, text="+", font=("微软雅黑", 18), width=2, command=self.increase_count)
        self.plus_btn.pack(side=tk.LEFT, padx=2)
        self.confirm_btn = tk.Button(self.action_frame, text="确认取走", font=("微软雅黑", 18), command=self.confirm_move)
        self.confirm_btn.pack(side=tk.LEFT, padx=10)
        self.reset_btn = tk.Button(self.action_frame, text="重新开始", font=("微软雅黑", 18), command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        self.back_btn = tk.Button(self.action_frame, text="返回主界面", font=("微软雅黑", 18), command=self.main_menu)
        self.back_btn.pack(side=tk.LEFT, padx=10)
        self.draw_piles()
        # 记录每堆初始汉堡胚索引
        self.bun_index = [pile-1 for pile in self.game.piles]
        self.update_status()
        # 如果AI先手，自动让AI走
        if self.human_player == 1:
            self.root.after(800, self.ai_move)

    def cancel_ai_timer(self):
        if self.ai_after_id is not None:
            try:
                self.root.after_cancel(self.ai_after_id)
            except Exception:
                pass
            self.ai_after_id = None

    def init_random_game(self):
        # 根据难度设置堆和棋子数
        mode = getattr(self, 'difficulty', None)
        if mode is not None:
            mode = mode.get()
        if mode == "easy":
            piles = [2, 4, 5]  # 异或和不为0
        elif mode == "hard":
            piles = [1, 3, 5, 7, 9]
        elif mode == "custom":
            if self.custom_stones:
                piles = self.custom_stones
            else:
                piles = [2, 4, 5, 8]  # 异或和不为0
        else:
            piles = [2, 4, 5, 8]  # 异或和不为0
        self.game = Nim(initial=piles)

    def get_pile_positions(self, pile_count):
        # 缩短间距，动态居中
        scale = 0.8
        offset_x = 30
        pile_spacing = int(180 * scale)  # 缩短间距
        pile_width = 0  # 棋子堆宽度可忽略，居中以间距为主
        total_width = (pile_count - 1) * pile_spacing
        start_x = (self.canvas_width - total_width) // 2
        return [start_x + i * pile_spacing for i in range(pile_count)]

    def draw_piles(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.table_photo)
        # 加载缩小后的图片并缩放（只加载一次）
        if not hasattr(self, 'img_meat_small'):
            from PIL import Image, ImageTk
            def load_and_resize(path, size):
                img = Image.open(path).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            scale = 0.8  # 缩小五分之一
            self.img_meat_small = load_and_resize("picture/burger.png", (int(80*scale), int(48*scale)))
            self.img_pineapple_small = load_and_resize("picture/pineapples.png", (int(80/0.729*scale), int(48/0.729*scale)))
            self.img_tomato_small = load_and_resize("picture/tomatoes.png", (int(80/0.729*scale), int(48/0.729*scale)))
            self.img_top_small = load_and_resize("picture/retro.png", (int(80*1.1*scale), int(48*1.1*scale)))
            self.img_bottom_small = load_and_resize("picture/retro-2.png", (int(80*1.1*scale), int(48*1.1*scale)))
            self.img_turner_player_small = load_and_resize("picture/turner-2.png", (int(32*scale), int(32*scale)))
            self.img_turner_ai_small = load_and_resize("picture/turner.png", (int(32*scale), int(32*scale)))
        # 偏移量
        offset_y = 30
        scale = 0.8
        pile_positions = self.get_pile_positions(len(self.game.piles))
        overlap_normal = int(16 * scale)
        overlap_selected = int(32 * scale)
        for i, pile in enumerate(self.game.piles):
            x = pile_positions[i]
            y_list = []
            y_base = 500
            y_base = int(y_base * scale) + offset_y
            # 选中堆时，取count_var的值，否则为0
            try:
                selected_count = int(self.count_var.get()) if (self.selected_pile == i and self.game.player == self.human_player) else 0
            except Exception:
                selected_count = 0
            for j in range(pile):
                is_selected = (self.selected_pile == i and self.game.player == self.human_player and j >= pile - selected_count)
                overlap = overlap_selected if is_selected else overlap_normal
                if j == 0:
                    y_list.append(y_base)
                else:
                    y_list.append(y_list[-1] - overlap)
            for j in range(pile):
                y = y_list[j]
                mark_selected = (self.selected_pile == i and self.game.player == self.human_player and j == pile - selected_count and selected_count > 0)
                if j == 0:
                    self.canvas.create_image(x, y, image=self.img_top_small)
                elif j == pile - 1:
                    self.canvas.create_image(x, y, image=self.img_bottom_small)
                else:
                    img_list = [self.img_meat_small, self.img_pineapple_small, self.img_tomato_small]
                    img = img_list[(j-1) % 3]
                    self.canvas.create_image(x, y, image=img)
                if mark_selected:
                    self.canvas.create_image(x+int(54*0.8), y+int(12*0.8), image=self.img_turner_player_small)
            self.canvas.create_text(x, y_base+int(40*0.8), text=f"第{i}堆  {pile}个", font=("微软雅黑", int(24*0.8)), fill="#222222")

    def play_click(self):
        if pygame:
            try:
                effect = pygame.mixer.Sound("music/click.MP3")
                effect.set_volume(1.0)
                effect.play()
            except Exception as e:
                print(f"播放点击音效失败: {e}")

    def decrease_count(self):
        # -按钮，减少数量
        try:
            val = int(self.count_var.get())
        except Exception:
            val = 1
        min_val = 1
        max_val = self.get_selected_pile_max()
        if val > min_val:
            val -= 1
        self.count_var.set(str(val))
        self.on_spin_change()

    def increase_count(self):
        # +按钮，增加数量
        try:
            val = int(self.count_var.get())
        except Exception:
            val = 1
        min_val = 1
        max_val = self.get_selected_pile_max()
        if val < max_val:
            val += 1
        self.count_var.set(str(val))
        self.on_spin_change()

    def get_selected_pile_max(self):
        # 获取当前选中堆最大可选数量
        if self.selected_pile is not None and 0 <= self.selected_pile < len(self.game.piles):
            return self.game.piles[self.selected_pile]
        return 1

    def on_canvas_click(self, event):
        if self.game.winner is not None or self.game.player != self.human_player:
            return
        scale = 0.8
        pile_spacing = int(180 * scale)
        pile_count = len(self.game.piles)
        total_width = (pile_count - 1) * pile_spacing
        start_x = (self.canvas_width - total_width) // 2
        for i in range(pile_count):
            x = start_x + i * pile_spacing
            if abs(event.x - x) < int(60 * scale):
                if self.game.piles[i] > 0:
                    self.selected_pile = i
                    # 选中堆后，最大数量自动调整
                    self.count_var.set("1")
                    self.on_spin_change()
                    self.play_click()  # 播放点击音效
                    self.draw_piles()
                break

    def confirm_move(self):
        if self.game.winner is not None or self.game.player != self.human_player:
            return
        if self.selected_pile is None:
            messagebox.showinfo("提示", "请先点击选择一个棋堆")
            return
        try:
            count = int(self.count_var.get())
        except Exception:
            count = 1
        # 先锁定所有棋子的y坐标（带缩放和偏移，和draw_piles完全一致）
        self.pile_y_lists = []
        scale = 0.8
        offset_y = 30
        overlap_normal = int(16 * scale)
        overlap_selected = int(32 * scale)
        for i, pile in enumerate(self.game.piles):
            y_list = []
            y_base = 500
            y_base = int(y_base * scale) + offset_y
            selected_count = count if (self.selected_pile == i and self.game.player == self.human_player) else 0
            for j in range(pile):
                is_selected = (self.selected_pile == i and self.game.player == self.human_player and j >= pile - selected_count)
                overlap = overlap_selected if is_selected else overlap_normal
                if j == 0:
                    y_list.append(y_base)
                else:
                    y_list.append(y_list[-1] - overlap)
            self.pile_y_lists.append(y_list)
        self.animate_collapse(self.selected_pile, count)

    def play_remove_sound(self, count):
        if pygame:
            try:
                if count <= 4:
                    effect = pygame.mixer.Sound("music/short.MP3")
                else:
                    effect = pygame.mixer.Sound("music/long.MP3")
                effect.set_volume(1.0)
                effect.play()
            except Exception as e:
                print(f"播放消失音效失败: {e}")

    def animate_collapse(self, pile, count, step=0):
        if step == 0:
            self.play_remove_sound(count)
        # 使用锁定的y坐标列表进行动画
        if step < count:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.table_photo)
            temp_piles = self.game.piles.copy()
            scale = 0.8
            offset_y = 30
            pile_positions = self.get_pile_positions(len(temp_piles))
            for i, pile_count in enumerate(temp_piles):
                x = pile_positions[i]
                y_list = self.pile_y_lists[i]
                remain = pile_count - step if (i == pile) else pile_count
                # 防止remain大于y_list长度
                remain = min(remain, len(y_list))
                for j in range(remain):
                    y = y_list[j]
                    if j == 0:
                        self.canvas.create_image(x, y, image=self.img_top_small)
                    elif j == remain - 1:
                        self.canvas.create_image(x, y, image=self.img_bottom_small)
                    else:
                        img_list = [self.img_meat_small, self.img_pineapple_small, self.img_tomato_small]
                        img = img_list[(j-1) % 3]
                        self.canvas.create_image(x, y, image=img)
                # 始终显示棋堆名字和棋子数，位置用y_list[0]或y_base
                if len(y_list) > 0:
                    name_y = y_list[0] + int(40*scale)
                else:
                    # 如果该堆已空，仍然显示在原始y_base位置
                    y_base = 500
                    name_y = int(y_base * scale) + offset_y + int(40*scale)
                self.canvas.create_text(x, name_y, text=f"第{i}堆  {remain}个", font=("微软雅黑", int(24*scale)), fill="#222222")
            self.ai_after_id = self.root.after(150, lambda: self.animate_collapse(pile, count, step+1))
        else:
            try:
                self.game.move((pile, count))
                self.selected_pile = None
                self.pile_y_lists = None
                self.draw_piles()
                if self.game.winner is not None:
                    self.root.after(2000, self.update_status)  # 延迟2秒再判定胜负
                else:
                    self.update_status()
                    self.root.after(600, self.ai_move)
            except Exception as e:
                messagebox.showerror("错误", str(e))

    def ai_move(self):
        if self.game.winner is not None or self.game.player == self.human_player:
            return
        action = self.ai.choose_action(self.game.piles, epsilon=False)
        if action:
            pile, count = action
            # 先高亮AI要取的棋子为紫色
            self.highlight_ai_choice(pile, count)
            # 2秒后再执行动画
            def do_ai_animate():
                # 先锁定所有棋子的y坐标（带缩放和偏移，和draw_piles完全一致）
                self.pile_y_lists = []
                scale = 0.8
                offset_y = 30
                overlap_normal = int(16 * scale)
                overlap_selected = int(32 * scale)
                for i, pile_num in enumerate(self.game.piles):
                    y_list = []
                    y_base = 500
                    y_base = int(y_base * scale) + offset_y
                    ai_selected_count = count if i == pile else 0
                    for j in range(pile_num):
                        is_selected = (i == pile and j >= pile_num - ai_selected_count)
                        overlap = overlap_selected if is_selected else overlap_normal
                        if j == 0:
                            y_list.append(y_base)
                        else:
                            y_list.append(y_list[-1] - overlap)
                    self.pile_y_lists.append(y_list)
                self.animate_collapse(pile, count)
            self.ai_after_id = self.root.after(2000, do_ai_animate)

    def highlight_ai_choice(self, pile, count):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.table_photo)
        if not hasattr(self, 'img_meat_small'):
            from PIL import Image, ImageTk
            def load_and_resize(path, size):
                img = Image.open(path).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            scale = 0.8
            self.img_meat_small = load_and_resize("picture/burger.png", (int(80*scale), int(48*scale)))
            self.img_pineapple_small = load_and_resize("picture/pineapples.png", (int(80/0.729*scale), int(48/0.729*scale)))
            self.img_tomato_small = load_and_resize("picture/tomatoes.png", (int(80/0.729*scale), int(48/0.729*scale)))
            self.img_top_small = load_and_resize("picture/retro.png", (int(80*1.1*scale), int(48*1.1*scale)))
            self.img_bottom_small = load_and_resize("picture/retro-2.png", (int(80*1.1*scale), int(48*1.1*scale)))
            self.img_turner_player_small = load_and_resize("picture/turner-2.png", (int(32*scale), int(32*scale)))
            self.img_turner_ai_small = load_and_resize("picture/turner.png", (int(32*scale), int(32*scale)))
        scale = 0.8
        offset_y = 30
        pile_positions = self.get_pile_positions(len(self.game.piles))
        overlap_normal = int(16 * scale)
        overlap_selected = int(32 * scale)
        for i, pile_count in enumerate(self.game.piles):
            x = pile_positions[i]
            y_list = []
            y_base = 500
            y_base = int(y_base * scale) + offset_y
            ai_selected_count = count if i == pile else 0
            for j in range(pile_count):
                is_selected = (i == pile and j >= pile_count - ai_selected_count)
                overlap = overlap_selected if is_selected else overlap_normal
                if j == 0:
                    y_list.append(y_base)
                else:
                    y_list.append(y_list[-1] - overlap)
            for j in range(pile_count):
                y = y_list[j]
                mark_ai = (i == pile and j == pile_count - ai_selected_count and ai_selected_count > 0)
                if j == 0:
                    self.canvas.create_image(x, y, image=self.img_top_small)
                elif j == pile_count - 1:
                    self.canvas.create_image(x, y, image=self.img_bottom_small)
                else:
                    img_list = [self.img_meat_small, self.img_pineapple_small, self.img_tomato_small]
                    img = img_list[(j-1) % 3]
                    self.canvas.create_image(x, y, image=img)
                if mark_ai:
                    self.canvas.create_image(x-int(54*0.8), y+int(12*0.8), image=self.img_turner_ai_small)
            self.canvas.create_text(x, y_base+int(40*scale), text=f"第{i}堆  {pile_count}个", font=("微软雅黑", int(24*scale)), fill="#222222")

    def play_music(self, path):
        if pygame:
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"播放音乐失败: {e}")

    def play_effect(self, path):
        if pygame:
            try:
                effect = pygame.mixer.Sound(path)
                effect.set_volume(1.0)  # 设置音效为最大音量
                effect.play()
            except Exception as e:
                print(f"播放音效失败: {e}")

    def update_status(self):
        if self.game.winner is not None:
            winner = "你" if self.game.winner == self.human_player else "AI"
            self.status_label.config(text=f"游戏结束，胜者是：{winner}")
            # 播放胜负音效（不会打断背景音乐）
            if winner == "你":
                self.play_effect("music/win.MP3")
            else:
                self.play_effect("music/lose.MP3")
            # 弹窗反馈，带“是否继续游戏”
            if winner == "你":
                msg = "恭喜你获胜！\n是否继续游戏？"
            else:
                msg = "很遗憾，AI 获胜！\n是否继续游戏？"
            res = messagebox.askyesno("游戏结束", msg)
            if res:
                self.reset_game()
            else:
                self.main_menu()
        elif self.game.player == self.human_player:
            self.status_label.config(text="你的回合，请点击棋堆")
        else:
            self.status_label.config(text="AI回合，请稍候...")

    def on_spin_change(self):
        self.draw_piles()

    def reset_game(self):
        self.cancel_ai_timer()
        self.init_random_game()
        self.selected_pile = None
        self.selected_count = 1
        # 保证每次重新开始后，先手方和本局一致
        self.game.player = self.human_player
        self.draw_piles()
        # 重置汉堡胚索引
        self.bun_index = [pile-1 for pile in self.game.piles]
        self.update_status()
        # 修复：AI先手时自动让AI走第一步
        if self.human_player == 1:
            self.ai_after_id = self.root.after(800, self.ai_move)

    def show_rules(self):
        rules = (
            "【Nim 汉堡游戏规则】\n\n"
            "1. 有若干堆汉堡，每堆有若干层。\n"
            "2. 玩家和AI轮流操作，每次只能从一堆中取走至少1层汉堡。\n"
            "3. 取走的数量不限，但只能取同一堆。\n"
            "4. 谁拿走最后一层汉堡，谁输掉本局。\n"
            "5. 你可以选择难度和先手，体验不同策略乐趣！"
        )
        self.root.after(100, lambda: messagebox.showinfo("规则说明", rules))
        self.root.after(200, lambda: self.root.focus_force())
