import os
import json

class IOHandler:
    @staticmethod
    def write_compressed_file(file_path: str, binary_str: str):
        """将 01 字符串写入二进制文件"""
        # 1. 计算填充位，保证能被 8 整除
        padding = 8 - (len(binary_str) % 8)
        binary_str += "0" * padding

        # 2. 将字符串转为字节流
        byte_array = bytearray()
        for i in range(0, len(binary_str), 8):
            byte = int(binary_str[i:i + 8], 2)
            byte_array.append(byte)

        # 3. 存储填充信息（放在文件头，方便解压）
        with open(file_path, "wb") as f:
            f.write(bytes([padding]))
            f.write(byte_array)

    @staticmethod
    def read_compressed_file(file_path: str) -> str:
        """从二进制文件读取并还原为 01 字符串"""
        with open(file_path, "rb") as f:
            padding = f.read(1)[0]
            data = f.read()

        binary_str = "".join(f"{byte:08b}" for byte in data)
        # 去除填充位
        if padding > 0:
            binary_str = binary_str[:-padding]
        return binary_str

    @staticmethod
    def save_bundle(file_path: str, code_map: dict, binary_str: str):
        """将映射表和二进制数据打包存储"""
        # 1. 序列化编码表
        meta_data = json.dumps(code_map).encode('utf-8')
        # 2. 获取二进制内容
        padding = 8 - (len(binary_str) % 8)
        binary_str += "0" * padding
        data = bytes([int(binary_str[i:i + 8], 2) for i in range(0, len(binary_str), 8)])

        with open(file_path, "wb") as f:
            # 先存元数据长度，再存元数据，最后存数据
            f.write(len(meta_data).to_bytes(4, byteorder='big'))
            f.write(meta_data)
            f.write(bytes([padding]))
            f.write(data)

    @staticmethod
    def load_bundle(file_path: str):
        """从二进制文件中还原 code_map 和 binary_str"""
        with open(file_path, "rb") as f:
            # 1. 读取元数据长度 (4 字节)
            meta_len = int.from_bytes(f.read(4), byteorder='big')
            # 2. 读取元数据 (json 格式的 code_map)
            meta_data = json.loads(f.read(meta_len).decode('utf-8'))
            # 3. 读取填充位数
            padding = f.read(1)[0]
            # 4. 读取二进制数据
            data = f.read()

        # 还原二进制字符串
        binary_str = "".join(f"{byte:08b}" for byte in data)
        if padding > 0:
            binary_str = binary_str[:-padding]

        return meta_data, binary_str