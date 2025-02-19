import os
import re
import json
import shutil
import struct
import binascii


# 映射关系存储文件路径
MAPPING_FILE = './mappings.json'


def load_mappings():
    """
    加载已存储的 cid 和 target_folder 的映射关系。
    """
    if not os.path.exists(MAPPING_FILE):
        return {}
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mappings(mapping):
    """
    将 cid 和 target_folder 的映射关系保存到文件。
    """
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)


def get_latest_file(folder, suffix, time_length=14):
    """
    获取指定文件夹下所有指定后缀的文件中，具有最新时间戳的文件内容。
    时间格式为yyyymmddhhmmss，位于文件名的最后14位。
    """
    latest_time = 0
    latest_file = ""

    for filename in os.listdir(folder):
        if filename.endswith(suffix):
            # 提取文件名中的时间部分
            file_time_str = filename[:-len(suffix)][-time_length:]
            try:
                file_time = int(file_time_str)
                if file_time > latest_time:
                    latest_file = filename
                    latest_time = file_time
            except ValueError:
                print(f"文件名{filename}中的时间部分不是有效的整数。")

    if not latest_file:
        print("未找到符合条件的文件。")
        return None

    try:
        print(f'最新的ManifestFiles文件为：{latest_file}，正在读取...\n')
        with open(os.path.join(folder, latest_file), 'r', encoding='ANSI', errors='replace') as f:
            latest_file_content = f.read()
    except IOError as e:
        print(f"文件{latest_file}读取失败: {e}")
        return None

    return latest_file_content


def extract_info(content, cid, max_retry=10):
    """
    在给定的内容中查找cid，并根据正则匹配提取32位文件夹名。
    """
    pattern = re.compile(r'^[a-z0-9]{32}$')

    # 查找cid对应的bundle位置
    index = content.find(f"{cid}.bundle")
    if index == -1:
        print(f"未找到编号{cid}的角色对应文件。")
        return None

    start_index = index + len(cid) + 10  # 跳过大约10个无效字符
    end_index = start_index + 32

    for i in range(max_retry):
        if start_index > len(content) - 32:
            print(f"无法在剩余内容中找到符合要求的字符串。")
            return None

        substring = content[start_index:start_index + 32]
        if pattern.match(substring):
            return substring

        start_index += 1
        end_index += 1

    print(f"未能在最大重试次数内找到符合要求的字符串。")
    return None


def copy_and_rename_file(src_path, target_folder, dest_filename="__data"):
    """
    将源文件复制到目标文件夹，并重命名。
    如果目标文件夹中已存在同名文件，则覆盖它。
    """
    # 创建目标文件夹（如果不存在）
    os.makedirs(target_folder, exist_ok=True)

    # 目标文件路径
    dest_path = os.path.join(target_folder, dest_filename)

    try:
        # 复制并重命名文件
        shutil.copy2(src_path, dest_path)
        print(f"{src_path}文件已成功覆盖到{dest_path}")
        return dest_path
    except Exception as e:
        print(f"文件复制或重命名失败: {e}")
        return None


def convert_size_to_hex(size):
    """
    将文件大小转换为小端序的十六进制字符串，并确保长度为8个字符（补0）。
    """
    # 将文件大小转换为小端序的二进制数据
    packed_data = struct.pack('<I', size)

    # 转换为十六进制字符串，并确保长度为8个字符（补0）
    hex_string = packed_data.hex().zfill(8)

    return hex_string


def update_info_file(info_path, new_address):
    """
    更新 __info 文件，从第21位开始替换为新的地址字符串，并将剩余部分设置为0。
    """
    try:
        with open(info_path, 'rb') as f:
            binary_data = f.read()

        print("修改校验文件：")

        hex_data = binascii.hexlify(binary_data).decode('utf-8')
        print(f"原始十六进制校验数据: {hex_data}")

        # 确保文件长度足够进行修改
        if len(hex_data) < 20 + len(new_address):
            raise ValueError("文件长度不足以进行修改")

        # 替换第21位开始的内容
        prefix = hex_data[:20]
        suffix_length = (len(hex_data) - 20 - len(new_address)) // 2
        suffix = '00' * suffix_length

        # 构建新的十六进制字符串
        new_hex_data = prefix + new_address + suffix

        print(f"新的十六进制校验数据: {new_hex_data}")

        # 将新的十六进制字符串转换回二进制数据
        new_binary_data = binascii.unhexlify(new_hex_data)

        # 写回文件
        with open(info_path, 'wb') as f:
            f.write(new_binary_data)

        print(f"校验文件{info_path}已更新。")

        return
    except Exception as e:
        print(f"文件{info_path}更新失败: {e}")


def main():
    mod_folder = './mod'
    manifest_folder = './ManifestFiles'
    cache_folder = './CacheFiles'
    suf_pkg = '.pkg'
    suf_bytes = '.bytes'

    # 加载已存储的 cid-target folder 映射关系
    mappings = load_mappings()

    # 记录新的 cid-target folder 映射关系
    new_mappings = {}
    
    # 记录已访问过文件夹
    folder_records = {}

    # 获取最新的ManifestFiles文件内容
    content = get_latest_file(manifest_folder, suf_bytes)
    if not content:
        print("无法获取最新的ManifestFiles文件内容。")
        return

    # 遍历./mod路径下所有pkg文件
    for filename in os.listdir(mod_folder):
        if filename.endswith(suf_pkg):
            # 去除文件后缀名.pkg
            cid = filename[:-len(suf_pkg)]
            
            # 先查找已存储的映射关系
            target_folder = mappings.get(cid)
            if not target_folder:
                # 根据角色ID在ManifestFiles文件中查找对应的文件夹名
                target_folder = extract_info(content, cid)
                if target_folder:
                    new_mappings[cid] = target_folder
                else:
                    print(f"未找到编号{cid}的相关信息或文件内容不符合预期。")
                    continue
            
            print(f"编号{cid}的角色对应文件夹为：{target_folder}")

            # 构建目标文件夹路径
            target_path = os.path.join(cache_folder, target_folder[:2], target_folder)

            # 源文件路径
            src_path = os.path.join(mod_folder, filename)

            # 移动并重命名文件
            copied_file_path = copy_and_rename_file(src_path, target_path)
            if copied_file_path:
                # 获取文件大小并转换为十六进制字符串
                file_size = os.path.getsize(copied_file_path)
                hex_address = convert_size_to_hex(file_size)
                print(f"文件大小为{file_size}字节，转化为小端序十六进制是：{hex_address}")

                # 构建 __info 文件路径
                info_path = os.path.join(target_path, "__info")

                # 更新 __info 文件
                update_info_file(info_path, hex_address)

            # 记录 target_folder 及其前两个字符
            prefix2 = target_folder[:2]
            if prefix2 not in folder_records:
                folder_records[prefix2] = []
            folder_records[prefix2].append(target_folder)
            
            print("")  # 每次处理的输出之间空一行，为了美观
    
    print("Mod修补完毕，正在清理非Mod文件...")
    # 遍历 cache_folder 并删除未被记录的文件夹
    for root, dirs, files in os.walk(cache_folder):
        if len(root.split(os.sep)) - len(cache_folder.split(os.sep)) == 1:
            # 当前目录是第一层子目录
            current_dir = os.path.basename(root)
            if current_dir in folder_records:
                # 获取当前目录下的所有 target_folder
                existing_folders = set(os.listdir(root))
                recorded_folders = set(folder_records[current_dir])
                folders_to_delete = existing_folders - recorded_folders
                
                for folder in folders_to_delete:
                    folder_path = os.path.join(root, folder)
                    shutil.rmtree(folder_path)
            else:
                # 如果当前目录没有记录的目标文件夹，删除整个目录
                shutil.rmtree(root)
    
    # 在所有任务完成后，将新的映射关系一次性写入到文件
    if new_mappings:
        mappings.update(new_mappings)
        save_mappings(mappings)
        print("新的映射关系已保存到文件。")
    
    # 提示用户按下回车键退出
    input("按下回车键退出...")


if __name__ == "__main__":
    main()
