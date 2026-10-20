#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建 LibreOffice 26.x 主题扩展：Violet Dusk

界面外壳（菜单栏 / 工具栏 / 窗口）：深紫 #343061 + 纯白文字
文档画布（Calc 单元格 / Writer 纸张）  ：浅紫 #F4F1FD + 深墨文字，与单元格定位色同色系

配置项路径：org.openoffice.Office.UI / ColorScheme / ColorSchemes / <主题名> / <颜色项> / Color
文件结构参照 26.2 官方主题扩展（Theme.xcu + description.xml + META-INF/manifest.xml）
"""
import os, shutil, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
THEME_NAME = "Violet Dusk"
THEME_VERSION = "1.1.0"
EXT_ID = "org.duskviolet.libreoffice.theme"
DIST = os.path.join(HERE, "dist")
OUT = os.path.join(DIST, "Violet-Dusk-%s.oxt" % THEME_VERSION)
PALETTE_OUT = os.path.join(DIST, "Violet-Dusk-palette.soc")
GUIDE_OUT = os.path.join(DIST, "导入说明.txt")

# ---------- 界面外壳：深色 ----------
UI = dict(
    main=0x343061,      # 应用 / 窗口 / 工具栏 / 菜单栏底色
    popup=0x2C2953,     # 弹出菜单 / 非活动窗口
    hover=0x423D7A,     # 悬停、按下、按钮面
    sel=0x4A4494,       # 选中高亮块
    border=0x4A4685,    # 分隔线 / 边框
    shadow=0x1E1C38,
    fg=0xFFFFFF,        # 界面文字：纯白
    fg_soft=0xB8B4E0,   # 非活动窗口文字
    fg_dim=0x8B87B8,    # 禁用文字
    accent=0x9B8CFF,    # 强调色
    field=0x2B2852,     # 对话框输入框（深色，配白字）
)

# ---------- 文档画布：浅色，与 #C0B0FF 定位色同属紫罗兰色系 ----------
DOC = dict(
    bg=0xF4F1FD,        # 单元格 / 纸张底色（定位色的极浅调）
    bg_soft=0xE9E3FA,   # 批注、受保护区域
    border=0xD9D1F2,    # 网格线 / 分页线 / 边界
    text=0x241F3D,      # 正文：深墨紫
    text_dim=0x6E68A0,  # 次要文字 / 非打印字符
    blue=0x1F5AA8,      # 数值、链接
    green=0x1F7A4C,     # 公式
    magenta=0xA8387F,   # 引用、关键字
    violet=0x6C4FC9,    # 数字、已访问链接
    red=0xB3362F,       # 拼写错误
    orange=0x9A5A00,    # 语法提示
    olive=0x6B5A00,     # 字符串
    focus=0x8B79E8,     # 单元格定位框（在浅底上要加深才看得见）
)

# ---------- Basic IDE：保持深色编辑器 ----------
IDE = dict(
    bg=0x2B2852,
    keyword=0xFF9BD2,
    ident=0x8FD8FF,
    number=0xC0B0FF,
    string=0xF6F08C,
    comment=0x8B87B8,
    op=0x7CE38B,
    err=0xFF6E6E,
)

# ---------- 93 个颜色项（与 26.8 main.xcd 的 UI/ColorScheme 完全对齐）----------
# (名称, 色值, IsVisible)
ENTRIES = [
    # ---- 文档通用 ----
    ("DocColor",                    DOC["bg"],        None),
    ("DocBoundaries",               DOC["border"],    None),
    ("AppBackground",               UI["main"],       None),
    ("TableBoundaries",             DOC["border"],    None),
    ("FontColor",                   DOC["text"],      None),
    ("Links",                       DOC["blue"],      True),
    ("LinksVisited",                DOC["violet"],    True),
    ("Spell",                       DOC["red"],       None),
    ("Grammar",                     DOC["orange"],    None),
    ("SmartTags",                   DOC["magenta"],   None),
    ("Shadow",                      DOC["border"],    True),
    # ---- Writer ----
    ("WriterTextGrid",              DOC["border"],    None),
    ("WriterBaselineGrid",          DOC["border"],    None),
    ("WriterFieldShadings",         DOC["border"],    True),
    ("WriterIdxShadings",           DOC["border"],    True),
    ("WriterDirectCursor",          DOC["text"],      True),
    ("WriterSectionBoundaries",     DOC["border"],    None),
    ("WriterHeaderFooterMark",      DOC["blue"],      None),
    ("WriterPageBreaks",            DOC["text_dim"],  None),
    ("WriterNonPrintChars",         DOC["text_dim"],  None),
    # ---- HTML ----
    ("HTMLSGML",                    DOC["blue"],      None),
    ("HTMLComment",                 DOC["text_dim"],  None),
    ("HTMLKeyword",                 DOC["magenta"],   None),
    ("HTMLUnknown",                 DOC["text"],      None),
    # ---- Calc ----
    ("CalcGrid",                    DOC["border"],    None),
    ("CalcCellFocus",               DOC["focus"],     None),
    ("CalcDBFocus",                 DOC["focus"],     None),
    ("CalcPageBreak",               DOC["text_dim"],  None),
    ("CalcPageBreakManual",         DOC["text_dim"],  None),
    ("CalcPageBreakAutomatic",      DOC["border"],    None),
    ("CalcHiddenColRow",            DOC["bg_soft"],   False),
    ("CalcTextOverflow",            DOC["text"],      True),
    ("CalcComments",                DOC["text_dim"],  None),
    ("CalcDetective",               DOC["blue"],      None),
    ("CalcDetectiveError",          DOC["red"],       None),
    ("CalcReference",               DOC["magenta"],   None),
    ("CalcNotesBackground",         DOC["bg_soft"],   None),
    ("CalcValue",                   DOC["blue"],      None),
    ("CalcFormula",                 DOC["green"],     None),
    ("CalcText",                    DOC["text"],      None),
    ("CalcProtectedBackground",     DOC["bg_soft"],   None),
    # ---- Draw ----
    ("DrawGrid",                    DOC["border"],    True),
    # ---- 批注作者 ----
    ("Author1",                     DOC["red"],       None),
    ("Author2",                     DOC["green"],     None),
    ("Author3",                     DOC["olive"],     None),
    ("Author4",                     DOC["violet"],    None),
    ("Author5",                     DOC["magenta"],   None),
    ("Author6",                     DOC["blue"],      None),
    ("Author7",                     DOC["orange"],    None),
    ("Author8",                     DOC["text"],      None),
    ("Author9",                     DOC["text_dim"],  None),
    # ---- Basic IDE（深色编辑器）----
    ("BASICEditor",                 IDE["bg"],        None),
    ("BASICIdentifier",             IDE["ident"],     None),
    ("BASICComment",                IDE["comment"],   None),
    ("BASICNumber",                 IDE["number"],    None),
    ("BASICString",                 IDE["string"],    None),
    ("BASICOperator",               IDE["op"],        None),
    ("BASICKeyword",                IDE["keyword"],   None),
    ("BASICError",                  IDE["err"],       None),
    # ---- SQL（跟随文档浅底）----
    ("SQLIdentifier",               DOC["blue"],      None),
    ("SQLNumber",                   DOC["violet"],    None),
    ("SQLString",                   DOC["olive"],     None),
    ("SQLOperator",                 DOC["green"],     None),
    ("SQLKeyword",                  DOC["magenta"],   None),
    ("SQLParameter",                DOC["orange"],    None),
    ("SQLComment",                  DOC["text_dim"],  None),
    # ---- 界面控件色 ----
    ("WindowColor",                 UI["main"],       None),
    ("WindowTextColor",             UI["fg"],         None),
    ("BaseColor",                   UI["main"],       None),
    ("ButtonColor",                 UI["hover"],      None),
    ("ButtonTextColor",             UI["fg"],         None),
    ("AccentColor",                 UI["accent"],     None),
    ("DisabledColor",               UI["main"],       None),
    ("DisabledTextColor",           UI["fg_dim"],     None),
    ("ShadowColor",                 UI["shadow"],     None),
    ("SeparatorColor",              UI["border"],     None),
    ("FaceColor",                   UI["main"],       None),
    ("ActiveColor",                 UI["hover"],      None),
    ("ActiveTextColor",             UI["fg"],         None),
    ("ActiveBorderColor",           UI["accent"],     None),
    ("FieldColor",                  UI["field"],      None),
    # ---- 菜单栏 / 菜单 ----
    ("MenuBarColor",                UI["main"],       None),
    ("MenuBarTextColor",            UI["fg"],         None),
    ("MenuBarHighlightColor",       UI["sel"],        None),
    ("MenuBarHighlightTextColor",   UI["fg"],         None),
    ("MenuColor",                   UI["popup"],      None),
    ("MenuTextColor",               UI["fg"],         None),
    ("MenuHighlightColor",          UI["sel"],        None),
    ("MenuHighlightTextColor",      UI["fg"],         None),
    ("MenuBorderColor",             UI["border"],     None),
    # ---- 非活动窗口 ----
    ("InactiveColor",               UI["popup"],      None),
    ("InactiveTextColor",           UI["fg_soft"],    None),
    ("InactiveBorderColor",         UI["border"],     None),
]

XML_HEAD = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE oor:component-data SYSTEM "../../../../component-update.dtd">
<oor:component-data xmlns:oor="http://openoffice.org/2001/registry"
  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:install="http://openoffice.org/2004/installation" oor:name="UI"
  oor:package="org.openoffice.Office">
  <node oor:name="ColorScheme">
    <node oor:name="ColorSchemes">
      <node oor:name="%s" oor:op="replace">
""" % THEME_NAME


def build_theme_xcu():
    out = [XML_HEAD]
    for name, color, visible in ENTRIES:
        out.append('        <node oor:name="%s">\n' % name)
        out.append('          <prop oor:name="Color" oor:op="fuse">\n')
        out.append('            <value>%d</value>\n' % color)
        out.append('          </prop>\n')
        if visible is not None:
            out.append('          <prop oor:name="IsVisible" oor:op="fuse">\n')
            out.append('            <value>%s</value>\n' % ("true" if visible else "false"))
            out.append('          </prop>\n')
        out.append('        </node>\n')
    out.append("""      </node>
    </node>
    <prop oor:name="CurrentColorScheme">
      <value>%s</value>
    </prop>
  </node>
</oor:component-data>
""" % THEME_NAME)
    return "".join(out)


DESCRIPTION_XML = """<?xml version='1.0' encoding='UTF-8'?>
<description xmlns="http://openoffice.org/extensions/description/2006"
  xmlns:xlink="http://www.w3.org/1999/xlink">
  <identifier value="%s"/>
  <version value="%s"/>
  <publisher>
    <name xlink:href="https://www.libreoffice.org">Custom theme</name>
  </publisher>
  <display-name>
    <name lang="en">Violet Dusk</name>
    <name lang="zh-CN">Violet Dusk 深紫外观 + 浅紫画布</name>
  </display-name>
</description>
""" % (EXT_ID, THEME_VERSION)

MANIFEST_XML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE manifest:manifest PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
  <manifest:file-entry manifest:full-path="Theme.xcu" manifest:media-type="application/vnd.sun.star.configuration-data"/>
  <manifest:file-entry manifest:full-path="pkg-description/pkg-description.en" manifest:media-type="application/vnd.sun.star.package-bundle-description;locale=en"/>
</manifest:manifest>
"""

PKG_DESC = ("Violet Dusk - dark chrome (#343061) with a light violet document canvas "
            "(#F4F1FD) and dark ink text, matching the cell locator color.\n")

README = """Violet Dusk %s  |  LibreOffice 25.2+
==========================================

界面外壳：深紫 #343061 + 纯白文字
文档画布：浅紫 #F4F1FD + 深墨文字（与单元格定位色同色系）

关键配置项（org.openoffice.Office.UI / ColorScheme / ColorSchemes / Violet Dusk）
---------------------------------------------------------------------------
  AppBackground            主界面背景                    #343061
  WindowColor / FaceColor  窗口 / 工具栏底色             #343061
  MenuBarColor / MenuColor 菜单栏 / 下拉菜单底色         #343061 / #2C2953
  MenuBarTextColor         菜单栏文字                    #FFFFFF
  MenuTextColor            下拉菜单文字                  #FFFFFF
  WindowTextColor          窗口 / 工具栏文字             #FFFFFF
  --- 文档与单元格 ---
  DocColor                 单元格 / 纸张底色             #F4F1FD
  CalcGrid                 网格线                        #D9D1F2
  CalcText / FontColor     单元格文字 / 正文             #241F3D
  CalcValue                数值                          #1F5AA8
  CalcFormula              公式                          #1F7A4C
  CalcReference            引用                          #A8387F
  CalcCellFocus            单元格定位框                  #8B79E8
  CalcNotesBackground      批注底色                      #E9E3FA
  --- 强调色 ---
  AccentColor              界面强调色                    #9B8CFF

导入（方式一：图形界面）
----------------------
  1) 完全退出 LibreOffice（含托盘里的快速启动器）
  2) 双击本 .oxt 文件，用 LibreOffice 打开，确认安装
     —— 或：工具 → 扩展管理器 → 添加 → 选择本文件
  3) 重启 LibreOffice
  4) 工具 → 选项 → LibreOffice → 外观 → 主题下拉选 Violet Dusk
     勾选「启用应用程序主题」
     不要勾「使用白色文档背景」（勾了画布会被强制变成纯白）

导入（方式二：命令行，适合批量部署）
--------------------------------
  "C:\\Program Files\\LibreOffice\\program\\unopkg.exe" add "Violet-Dusk-%s.oxt"
  若 LibreOffice 不在默认路径，把 \\program\\unopkg.exe 换成实际路径

卸载
----
  工具 → 扩展管理器 → 选中 Violet Dusk → 移除
  或："C:\\Program Files\\LibreOffice\\program\\unopkg.exe" remove %s
""" % (THEME_VERSION, THEME_VERSION, EXT_ID)


def build_palette():
    """生成可供 LibreOffice 颜色选择器加载的 .soc 调色板"""
    rows = [
        ("界面底 #343061", UI["main"]),
        ("菜单背景 #2C2953", UI["popup"]),
        ("悬停面 #423D7A", UI["hover"]),
        ("选中块 #4A4494", UI["sel"]),
        ("分隔线 #4A4685", UI["border"]),
        ("深阴影 #1E1C38", UI["shadow"]),
        ("界面白 #FFFFFF", UI["fg"]),
        ("次要文字 #B8B4E0", UI["fg_soft"]),
        ("禁用文字 #8B87B8", UI["fg_dim"]),
        ("强调紫 #9B8CFF", UI["accent"]),
        ("画布底 #F4F1FD", DOC["bg"]),
        ("画布浅层 #E9E3FA", DOC["bg_soft"]),
        ("网格线 #D9D1F2", DOC["border"]),
        ("墨紫正文 #241F3D", DOC["text"]),
        ("次要墨 #6E68A0", DOC["text_dim"]),
        ("数值蓝 #1F5AA8", DOC["blue"]),
        ("公式绿 #1F7A4C", DOC["green"]),
        ("引用品红 #A8387F", DOC["magenta"]),
        ("数字紫 #6C4FC9", DOC["violet"]),
        ("错误红 #B3362F", DOC["red"]),
        ("提示橙 #9A5A00", DOC["orange"]),
        ("字符串橄榄 #6B5A00", DOC["olive"]),
        ("定位紫 #8B79E8", DOC["focus"]),
    ]
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<office:color-table xmlns:office="http://openoffice.org/2000/office" '
            'xmlns:draw="http://openoffice.org/2000/drawing">\n'
            '  <!-- Violet Dusk %s palette -->\n' % THEME_VERSION)
    body = "".join('  <draw:color draw:name="%s" draw:color="#%06X"/>\n' % (n, c) for n, c in rows)
    tail = "</office:color-table>\n"
    with open(PALETTE_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(head + body + tail)
    print("生成:", PALETTE_OUT, "(%d 色)" % len(rows))


GUIDE = """Violet Dusk %s — 导入说明
================================

一、这个包是什么
    Violet-Dusk-%s.oxt   LibreOffice 扩展包，双击即可导入，含完整配色方案
    Violet-Dusk-palette.soc  文档调色板，导入后可在单元格/文字颜色里直接选用
    （.oxt 本身就是 LibreOffice 的标准可导入格式，无需解压）

二、导入主题（推荐）
    1. 完全退出 LibreOffice（含托盘里的快速启动器，任务管理器里不应有 soffice.bin）
    2. 双击 Violet-Dusk-%s.oxt → 由 LibreOffice 打开 → 点「安装」
       或：工具 → 扩展管理器 → 添加 → 选择该文件
    3. 重启 LibreOffice
    4. 工具 → 选项 → LibreOffice → 外观 → 主题下拉选「Violet Dusk」
       勾选「启用应用程序主题」
       不要勾「使用白色文档背景」——勾了画布会被强制为纯白，浅紫失效

    命令行方式（批量部署）：
      "C:\\Program Files\\LibreOffice\\program\\unopkg.exe" add "Violet-Dusk-%s.oxt"
      LO 装在别处时替换路径即可，扩展内部不含任何绝对路径，可跨机器使用。

三、导入调色板（可选）
    工具 → 选项 → LibreOffice → 颜色 → 打开 → 选择 Violet-Dusk-palette.soc
    之后在「单元格背景」「字体颜色」「图表颜色」等所有取色面板里都能看到
    这套 23 色，包括 #F4F1FD 画布底与 #8B79E8 定位紫。

四、验证是否生效
    新建一个 Calc：表格区应为浅紫 #F4F1FD，网格线淡紫，输入数字显示深墨紫；
    点击任一单元格，行列定位十字为 #8B79E8；菜单栏与工具栏仍是 #343061 白字。

五、回退
    工具 → 扩展管理器 → 选中 Violet Dusk → 移除，然后重启。
    删除调色板：工具 → 选项 → LibreOffice → 颜色 → 选中该组 → 删除。

六、兼容性
    需要 LibreOffice 25.2 及以上。25.2 之前没有新的 Appearance 主题框架，
    装上也不会出现在「外观」页的主题下拉里（但不影响已有文档与设置）。
    本包未写版本依赖声明——LibreOffice 对扩展依赖的版本号校验会误拒新版，
    加了反而装不上，所以版本要求以此文字为准。
""" % (THEME_VERSION, THEME_VERSION, THEME_VERSION, THEME_VERSION)


def build():
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(os.path.join(BUILD, "META-INF"))
    os.makedirs(os.path.join(BUILD, "pkg-description"))
    os.makedirs(DIST, exist_ok=True)

    files = {
        "Theme.xcu": build_theme_xcu(),
        "description.xml": DESCRIPTION_XML,
        "META-INF/manifest.xml": MANIFEST_XML,
        "pkg-description/pkg-description.en": PKG_DESC,
        "README.txt": README,
    }
    for rel, content in files.items():
        with open(os.path.join(BUILD, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            z.write(os.path.join(BUILD, rel), rel)

    # 同名副本，方便沿用旧路径
    shutil.copy2(OUT, os.path.join(HERE, "Violet-Dusk-theme.oxt"))

    build_palette()
    with open(GUIDE_OUT, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(GUIDE)

    print("生成:", OUT, "(%d bytes)" % os.path.getsize(OUT))
    print("生成:", GUIDE_OUT)
    print("颜色条目数:", len(ENTRIES))


if __name__ == "__main__":
    build()
