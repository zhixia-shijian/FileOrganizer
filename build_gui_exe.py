import os
import sys
import subprocess
from pathlib import Path

def create_icon():
    """创建图标文件"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建256x256的图像
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制文件夹主体（黄色渐变）
        folder_color = (255, 193, 7)  # 黄色
        
        # 文件夹主体
        draw.rectangle([30, 70, 226, 200], fill=folder_color, outline=(255, 152, 0), width=3)
        
        # 文件夹标签
        draw.polygon([30, 70, 100, 70, 120, 90, 30, 90], fill=folder_color, outline=(255, 152, 0), width=3)
        
        # 添加文件图标（表示文件整理）
        file_colors = [(33, 150, 243), (76, 175, 80), (244, 67, 54), (156, 39, 176)]
        file_positions = [(60, 110), (90, 110), (130, 110), (170, 110)]
        
        for i, (color, pos) in enumerate(zip(file_colors, file_positions)):
            # 绘制小文件
            draw.rectangle([pos[0], pos[1], pos[0]+20, pos[1]+25], fill=color, outline=(255, 255, 255), width=1)
            # 文件标签
            draw.rectangle([pos[0], pos[1], pos[0]+12, pos[1]+6], fill=(255, 255, 255, 200))
        
        # 添加箭头表示整理动作
        arrow_color = (255, 255, 255)
        # 箭头主体
        draw.polygon([190, 140, 210, 140, 200, 155, 210, 155, 190, 170, 190, 155], fill=arrow_color)
        
        # 保存图标
        icon_path = "folder_organizer_gui.ico"
        img.save(icon_path, format='ICO', sizes=[(256, 256)])
        
        print(f"✅ 图标已创建：{icon_path}")
        return icon_path
        
    except ImportError:
        print("❌ PIL未安装，使用默认图标")
        return None
    except Exception as e:
        print(f"❌ 创建图标失败：{e}")
        return None

def create_spec():
    """创建PyInstaller spec文件"""
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mian.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
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
    name='FileOrganizerGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='folder_organizer_gui.ico',
    version='version_info.txt'
)
"""
    
    with open("FileOrganizerGUI.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Spec文件已创建：FileOrganizerGUI.spec")

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
        [StringStruct(u'CompanyName', u'File Organizer'),
         StringStruct(u'FileDescription', u'文件整理工具 - GUI版本'),
         StringStruct(u'FileVersion', u'1.0.0.0'),
         StringStruct(u'InternalName', u'FileOrganizerGUI'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
         StringStruct(u'OriginalFilename', u'FileOrganizerGUI.exe'),
         StringStruct(u'ProductName', u'File Organizer GUI'),
         StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_content)
    
    print("✅ 版本信息文件已创建：version_info.txt")

def install_pyinstaller():
    """安装PyInstaller"""
    print("🔧 检查PyInstaller...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("📦 正在安装PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False

def install_pillow():
    """安装Pillow"""
    print("🔧 检查Pillow...")
    
    try:
        from PIL import Image
        print("✅ Pillow已安装")
        return True
    except ImportError:
        print("📦 正在安装Pillow...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
            print("✅ Pillow安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ Pillow安装失败")
            return False

def build_exe():
    """构建exe文件"""
    print("\n🚀 开始构建GUI版本exe文件...")
    
    # 创建图标
    icon_path = create_icon()
    
    # 创建版本信息
    create_version_info()
    
    # 创建spec文件
    create_spec()
    
    # 运行PyInstaller
    print("📦 打包exe文件...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "FileOrganizerGUI.spec", "--clean"])
        print("✅ 构建完成！")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败：{e}")
        return False
    
    print(f"\n📁 exe文件位置：{os.path.abspath('dist/FileOrganizerGUI.exe')}")
    
    # 清理临时文件
    print("🧹 清理临时文件...")
    cleanup_files = ["build", "FileOrganizerGUI.spec", "__pycache__", "*.pyc"]
    for item in cleanup_files:
        if "*" in item:
            import glob
            for file in glob.glob(item):
                try:
                    if os.path.isdir(file):
                        import shutil
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
                except:
                    pass
        else:
            try:
                if os.path.exists(item):
                    if os.path.isdir(item):
                        import shutil
                        shutil.rmtree(item)
                    else:
                        os.remove(file)
            except:
                pass
    
    print("✨ GUI版本打包完成！老板可以直接使用 dist/FileOrganizerGUI.exe 了！")
    return True

def main():
    """主函数"""
    print("🔧 检查依赖...")
    
    # 检查并安装依赖
    if not install_pyinstaller():
        print("❌ 无法安装PyInstaller，请手动安装：pip install pyinstaller")
        return
    
    if not install_pillow():
        print("❌ 无法安装Pillow，请手动安装：pip install pillow")
        return
    
    # 构建exe
    build_exe()

if __name__ == "__main__":
    main()