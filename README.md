# CWCX_AutoMod
## 概述
某游戏的Mod自动修复工具。你只需要将游戏原本的CacheFiles和ManifestFiles文件复制过来，挑选你喜欢的Mod放入mod文件夹中，然后执行程序一键修补。
## 使用说明
### 懒人包（推荐）
可以在右侧release中直接下载修补好的CacheFiles文件。
### 使用可执行文件（推荐给想自己挑选Mod的人）
1. 在右侧release中下载最新版压缩包；
2. 解压压缩包，得到一个可执行文件AutoMod.exe和一个空文件夹mod；
3. 将手机/模拟器中 ./android/data/com.tingzhou.cwcxtw.qooapp/files/yoo/ResPackage 路径下的CacheFiles和ManifestFiles文件复制出来，与AutoMod.exe放在同文件夹下；
4. 挑选自己喜欢的Mod，将它们放在mod文件夹中；
5. 执行AutoMod.exe，程序会自动修补Mod。修补结束后，将CacheFiles文件夹复制回手机/模拟器的原路径中，覆盖原文件。
### 使用源代码
1. 安装python，推荐3.8.10，记得把python加入系统路径；
2. 克隆本项目：

   ```powershell
   git clone https://github.com/HHEBL/CWCX_AutoMod.git
   ```
   得到CWCX_AutoMod文件夹。一般不需要安装第三方依赖；
4. 将手机/模拟器中 ./android/data/com.tingzhou.cwcxtw.qooapp/files/yoo/ResPackage 路径下的CacheFiles和ManifestFiles文件复制出来，放在CWCX_AutoMod文件夹中；
5. 挑选自己喜欢的Mod，将它们放在CWCX_AutoMod文件夹下的mod文件夹中；
6. 在终端中执行命令：

   ```powershell
   python main.py
   ```
   程序会自动修补Mod。修补结束后，将CacheFiles文件夹复制回手机/模拟器的原路径中，覆盖原文件。
## 有问题的Mod
以下Mod存在一些问题：
| 编号 | 存在问题 | 是否放入懒人包 |
|:--------:|:--------:|:--------:|
|11030001|无背景|是|
|10010001|有紫色块|是|
|11040001|有紫色块|是|
|12017|黑屏|否|
|11021|黑屏|否|
|13005001|黑屏|否|
|13020001|黑屏|否|
|13010001|黑屏|否|
|13004001|黑屏卡死|否|
|13003001|黑屏卡死|否|
## TODO
由于修补后未将打mod和未打mod的文件区分开，打包的懒人包体积过大。以后可能会将打了mod的文件单独区分出来，减少包体积。
