from PIL import Image, ImageDraw, ImageFont
import os

def create_folder_icon():
    """创建一个文件夹图标"""
    # 创建256x256的图像
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制文件夹主体（黄色渐变）
    folder_color = (255, 193, 7)  # 黄色
    
    # 文件夹主体
    draw.rectangle([20, 60, 236, 220], fill=folder_color, outline=(255, 152, 0), width=2)
    
    # 文件夹标签
    draw.polygon([20, 60, 100, 60, 120, 80, 20, 80], fill=folder_color, outline=(255, 152, 0), width=2)
    
    # 添加文件图标（表示文件整理）
    file_colors = [(33, 150, 243), (76, 175, 80), (244, 67, 54), (156, 39, 176)]
    file_positions = [(50, 100), (90, 100), (130, 100), (170, 100)]
    
    for i, (color, pos) in enumerate(zip(file_colors, file_positions)):
        # 绘制小文件
        draw.rectangle([pos[0], pos[1], pos[0]+25, pos[1]+35], fill=color, outline=(255, 255, 255), width=1)
        # 文件标签
        draw.rectangle([pos[0], pos[1], pos[0]+15, pos[1]+8], fill=(255, 255, 255, 180))
    
    # 添加箭头表示整理动作
    arrow_color = (255, 255, 255)
    # 箭头主体
    draw.polygon([200, 140, 220, 140, 210, 160, 220, 160, 200, 180, 200, 160], fill=arrow_color)
    
    # 保存图标
    icon_path = "folder_organizer.ico"
    img.save(icon_path, format='ICO', sizes=[(256, 256)])
    
    print(f"图标已创建：{icon_path}")
    return icon_path

def create_exe_spec():
    """创建PyInstaller spec文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['file_organizer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FileOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='folder_organizer.ico',
    version='version_info.txt'
)
"""
    
    with open("FileOrganizer.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("Spec文件已创建：FileOrganizer.spec")

def create_version_info():
    """创建版本信息文件"""
    version_content = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AiPy File Organizer'),
         StringStruct(u'FileDescription', u'文件自动整理工具'),
         StringStruct(u'FileVersion', u'1.0.0.0'),
         StringStruct(u'InternalName', u'FileOrganizer'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2024 AiPy'),
         StringStruct(u'OriginalFilename', u'FileOrganizer.exe'),
         StringStruct(u'ProductName', u'File Organizer'),
         StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_content)
    
    print("版本信息文件已创建：version_info.txt")

if __name__ == "__main__":
    print("开始创建打包文件...")
    
    # 创建图标
    icon_path = create_folder_icon()
    
    # 创建版本信息
    create_version_info()
    
    # 创建spec文件
    create_exe_spec()
    
    print("\n✨ 所有打包文件已准备完成！")
    print("请运行以下命令打包exe：")
    print("pyinstaller FileOrganizer.spec")
    print("\n打包后的exe文件将在 dist 文件夹中")