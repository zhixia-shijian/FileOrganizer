import os
import shutil
import re
import threading
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文件整理工具")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 配置按钮样式 - 只改变字体颜色，保持原有按钮颜色
        style.configure('TButton', 
                       foreground='black',  # 改变字体颜色为黑色
                       font=('Microsoft YaHei', 10, 'bold'))
        
        # 配置框架样式
        style.configure('Card.TFrame', 
                       background='#F8F8F8',
                       relief='solid',
                       borderwidth=1)
        
        # 设置根窗口背景色
        self.root.configure(bg='white')
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_container, 
                              text="文件整理工具", 
                              font=('Microsoft YaHei', 16, 'bold'),
                              bg='white',
                              fg='black')  # 改为黑色
        title_label.pack(pady=(0, 5))
        
        # 副标题
        subtitle_label = tk.Label(main_container, 
                                 text="将相似文件自动归类到对应文件夹", 
                                 font=('Microsoft YaHei', 10),
                                 fg='#333333',  # 深灰色，更清晰
                                 bg='white')
        subtitle_label.pack(pady=(0, 20))
        
        # 目录选择卡片
        dir_card = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        dir_card.pack(fill=tk.X, pady=(0, 10))
        
        dir_label = tk.Label(dir_card, 
                           text="选择要整理的目录：", 
                           font=('Microsoft YaHei', 10),
                           bg='#F8F8F8',
                           fg='black')  # 改为黑色
        dir_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 目录输入框和按钮容器
        dir_input_container = ttk.Frame(dir_card)
        dir_input_container.pack(fill=tk.X)
        
        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_input_container, 
                             textvariable=self.dir_var, 
                             font=('Microsoft YaHei', 9),
                             foreground='black',  # 输入框文字颜色
                             width=35)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_input_container, 
                               text="浏览", 
                               style='TButton',
                               command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)
        
        # 选项卡片
        options_card = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        options_card.pack(fill=tk.X, pady=(0, 10))
        
        self.recursive_var = tk.BooleanVar()
        # 使用普通的tk.Checkbox，并设置字体颜色
        recursive_check = tk.Checkbutton(options_card, 
                                       text="递归处理子目录", 
                                       variable=self.recursive_var,
                                       font=('Microsoft YaHei', 10),
                                       bg='#F8F8F8',
                                       fg='black',  # 改为黑色
                                       selectcolor='#F8F8F8',
                                       activebackground='#F8F8F8',
                                       activeforeground='black')
        recursive_check.pack(anchor=tk.W)
        
        # 按钮容器
        button_container = ttk.Frame(main_container)
        button_container.pack(fill=tk.X, pady=(10, 10))
        
        self.organize_btn = ttk.Button(button_container,
                                      text="开始整理",
                                      style='TButton',
                                      state='disabled',
                                      command=self.start_organize)
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.decompose_btn = ttk.Button(button_container,
                                       text="分解到根目录",
                                       style='TButton',
                                       state='disabled',
                                       command=self.start_decompose)
        self.decompose_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = ttk.Button(button_container,
                             text="退出",
                             style='TButton',
                             command=self.root.quit)
        exit_btn.pack(side=tk.LEFT)
        
        # 状态标签
        self.status_label = tk.Label(main_container, 
                                   text="状态：准备就绪", 
                                   font=('Microsoft YaHei', 9),
                                   fg='black',  # 改为黑色
                                   bg='white')
        self.status_label.pack(pady=(0, 5))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_container, 
                                          variable=self.progress_var, 
                                          maximum=100,
                                          length=400)
        self.progress_bar.pack(pady=(0, 10))
        
        # 日志区域
        log_label = tk.Label(main_container, 
                           text="操作日志", 
                           font=('Microsoft YaHei', 10, 'bold'),
                           bg='white',
                           fg='black')  # 改为黑色
        log_label.pack(anchor=tk.W, pady=(0, 5))
        
        log_frame = ttk.Frame(main_container, style='Card.TFrame', padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 height=8, 
                                                 width=45,
                                                 font=('Microsoft YaHei', 9),
                                                 bg='#F8F8F8',
                                                 fg='black',  # 改为黑色
                                                 wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory(
            title="选择要整理的目录",
            initialdir=os.getcwd()
        )
        
        if directory:
            self.dir_var.set(directory)
            self.organize_btn.config(state='normal')
            self.decompose_btn.config(state='normal')
            self.status_label.config(text="状态：目录已选择")
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"已选择目录：{directory}\n")
    
    def start_organize(self):
        """开始整理文件"""
        directory_path = self.dir_var.get()
        recursive = self.recursive_var.get()
        
        if not directory_path:
            messagebox.showerror("错误", "请先选择要整理的目录！")
            return
        
        # 禁用开始按钮
        self.organize_btn.config(state='disabled')
        
        # 重置进度条
        self.progress_var.set(0)
        self.status_label.config(text="状态：正在整理文件...")
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"开始整理目录：{directory_path}\n")
        
        # 在线程中执行文件整理
        thread = threading.Thread(target=self.organize_files_thread, 
                                args=(directory_path, recursive),
                                daemon=True)
        thread.start()
    
    def organize_files_thread(self, directory_path, recursive):
        """在线程中执行文件整理"""
        try:
            success, message = self.organize_files(directory_path, recursive)
            
            # 在主线程中更新UI
            self.root.after(0, self.organize_finished, success, message)
            
        except Exception as e:
            self.root.after(0, self.organize_finished, False, f"程序执行出错：{str(e)}")
    
    def organize_files(self, directory_path, recursive=False):
        """执行文件整理"""
        try:
            directory_path = Path(directory_path).resolve()
            
            if not directory_path.exists():
                return False, f"目录不存在：{directory_path}"
            
            if not directory_path.is_dir():
                return False, f"路径不是目录：{directory_path}"
            
            # 获取文件列表
            if recursive:
                file_list = []
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_list.append(Path(root) / file)
            else:
                file_list = [f for f in directory_path.iterdir() if f.is_file()]
            
            if not file_list:
                return True, "该目录下没有找到文件！"
            
            # 获取脚本文件名
            try:
                script_name = os.path.basename(__file__)
            except NameError:
                script_name = "file_organizer_gui_fontcolor.py"
            
            # 按基础名称分组文件
            file_groups = {}
            total_files = len(file_list)
            processed_files = 0
            
            for file_path in file_list:
                file_name = file_path.name
                
                # 跳过隐藏文件和系统文件
                if file_name.startswith('.') or file_name.startswith('~'):
                    continue
                
                # 跳过脚本文件本身
                if file_name == script_name:
                    continue
                
                base_name = self.extract_base_name(file_name)
                if not base_name:
                    continue
                
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(file_path)
                
                processed_files += 1
                progress = int((processed_files / total_files) * 50)
                self.root.after(0, self.update_progress, progress, f"扫描文件：{file_name}")
            
            organized_count = 0
            total_groups = len(file_groups)
            
            # 处理每个文件组
            for i, (base_name, file_paths) in enumerate(file_groups.items()):
                try:
                    target_folder = directory_path / base_name
                    
                    if not target_folder.exists():
                        target_folder.mkdir(parents=True, exist_ok=True)
                        self.root.after(0, self.update_log, f"创建文件夹：{target_folder}")
                    
                    for file_path in file_paths:
                        file_name = file_path.name
                        target_file_path = target_folder / file_name
                        
                        if file_path == target_file_path:
                            continue
                        
                        # 处理文件名冲突
                        counter = 1
                        while target_file_path.exists():
                            file_stem = file_path.stem
                            file_ext = file_path.suffix
                            new_name = f"{file_stem}_{counter}{file_ext}"
                            target_file_path = target_folder / new_name
                            counter += 1
                        
                        shutil.move(str(file_path), str(target_file_path))
                        self.root.after(0, self.update_log, f"移动：{file_name} -> {base_name}")
                        organized_count += 1
                        
                except Exception as e:
                    self.root.after(0, self.update_log, f"处理文件夹 {base_name} 时出错：{str(e)}")
                    continue
                
                progress = 50 + int(((i + 1) / total_groups) * 50)
                self.root.after(0, self.update_progress, progress, f"整理文件夹：{base_name}")
            
            return True, f"整理完成！成功整理 {organized_count} 个文件到 {len(file_groups)} 个文件夹"
            
        except Exception as e:
            return False, f"程序执行出错：{str(e)}"
    
    def extract_base_name(self, filename):
        """从文件名中提取基础名称（综合解决方案）"""
        # 移除文件扩展名
        name_without_ext = os.path.splitext(filename)[0]
        
        # 步骤1：移除@符号及其后的所有内容
        name_without_ext = re.sub(r'@.*$', '', name_without_ext)
        
        # 步骤2：移除中文引号
        name_without_ext = re.sub(r'[「」]', '', name_without_ext)
        
        # 步骤3：检查是否包含CJK字符（中文、日文、韩文）
        has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7a3]', name_without_ext))
        
        if has_cjk:
            # 对于包含CJK字符的文件名，使用新算法
            # 移除常见的修饰词和数字后缀
            patterns_to_remove = [
                r'[ 　]*第\d+[話集章节回]',
                r'[ 　]*\d+[話集章节回]',
                r'[ 　]*\d+$',
                r'[ 　]*[上下中前后全][話集章节回]',
                r'[ 　]*总导航',
                r'[ 　]*导航',
                r'[ 　]*介绍',
                r'[ 　]*预告',
                r'[ 　]*宣传',
                r'[ 　]*特别篇',
                r'[ 　]*番外',
                r'[ 　]*OVA',
                r'[ 　]*OAD',
                r'[ 　]*SP',
            ]
            
            for pattern in patterns_to_remove:
                name_without_ext = re.sub(pattern, '', name_without_ext)
            
            # 提取最长的CJK字符串
            cjk_chars = re.findall(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7a3]+', name_without_ext)
            if cjk_chars:
                base_name = max(cjk_chars, key=len)
            else:
                base_name = name_without_ext
        else:
            # 对于纯英文/数字文件名，使用原有算法
            # 处理空格
            name_without_ext = re.sub(r'\s+', ' ', name_without_ext).strip()
            
            # 处理特殊符号
            name_without_ext = re.sub(r'[!#$%^&*()+=\[\]{}|;:\'",.<>?/~`\\-]+', '_', name_without_ext)
            name_without_ext = re.sub(r'_+', '_', name_without_ext)
            name_without_ext = name_without_ext.strip('_')
            
            # 应用后缀移除模式
            suffix_patterns = [
                r'[_\-\s]v\d+\.?\d*\b',
                r'[_\-\s]\d+\.?\d*\b',
                r'[_\-\s]final\b',
                r'[_\-\s]draft\b',
                r'[_\-\s]copy\b',
                r'[_\-\s]old\b',
                r'[_\-\s]new\b',
                r'[_\-\s]backup\b',
                r'[_\-\s]\d{8}\b',
                r'\(\d+\)',
                r'\(.*?\)',
                r'\[.*?\]',
            ]
            
            changed = True
            base_name = name_without_ext
            while changed:
                changed = False
                for pattern in suffix_patterns:
                    new_name = re.sub(pattern, '', base_name, flags=re.IGNORECASE)
                    if new_name != base_name:
                        base_name = new_name
                        changed = True
            
            # 处理颠倒文件名
            if '_' in base_name:
                parts = base_name.split('_')
                if len(parts) >= 2:
                    filtered_parts = []
                    for part in parts:
                        if part and not part.isdigit():
                            part = re.sub(r'\d+$', '', part)
                            if part:
                                filtered_parts.append(part)
                    
                    if filtered_parts:
                        sorted_parts = sorted(filtered_parts, key=lambda x: x.lower())
                        base_name = '_'.join(sorted_parts)
        
        # 最终清理
        base_name = re.sub(r'[\d、，,@\.\s]+$', '', base_name)
        base_name = re.sub(r'[_\-\s]+$', '', base_name)
        base_name = re.sub(r'[.、，,]+$', '', base_name)
        base_name = base_name.strip()
        
        return base_name
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_var.set(value)
        self.status_label.config(text=f"状态：{message}")
    
    def update_log(self, message):
        """更新日志"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def organize_finished(self, success, message):
        """整理完成"""
        self.progress_var.set(100)
        self.status_label.config(text="状态：整理完成")
        self.organize_btn.config(state='normal')
        self.decompose_btn.config(state='normal')
        
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        if success:
            messagebox.showinfo("完成", message)
        else:
            messagebox.showerror("错误", message)
    
    def start_decompose(self):
        """开始分解文件到根目录"""
        directory_path = self.dir_var.get()
        
        if not directory_path:
            messagebox.showerror("错误", "请先选择要处理的目录！")
            return
        
        # 禁用按钮
        self.organize_btn.config(state='disabled')
        self.decompose_btn.config(state='disabled')
        
        # 重置进度条
        self.progress_var.set(0)
        self.status_label.config(text="状态：正在分解文件到根目录...")
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"开始分解目录：{directory_path}\n")
        
        # 在线程中执行文件分解
        thread = threading.Thread(target=self.decompose_files_thread,
                                args=(directory_path,),
                                daemon=True)
        thread.start()
    
    def decompose_files_thread(self, directory_path):
        """在线程中执行文件分解"""
        try:
            success, message = self.decompose_files(directory_path)
            
            # 在主线程中更新UI
            self.root.after(0, self.decompose_finished, success, message)
            
        except Exception as e:
            self.root.after(0, self.decompose_finished, False, f"程序执行出错：{str(e)}")
    
    def decompose_files(self, directory_path):
        """执行文件分解到根目录（递归处理嵌套文件夹）"""
        try:
            directory_path = Path(directory_path).resolve()
            
            if not directory_path.exists():
                return False, f"目录不存在：{directory_path}"
            
            if not directory_path.is_dir():
                return False, f"路径不是目录：{directory_path}"
            
            # 收集所有需要处理的文件夹（包括嵌套文件夹）
            all_folders = []
            for root, dirs, files in os.walk(directory_path):
                # 跳过根目录本身
                if Path(root) == directory_path:
                    continue
                all_folders.append(Path(root))
            
            if not all_folders:
                return True, "该目录下没有找到子文件夹！"
            
            total_folders = len(all_folders)
            moved_files = 0
            empty_folders_removed = 0
            
            # 按路径深度排序，从最深层的文件夹开始处理
            all_folders.sort(key=lambda x: len(str(x)), reverse=True)
            
            # 处理每个文件夹（包括嵌套文件夹）
            for i, folder in enumerate(all_folders):
                try:
                    # 计算相对于根目录的路径
                    relative_path = folder.relative_to(directory_path)
                    folder_display_name = str(relative_path)
                    
                    # 跳过隐藏文件夹
                    if folder.name.startswith('.') or folder.name.startswith('~'):
                        continue
                    
                    # 获取文件夹中的所有文件
                    files_in_folder = [f for f in folder.iterdir() if f.is_file()]
                    
                    if not files_in_folder:
                        # 如果是空文件夹，尝试删除
                        try:
                            folder.rmdir()
                            self.root.after(0, self.update_log, f"删除空文件夹：{folder_display_name}")
                            empty_folders_removed += 1
                        except:
                            pass  # 文件夹非空或其他错误，跳过
                        continue
                    
                    # 移动文件到根目录
                    for file_path in files_in_folder:
                        file_name = file_path.name
                        
                        # 跳过隐藏文件和系统文件
                        if file_name.startswith('.') or file_name.startswith('~'):
                            continue
                        
                        target_file_path = directory_path / file_name
                        
                        # 处理文件名冲突
                        counter = 1
                        original_stem = file_path.stem
                        original_ext = file_path.suffix
                        
                        while target_file_path.exists():
                            new_name = f"{original_stem}_{counter}{original_ext}"
                            target_file_path = directory_path / new_name
                            counter += 1
                        
                        # 移动文件
                        shutil.move(str(file_path), str(target_file_path))
                        self.root.after(0, self.update_log, f"移动：{folder_display_name}/{file_name} -> {target_file_path.name}")
                        moved_files += 1
                    
                    # 尝试删除空文件夹（如果所有文件都已移出）
                    try:
                        # 检查文件夹是否为空
                        remaining_items = list(folder.iterdir())
                        if not remaining_items:
                            folder.rmdir()
                            self.root.after(0, self.update_log, f"删除空文件夹：{folder_display_name}")
                            empty_folders_removed += 1
                    except:
                        pass  # 文件夹非空或其他错误，跳过
                    
                except Exception as e:
                    self.root.after(0, self.update_log, f"处理文件夹 {folder_display_name} 时出错：{str(e)}")
                    continue
                
                # 更新进度
                progress = int(((i + 1) / total_folders) * 100)
                self.root.after(0, self.update_progress, progress, f"处理文件夹：{folder_display_name}")
            
            message = f"分解完成！成功移动 {moved_files} 个文件到根目录"
            if empty_folders_removed > 0:
                message += f"，删除了 {empty_folders_removed} 个空文件夹"
            
            return True, message
            
        except Exception as e:
            return False, f"程序执行出错：{str(e)}"
    
    def decompose_finished(self, success, message):
        """分解完成"""
        self.progress_var.set(100)
        self.status_label.config(text="状态：分解完成")
        self.organize_btn.config(state='normal')
        self.decompose_btn.config(state='normal')
        
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        if success:
            messagebox.showinfo("完成", message)
        else:
            messagebox.showerror("错误", message)

def main():
    """主函数"""
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()