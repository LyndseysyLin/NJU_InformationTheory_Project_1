import math
from collections import Counter


class Analysis:
    """性能评估与信息论指标分析类"""

    @staticmethod
    def get_entropy(data: str) -> float:
        """计算信源的一阶香农熵 (单位: bits/symbol)"""
        if not data:
            return 0.0

        freqs = Counter(data)
        total_len = len(data)
        entropy = 0.0

        for count in freqs.values():
            p = count / total_len
            entropy -= p * math.log2(p)

        return entropy

    @staticmethod
    def get_average_code_length(data: str, code_map: dict) -> float:
        """计算霍夫曼编码的平均码长 (单位: bits/symbol)"""
        if not data or not code_map:
            return 0.0

        freqs = Counter(data)
        total_len = len(data)
        avg_length = 0.0

        for char, count in freqs.items():
            prob = count / total_len
            avg_length += prob * len(code_map[char])

        return avg_length

    @staticmethod
    def report(data: str, code_map: dict, original_size: int, compressed_size: int):
        """生成并打印完整的性能分析报告"""
        h = Analysis.get_entropy(data)
        l = Analysis.get_average_code_length(data, code_map)
        efficiency = (h / l) * 100 if l != 0 else 0
        cr = original_size / compressed_size if compressed_size != 0 else 0

        print("\n" + "=" * 30)
        print("   --- 项目性能分析报告 ---")
        print("=" * 30)
        print(f"理论极限 (熵 H):    {h:.4f} bits/symbol")
        print(f"实际平均码长 (L):   {l:.4f} bits/symbol")
        print(f"编码效率 (η):       {efficiency:.2f}%")
        print(f"压缩比 (CR):        {cr:.2f}x")
        print("-" * 30)