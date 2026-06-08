import os
import json
from huffman_codec import HuffmanCodec
from io_handler import IOHandler
from analysis import Analysis


def main():
    source_file = "source.txt"
    compressed_file = "compressed.bin"

    # 1. 读取原始数据
    if not os.path.exists(source_file):
        print(f"错误: 找不到 {source_file}，请确保它存在。")
        return

    with open(source_file, "r", encoding="utf-8") as f:
        data = f.read()

    print(f"正在压缩: {source_file} ({len(data)} 字符)...")

    # 2. 压缩流程
    coder = HuffmanCodec(data)
    coder.build()
    encoded_binary = coder.encode()
    IOHandler.save_bundle(compressed_file, coder.code_map, encoded_binary)

    # 3. 性能分析报告
    original_size = os.path.getsize(source_file)
    compressed_size = os.path.getsize(compressed_file)
    Analysis.report(data, coder.code_map, original_size, compressed_size)

    # 4. 无损验证流程
    print("\n开始进行无损校验...")
    loaded_map, loaded_binary = IOHandler.load_bundle(compressed_file)

    # 将加载的 map 重新注入给 codec 以进行解码
    coder.code_map = loaded_map
    # 恢复逆向查找表用于解码
    coder.reverse_code_map = {v: k for k, v in loaded_map.items()}

    decoded_data = coder.decode(loaded_binary)

    if decoded_data == data:
        print("校验结果: [成功] 解压数据与原文完全匹配！")
    else:
        print("校验结果: [失败] 数据不一致，请检查算法。")


if __name__ == "__main__":
    main()