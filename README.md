<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-6.5+-green?logo=qt" alt="PySide6">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey" alt="Platform">
</p>

<h1 align="center">PDF Merge & Delete</h1>

<p align="center">
  <b>A simple and easy-to-use PDF processing tool</b><br>
  <sub>Click <a href="#-中文">中文</a> for Chinese version</sub>
</p>

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [File Structure](#-file-structure)
- [Requirements](#-requirements)
- [FAQ](#-faq)
- [Changelog](#-changelog)
- [License](#-license)

---

## ✨ Features

### 📎 Merge PDF
- Merge multiple PDF files into one
- Support drag to adjust file order
- Set page ranges for each file
- Bookmark handling options

### 🗑️ Delete Pages
- Delete specified pages from a single PDF
- Support single page: `1, 3, 5`
- Support page range: `5-8`
- Support mixed format: `1, 3, 5-8, 10-15, 20`

### 📁 Batch Delete
- Batch delete pages from all PDFs in a directory
- Automatic output naming: `original_name_del.pdf`
- Progress display for each file
- Error handling and reporting

---

## 📸 Screenshots

<div align="center">
  <a href="https://imgchr.com/i/pmgvvK1"><img src="https://s41.ax1x.com/2026/07/24/pmgvvK1.png" alt="Home Page" border="0" /></a>
  <a href="https://imgchr.com/i/pmgvxDx"><img src="https://s41.ax1x.com/2026/07/24/pmgvxDx.png" alt="Merge Page" border="0" /></a>
  <a href="https://imgchr.com/i/pmgvXvR"><img src="https://s41.ax1x.com/2026/07/24/pmgvXvR.png" alt="Delete Page" border="0" /></a>
</div>

---

## 🚀 Installation

### Option 1: Download Executable (Recommended)

Download `PDF合并删除.exe` from the release page and run it directly. No Python installation required.

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-processor.git
cd pdf-processor

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 3: Build Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "PDF_Merge_Delete" main.py
```

---

## 📖 Usage

### Merge PDF Files

1. Click **"Merge"** on the home page
2. Click **"Add Files"** to select PDF files
3. Use **"Up"/"Down"** buttons to adjust file order
4. Set page range (optional)
5. Select output file path
6. Click **"Start Merge"**

### Delete Pages (Single File)

1. Click **"Delete"** on the home page
2. Click **"Browse"** to select a PDF file
3. Enter pages to delete:
   - Single pages: `1, 3, 5`
   - Page range: `5-8`
   - Mixed: `1, 3, 5-8, 10-15`
4. Select output file path
5. Click **"Start Delete"**

### Batch Delete Pages

1. Click **"Batch Delete"** on the home page
2. Click **"Browse Directory"** to select a folder containing PDFs
3. Enter pages to delete (same format as above)
4. Select output directory (optional, defaults to source directory)
5. Click **"Start Batch Delete"**

**Output Naming Rule**: Files are saved as `original_name_del.pdf`

| Input File | Output File |
|------------|-------------|
| `001. Journey to the West.pdf` | `001. Journey to the West_del.pdf` |
| `report_2024.pdf` | `report_2024_del.pdf` |

---

## 📁 File Structure

```
pdf_processor/
├── main.py                  # Main application entry point
├── home_page.py             # Home page with navigation buttons
├── merge_page.py            # Merge PDF functionality
├── delete_page.py           # Delete pages functionality
├── batch_delete_page.py     # Batch delete functionality
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 📋 Requirements

| Package | Version | Description |
|---------|---------|-------------|
| Python | >= 3.8 | Programming language |
| PySide6 | >= 6.5.0 | GUI framework |
| PyPDF2 | >= 3.0.0 | PDF processing library |
| pycryptodome | >= 3.15.0 | Encryption support for AES |

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## ❓ FAQ

<details>
<summary><b>Q: Why do I get "PyCryptodome is required for AES algorithm" error?</b></summary>

Some PDF files use AES encryption. Install pycryptodome to fix this:
```bash
pip install pycryptodome
```
</details>

<details>
<summary><b>Q: Why is the last PDF file missing from the list?</b></summary>

This was a bug in earlier versions. Update to the latest version where the file list now properly displays all PDF files.
</details>

<details>
<summary><b>Q: Can I undo a delete operation?</b></summary>

No, delete operations are irreversible. Always backup your files before processing.
</details>

<details>
<summary><b>Q: What page numbering is used?</b></summary>

Pages are numbered starting from 1 (not 0).
</details>

---

## 📝 Changelog

### v1.1.0 (2026-07-08)
- ✨ Added batch delete feature
- ✨ Home page now has 3 quick navigation buttons
- 🐛 Fixed page layout issues with scroll area
- 🐛 Fixed file list not showing all PDFs
- 🔒 Added pycryptodome for AES encryption support

### v1.0.0 (2026-07-06)
- 🎉 Initial release
- ✅ Merge multiple PDF files
- ✅ Delete pages from single PDF
- ✅ Modern GUI with PySide6

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [PySide6](https://wiki.qt.io/Qt_for_Python) - GUI Framework
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF Processing
- [PyCryptodome](https://pycryptodome.readthedocs.io/) - Encryption Support

---

<div align="center">
  <sub>Made with ❤️ by PDF Processor Team</sub>
</div>

---

# 🇨🇳 中文

<p align="center">
  <b>简单易用的PDF处理工具</b><br>
  <sub>点击 <a href="#-table-of-contents">English</a> 返回英文版本</sub>
</p>

---

## 📖 目录

- [功能特性](#-功能特性)
- [安装说明](#-安装说明)
- [使用说明](#-使用说明)
- [文件结构](#-文件结构)
- [依赖要求](#-依赖要求)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 📎 合并PDF
- 将多个PDF文件合并为一个
- 支持调整文件顺序
- 设置每个文件的页码范围
- 书签处理选项

### 🗑️ 删除页面
- 从单个PDF中删除指定页面
- 支持单页：`1, 3, 5`
- 支持连续页：`5-8`
- 支持混合格式：`1, 3, 5-8, 10-15, 20`

### 📁 批量删除
- 批量删除目录中所有PDF的指定页面
- 自动命名输出文件：`原文件名_del.pdf`
- 显示每个文件的处理进度
- 错误处理和报告

---

## 🚀 安装说明

### 方式一：下载可执行文件（推荐）

从发布页面下载 `PDF合并删除.exe`，直接运行即可，无需安装Python环境。

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/yourusername/pdf-processor.git
cd pdf-processor

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

### 方式三：打包成可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed --name "PDF合并删除" main.py
```

---

## 📖 使用说明

### 合并PDF文件

1. 在首页点击 **"合并"**
2. 点击 **"添加文件"** 选择PDF文件
3. 使用 **"上移"/"下移"** 按钮调整文件顺序
4. 设置页码范围（可选）
5. 选择输出文件路径
6. 点击 **"开始合并"**

### 删除页面（单个文件）

1. 在首页点击 **"删除"**
2. 点击 **"浏览"** 选择PDF文件
3. 输入要删除的页码：
   - 单页：`1, 3, 5`
   - 连续页：`5-8`
   - 混合格式：`1, 3, 5-8, 10-15`
4. 选择输出文件路径
5. 点击 **"开始删除"**

### 批量删除页面

1. 在首页点击 **"批量删除"**
2. 点击 **"浏览目录"** 选择包含PDF的文件夹
3. 输入要删除的页码（格式同上）
4. 选择输出目录（可选，默认为源文件目录）
5. 点击 **"开始批量删除"**

**输出命名规则**：文件保存为 `原文件名_del.pdf`

| 输入文件 | 输出文件 |
|----------|----------|
| `001. 西游记.pdf` | `001. 西游记_del.pdf` |
| `报告_2024.pdf` | `报告_2024_del.pdf` |

---

## 📁 文件结构

```
pdf_processor/
├── main.py                  # 主程序入口
├── home_page.py             # 首页（含导航按钮）
├── merge_page.py            # 合并功能页面
├── delete_page.py           # 删除功能页面
├── batch_delete_page.py     # 批量删除功能页面
├── requirements.txt         # Python依赖文件
└── README.md                # 本文件
```

---

## 📋 依赖要求

| 包名 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.8 | 编程语言 |
| PySide6 | >= 6.5.0 | GUI框架 |
| PyPDF2 | >= 3.0.0 | PDF处理库 |
| pycryptodome | >= 3.15.0 | AES加密支持 |

安装所有依赖：
```bash
pip install -r requirements.txt
```

---

## ❓ 常见问题

<details>
<summary><b>问：为什么提示 "PyCryptodome is required for AES algorithm" 错误？</b></summary>

某些PDF文件使用了AES加密，需要安装pycryptodome：
```bash
pip install pycryptodome
```
</details>

<details>
<summary><b>问：为什么文件列表缺少最后一个PDF文件？</b></summary>

这是早期版本的bug，更新到最新版本即可解决。
</details>

<details>
<summary><b>问：删除操作可以撤销吗？</b></summary>

不可以，删除操作不可逆。处理前请务必备份文件。
</details>

<details>
<summary><b>问：页码是从0还是1开始计数？</b></summary>

页码从1开始计数。
</details>

---

## 📝 更新日志

### v1.1.0 (2026-07-08)
- ✨ 新增批量删除功能
- ✨ 首页增加3个快捷导航按钮
- 🐛 修复页面布局错位问题（添加滚动区域）
- 🐛 修复文件列表不完整问题
- 🔒 添加pycryptodome支持AES加密

### v1.0.0 (2026-07-06)
- 🎉 首次发布
- ✅ 合并多个PDF文件
- ✅ 删除单个PDF的指定页面
- ✅ 基于PySide6的现代化界面

---

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [PySide6](https://wiki.qt.io/Qt_for_Python) - GUI框架
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF处理库
- [PyCryptodome](https://pycryptodome.readthedocs.io/) - 加密支持

---

<div align="center">
  <sub>由 PDF Processor Team 用 ❤️ 制作</sub>
</div>
