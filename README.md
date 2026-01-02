# File Organizer GUI

一个功能强大的桌面应用程序，用于智能整理和分类文件，支持复杂文件名处理和嵌套文件夹分解。

![文件整理工具](folder_organizer_gui.ico)

## ✨ 功能特性

### 🗂️ 智能文件整理
- 自动识别相似文件名并归类到对应文件夹
- 支持中文、日文、英文混合文件名
- 智能处理版本后缀、特殊符号和颠倒文件名

### 🔄 文件分解到根目录
- 将嵌套文件夹中的文件移动到根目录
- 支持多层嵌套文件夹结构
- 自动删除空文件夹，智能处理文件名冲突

### 🖥️ 用户友好界面
- 直观的图形用户界面
- 实时进度显示和操作日志
- 多线程处理，避免界面卡顿

## 🚀 快速开始

### 方式一：使用可执行文件（推荐）
1. 下载 [FileOrganizerGUI.exe](dist/FileOrganizerGUI.exe)
2. 双击运行即可使用
3. 无需安装Python环境

### 方式二：运行Python脚本
```bash
# 运行程序
python mian.py
```

## 📋 使用说明

1. **启动程序**：双击 `FileOrganizerGUI.exe` 或运行 `python mian.py`
2. **选择目录**：点击"浏览"按钮选择要整理的文件夹
3. **选择功能**：
   - **开始整理**：将相似文件归类到文件夹
   - **分解到根目录**：将子文件夹中的文件移动到根目录
4. **查看结果**：进度条显示处理进度，日志区域显示详细操作记录

## 📁 项目结构

```
文件整理工具/
├── mian.py                    # 主程序文件
├── build_gui_exe.py           # 打包脚本
├── create_icon.py             # 图标创建脚本
├── FileOrganizerGUI.spec      # PyInstaller配置文件
├── folder_organizer_gui.ico   # 应用程序图标
├── version_info.txt           # 版本信息
├── dist/
│   └── FileOrganizerGUI.exe   # 可执行文件
└── README.md                  # 本文档
```

## 🔧 技术细节

### 核心算法
- **智能CJK字符识别**：自动检测中文、日文、韩文字符
- **复杂文件名解析**：处理@符号、中文引号、版本后缀等
- **嵌套文件夹处理**：递归遍历所有文件夹，按深度排序处理

### 打包信息
- **打包工具**：PyInstaller 6.16.0
- **文件大小**：8.6 MB
- **运行环境**：Windows 10/11
- **依赖**：无需Python环境，独立运行

## 📦 打包说明

```bash
# 运行打包脚本
python build_gui_exe.py

# 或手动打包
pyinstaller --onefile --windowed --icon=folder_organizer_gui.ico --name=FileOrganizerGUI mian.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request


## ⚠️ 注意事项

- 使用前建议备份重要文件
- 本工具按"原样"提供，作者不对使用造成的任何数据丢失负责

---

**提示**：程序支持递归处理子目录，勾选"递归处理子目录"选项即可。