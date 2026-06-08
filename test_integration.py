import unittest
import os
from huffman_codec import HuffmanCodec
from io_handler import IOHandler


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_file = "temp_test.bin"
        self.data = "hello world, this is a lossless compression test."

    def tearDown(self):
        """测试结束后清理临时文件"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_full_pipeline(self):
        """测试：数据 -> 编码 -> 存盘 -> 读盘 -> 解码 -> 校验"""
        # 1. 编码
        coder = HuffmanCodec(self.data)
        coder.build()
        encoded_str = coder.encode()

        # 2. 存入二进制文件
        IOHandler.write_compressed_file(self.test_file, encoded_str)

        # 3. 从二进制文件读取
        recovered_binary = IOHandler.read_compressed_file(self.test_file)

        # 4. 验证二进制位是否一致
        self.assertEqual(encoded_str, recovered_binary)

        # 5. 解码并校验原文
        decoded_data = coder.decode(recovered_binary)
        self.assertEqual(self.data, decoded_data)
        print("集成测试通过：文件读写与解压流程完美联动。")


if __name__ == "__main__":
    unittest.main()