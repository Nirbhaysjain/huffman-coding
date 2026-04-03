import heapq


# Node for Huffman Tree
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # needed for heap comparison
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    # Step 1: build frequency map
    def build_frequency(self, text):
        freq = {}
        for ch in text:
            if ch not in freq:
                freq[ch] = 0
            freq[ch] += 1
        return freq

    # Step 2: build min heap
    def build_heap(self, freq_map):
        heap = []
        for ch in freq_map:
            node = Node(ch, freq_map[ch])
            heapq.heappush(heap, node)
        return heap

    # Step 3: merge nodes to form tree
    def merge_nodes(self, heap):
        # edge case: only one unique character
        if len(heap) == 1:
            return heap[0]

        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            merged = Node(freq=node1.freq + node2.freq)
            merged.left = node1   # left = 0
            merged.right = node2  # right = 1

            heapq.heappush(heap, merged)

        return heap[0]

    # Step 4: generate codes from tree
    def build_codes_helper(self, node, current_code):
        if node is None:
            return

        # leaf node
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
            return

        self.build_codes_helper(node.left, current_code + "0")
        self.build_codes_helper(node.right, current_code + "1")

    def build_codes(self, root):
        self.build_codes_helper(root, "")

    # Step 5: encode text
    def encode(self, text):
        encoded = ""
        for ch in text:
            encoded += self.codes[ch]
        return encoded

    # Step 6: decode text
    def decode(self, encoded_text, root):
        decoded = ""
        current = root

        for bit in encoded_text:
            if bit == '0':
                current = current.left
            else:
                current = current.right

            # reached leaf node
            if current.char is not None:
                decoded += current.char
                current = root

        return decoded


# ------------------ DRIVER CODE ------------------

def run_huffman(text):
    hc = HuffmanCoding()

    # frequency
    freq_map = hc.build_frequency(text)

    # heap
    heap = hc.build_heap(freq_map)

    # tree
    root = hc.merge_nodes(heap)

    # codes
    hc.build_codes(root)

    print("\nCharacter | Frequency | Code")
    print("--------------------------------")
    for ch in freq_map:
        print(f"   {ch}      |     {freq_map[ch]}     | {hc.codes[ch]}")

    # encode
    encoded = hc.encode(text)
    print("\nEncoded Text:")
    print(encoded)

    # decode
    decoded = hc.decode(encoded, root)
    print("\nDecoded Text:")
    print(decoded)

    # stats
    original_bits = len(text) * 8
    compressed_bits = len(encoded)

    print("\nCompression Analysis:")
    print(f"Original size   : {original_bits} bits")
    print(f"Compressed size : {compressed_bits} bits")

    ratio = compressed_bits / original_bits
    print(f"Compression ratio: {round(ratio, 3)}")


if __name__ == "__main__":
    print("Huffman Coding Compression\n")

    text = input("Enter text to compress: ")

    if len(text) == 0:
        print("Empty input. Exiting.")
    else:
        run_huffman(text)