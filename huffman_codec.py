import heapq
from collections import Counter
from typing import Dict, Optional


class Node:
    """霍夫曼树节点类"""

    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None

    def __lt__(self, other: 'Node') -> bool:
        """为 heapq 提供比较逻辑，按频率升序排列"""
        return self.freq < other.freq


class HuffmanCodec:
    """霍夫曼编解码核心类"""

    def __init__(self, data: str):
        self.data = data
        self.root: Optional[Node] = None
        self.code_map: Dict[str, str] = {}
        self.reverse_code_map: Dict[str, str] = {}

    def build(self):
        """构建霍夫曼树并生成编码映射表"""
        if not self.data:
            return

        # 1. 频率统计
        freqs = Counter(self.data)

        # 2. 构建最小堆
        heap = [Node(char, freq) for char, freq in freqs.items()]

        # 如果只有一个字符，手动构建一个根节点指向该字符
        if len(heap) == 1:
            self.root = Node(None, heap[0].freq)
            self.root.left = heap[0]
            self._generate_codes(self.root, "")
            return

        heapq.heapify(heap)

        # 3. 构建霍夫曼树
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left, merged.right = left, right
            heapq.heappush(heap, merged)

        self.root = heap[0]
        self._generate_codes(self.root, "")

    def _generate_codes(self, node: Node, current_code: str):
        """递归遍历树生成哈夫曼编码表"""
        if node.left is None and node.right is None:  # 叶子节点
            self.code_map[node.char] = current_code if current_code else "0"
            self.reverse_code_map[self.code_map[node.char]] = node.char
            return

        if node.left:
            self._generate_codes(node.left, current_code + "0")
        if node.right:
            self._generate_codes(node.right, current_code + "1")

    def encode(self) -> str:
        """将字符串编码为 01 序列"""
        return "".join([self.code_map[char] for char in self.data])

    def decode(self, binary_str: str) -> str:
        """根据 01 序列还原原始数据"""
        if not self.root:
            return ""

        result = []
        curr = self.root
        for bit in binary_str:
            curr = curr.left if bit == '0' else curr.right
            if curr.char is not None:
                result.append(curr.char)
                curr = self.root
        return "".join(result)