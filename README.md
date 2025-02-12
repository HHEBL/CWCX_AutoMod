# CWCX_AutoMod
## 概述
某游戏的Mod自动修复工具。你只需要将游戏原本的CacheFiles和ManifestFiles文件复制过来，挑选你喜欢的Mod放入mod文件夹中，然后执行程序一键修补。
## 使用说明
### 懒人包（推荐）
可以在右侧release中直接下载package.zip文件，将解压后得到的CacheFiles文件夹放到手机/模拟器的 ./android/data/com.tingzhou.cwcxtw.qooapp/files/yoo/ResPackage 路径下。
### 使用可执行文件（推荐给想自己挑选Mod的人）
1. 在右侧release中下载最新版压缩包；
2. 解压压缩包，得到一个可执行文件AutoMod.exe和一个空文件夹mod；
3. 将手机/模拟器中 ./android/data/com.tingzhou.cwcxtw.qooapp/files/yoo/ResPackage 路径下的CacheFiles和ManifestFiles文件复制出来，与AutoMod.exe放在同文件夹下；
4. 挑选自己喜欢的Mod，将它们放在mod文件夹中；
5. 执行AutoMod.exe，程序会自动修补Mod，并清理无用文件。修补结束后，将CacheFiles文件夹复制回手机/模拟器的原路径中，覆盖原文件。
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
   程序会自动修补Mod，并清理无用文件。修补结束后，将CacheFiles文件夹复制回手机/模拟器的原路径中，覆盖原文件。
## 有问题的Mod
以下Mod存在一些小问题，它们被放在懒人包里一个单独的文件夹中，可自行决定是否使用这些Mod：
| 编号 | 文件路径 | 存在问题 |
|:--------:|:--------:|:--------:|
|10010001|78\78c76b752e1926a5d52e4292fca703f2|有紫色块|
|11030001|29\2958e19b3d53440377c2ce03e6b5a5eb|无背景|
|11040001|36\366c9cfff3df245753c2279b2327d2df|有紫色块|
|12017001|4d\4de5f0c4a41af75360754709a53ce243|进入切换皮肤页面会黑屏|

以下Mod存在恶性问题，未放入懒人包中：
| 编号 | 文件路径 | 存在问题 |
|:--------:|:--------:|:--------:|
|11021|94\94912a1a46f7992db1e04eb273e0dee3|黑屏|
|12017|6e\6e830d0605931ae5745e6e0e46245c48|黑屏|
|13003001|43\43905d74e4dbee579c7d0a5f0b582f44|黑屏卡死|
|13004001|69\69ab2d94bfd04c351188abe8c86e4394|黑屏卡死|
|13005001|1f\1f5d78bc63e1b01384c0bdb8f77a09ac|黑屏|
|13010001|73\73d31b04d759e4e97974b87247085648|黑屏|
|13020001|67\679a3bf5b0cce3b8d962346c4279f26d|黑屏|
## TODO & 反馈
暂时没有需要改进的地方。有任何问题或建议请提Issues。
