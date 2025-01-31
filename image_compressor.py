import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import heapq
from tqdm import tqdm
import os
import graphviz

class HuffmanNode:
    def __init__(self, value=None, freq=None):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

class ImageCompressor:
    def __init__(self):
        self.huffman_tree = None
        self.huffman_codes = {}
        self.original_shape = None
        self.compressed_data = None
        self.pixel_frequencies = None
        
    def build_huffman_tree(self, pixel_freq):
        """Build Huffman tree from pixel frequencies"""
        self.pixel_frequencies = pixel_freq
        heap = []
        for value, freq in pixel_freq.items():
            node = HuffmanNode(value, freq)
            heapq.heappush(heap, node)
            
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            internal_node = HuffmanNode(freq=left.freq + right.freq)
            internal_node.left = left
            internal_node.right = right
            
            heapq.heappush(heap, internal_node)
            
        self.huffman_tree = heap[0]
        
    def generate_huffman_codes(self, node=None, code=""):
        """Generate Huffman codes for each pixel value"""
        if node is None:
            node = self.huffman_tree
            
        if node.value is not None:
            self.huffman_codes[node.value] = code
            return
            
        self.generate_huffman_codes(node.left, code + "0")
        self.generate_huffman_codes(node.right, code + "1")
        
    def compress(self, image_path, visualize=True):
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        self.original_shape = img_array.shape
        
        pixel_freq = Counter(img_array.flatten())
        
        self.build_huffman_tree(pixel_freq)
        self.generate_huffman_codes()
        
        compressed = ''.join(self.huffman_codes[pixel] for pixel in img_array.flatten())
        self.compressed_data = compressed

        original_size = img_array.size * 8  # 8 bits per pixel
        compressed_size = len(compressed)
        compression_ratio = original_size / compressed_size
        
        if visualize:
            self.visualize_compression(img_array, compression_ratio)
            
        return compressed, compression_ratio
    
    def get_sample_pixels(self, img_array, sample_size=5):
        flattened = img_array.flatten()
        unique_pixels = np.unique(flattened)
        
        pixel_freq = Counter(flattened)
        sample_pixels = dict(sorted(pixel_freq.items(), key=lambda x: x[1], reverse=True)[:sample_size])
        
        return sample_pixels
    
    def visualize_huffman_tree(self, sample_pixels=None):
        if not self.huffman_tree:
            return None
            
        dot = graphviz.Digraph(comment='Huffman Tree')
        dot.attr(rankdir='TB')
        
        def add_nodes_edges(node, node_id=0):
            if node is None:
                return
                
            if node.value is not None:
                if sample_pixels and node.value in sample_pixels:
                    dot.node(str(node_id), f'Value: {node.value}\nFreq: {node.freq}', 
                            style='filled', fillcolor='lightblue')
                else:
                    dot.node(str(node_id), f'Value: {node.value}\nFreq: {node.freq}')
            else:
                dot.node(str(node_id), f'Freq: {node.freq}')
                
            if node.left:
                left_id = node_id * 2 + 1
                dot.edge(str(node_id), str(left_id), '0')
                add_nodes_edges(node.left, left_id)
                
            if node.right:
                right_id = node_id * 2 + 2
                dot.edge(str(node_id), str(right_id), '1')
                add_nodes_edges(node.right, right_id)
                
        add_nodes_edges(self.huffman_tree)
        return dot
        
    def decompress(self):
        if not self.compressed_data or not self.huffman_tree:
            raise ValueError("No compressed data available")
            
        current = self.huffman_tree
        decompressed = []
        
        for bit in tqdm(self.compressed_data, desc="Decompressing"):
            if bit == '0':
                current = current.left
            else:
                current = current.right
                
            if current.value is not None:
                decompressed.append(current.value)
                current = self.huffman_tree
                
        decompressed_array = np.array(decompressed).reshape(self.original_shape)
        return Image.fromarray(decompressed_array.astype(np.uint8))
        
    def visualize_compression(self, original_array, compression_ratio):
        plt.figure(figsize=(15, 5))
        
        plt.subplot(131)
        plt.imshow(original_array, cmap='gray')
        plt.title('Original Image')
        plt.axis('off')
        
        plt.subplot(132)
        self._plot_huffman_tree_distribution()
        plt.title('Huffman Codes Distribution')
        
        plt.subplot(133)
        plt.text(0.5, 0.5, f'Compression Ratio: {compression_ratio:.2f}x\n'
                          f'Original Size: {original_array.size * 8} bits\n'
                          f'Compressed Size: {len(self.compressed_data)} bits\n'
                          f'Space Saved: {(1 - 1/compression_ratio)*100:.1f}%',
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=plt.gca().transAxes)
        plt.axis('off')
        
        plt.tight_layout()
        return plt
        
    def _plot_huffman_tree_distribution(self):
        code_lengths = [len(code) for code in self.huffman_codes.values()]
        plt.hist(code_lengths, bins=range(min(code_lengths), max(code_lengths) + 2, 1),
                alpha=0.7, color='blue', edgecolor='black')
        plt.xlabel('Code Length (bits)')
        plt.ylabel('Frequency')
        
    def get_compression_stats(self, original_array):
        original_size = original_array.size * 8
        compressed_size = len(self.compressed_data)
        compression_ratio = original_size / compressed_size
        space_saved = (1 - 1/compression_ratio) * 100
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'space_saved': space_saved
        }
        
    def save_compressed(self, output_path):
        if not self.compressed_data:
            raise ValueError("No compressed data available")
            
        compressed_data = {
            'data': self.compressed_data,
            'shape': self.original_shape,
            'codes': self.huffman_codes
        }
        np.save(output_path, compressed_data)
        
    @staticmethod
    def load_compressed(input_path):
        compressed_data = np.load(input_path, allow_pickle=True).item()
        compressor = ImageCompressor()
        compressor.compressed_data = compressed_data['data']
        compressor.original_shape = compressed_data['shape']
        compressor.huffman_codes = compressed_data['codes']
        return compressor 