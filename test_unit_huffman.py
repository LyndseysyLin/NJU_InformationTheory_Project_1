import unittest
from huffman_codec import HuffmanCodec


class TestHuffmanCodec(unittest.TestCase):

    def setUp(self):
        """每个测试方法运行前都会执行此初始化"""
        self.sample_text = "huffman_coding_is_efficient"
        self.coder = HuffmanCodec(self.sample_text)
        self.coder.build()

    def test_build_tree_validity(self):
        """验证树是否成功构建且包含所有字符"""
        self.assertIsNotNone(self.coder.root)
        # 确保编码表不为空
        self.assertTrue(len(self.coder.code_map) > 0)
        # 验证所有字符都有编码
        for char in set(self.sample_text):
            self.assertIn(char, self.coder.code_map)

    def test_encode_decode_integrity(self):
        """核心无损性测试：编码后再解码必须等于原文"""
        encoded = self.coder.encode()
        decoded = self.coder.decode(encoded)
        self.assertEqual(self.sample_text, decoded, "解码还原后的数据与原文不一致！")

    def test_prefix_property(self):
        """验证霍夫曼编码的前缀性质"""
        codes = list(self.coder.code_map.values())
        for i in range(len(codes)):
            for j in range(len(codes)):
                if i != j:
                    self.assertFalse(codes[i].startswith(codes[j]),
                                     f"编码违反前缀性质: {codes[i]} 包含 {codes[j]}")

    def test_single_char_data(self):
        """边界测试：测试仅由单个字符重复组成的字符串"""
        data = "aaaaa"
        single_coder = HuffmanCodec(data)
        single_coder.build()
        # 对于单字符，编码应为 '0'
        encoded = single_coder.encode()
        self.assertEqual(encoded, "0" * len(data))
        self.assertEqual(single_coder.decode(encoded), data)


if __name__ == "__main__":
    unittest.main()