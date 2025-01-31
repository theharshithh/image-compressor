import streamlit as st
import numpy as np
from PIL import Image
import io
from image_compressor import ImageCompressor
import matplotlib.pyplot as plt

st.set_page_config(page_title="Image Compression Visualizer", layout="wide")

st.title("Image Compression using Huffman Coding")



st.markdown("""
### Project Information
Name: Harshith K Murthy  
USN: 1RV22ET020
Course: Communication Engineering - II

**Submitted to:**  Dr. P N Nagraj

---
""")

st.write("""
This application demonstrates the implementation of image compression using Huffman coding algorithm. 
The visualization shows:
- The compression process
- Huffman tree visualization
- Compression statistics
- Before/After comparison
""")

uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)
    

    compressor = ImageCompressor()
    
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    compressed_data, compression_ratio = compressor.compress("temp_image.png", visualize=False)
    
    gray_image = np.array(image.convert('L'))
    
    sample_pixels = compressor.get_sample_pixels(gray_image)
    
    with col2:
        st.subheader("Compressed Image")
        decompressed_image = compressor.decompress()
        st.image(decompressed_image, use_column_width=True)
    
    st.subheader("Compression Statistics")
    stats = compressor.get_compression_stats(gray_image)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Compression Ratio", f"{stats['compression_ratio']:.2f}x")
    with stat_col2:
        st.metric("Space Saved", f"{stats['space_saved']:.1f}%")
    with stat_col3:
        original_kb = stats['original_size'] / 8 / 1024
        compressed_kb = stats['compressed_size'] / 8 / 1024
        st.metric("Size Reduction", f"{original_kb:.1f}KB → {compressed_kb:.1f}KB")
    
    st.subheader("Huffman Code Distribution")
    fig = compressor.visualize_compression(gray_image, compression_ratio)
    st.pyplot(fig)
    plt.close()
    
    st.subheader("Huffman Tree Visualization (Sample)")
    st.write("""
    This is a visualization of the Huffman tree for the most frequent pixel values.
    - Blue nodes represent the most frequent pixel values
    - Edge labels (0/1) represent the binary codes
    - Frequency shows how often each pixel value appears
    """)
    
    dot = compressor.visualize_huffman_tree(sample_pixels)
    if dot:
        dot.render("huffman_tree", format="png", cleanup=True)
        st.image("huffman_tree.png")
    
    st.subheader("Sample Pixel Codes")
    code_data = []
    for pixel, freq in sample_pixels.items():
        code = compressor.huffman_codes[pixel]
        code_data.append({
            "Pixel Value": pixel,
            "Frequency": freq,
            "Huffman Code": code,
            "Code Length": len(code)
        })
    
    st.table(code_data)
    
    import os
    if os.path.exists("temp_image.png"):
        os.remove("temp_image.png")
    if os.path.exists("huffman_tree.png"):
        os.remove("huffman_tree.png")
    if os.path.exists("huffman_tree"):
        os.remove("huffman_tree") 