# Image Compression using Huffman Coding

This project implements image compression using Huffman coding, demonstrating the internal workings of image compression algorithms. It provides a comprehensive visualization of the compression process, including the Huffman tree distribution and compression metrics.

## Features

- Image compression using Huffman coding algorithm
- Visualization of compression process and results
- Support for various image formats (PNG, JPG, JPEG)
- Detailed compression metrics and statistics
- Interactive visualization of Huffman code distribution
- Save and load compressed image data
- Batch processing of multiple images

## Requirements

- Python 3.7+
- NumPy
- Pillow (PIL)
- Matplotlib
- tqdm
- Streamlit
- Graphviz

We recommend using `uv` for dependency management as it's significantly faster than pip. Here's how to set up:

1. First, install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

   Alternatively, you can use:
   ```bash
   uv sync
   ```

## Project Structure

```
.
├── image_compressor.py  # Main implementation of the compression algorithm
├── app.py              # Streamlit web application
├── demo.py             # Demo script to showcase compression
├── requirements.txt    # Project dependencies
├── samples/           # Directory for test images
└── README.md          # Project documentation
```

## How to Use

1. Set up the environment as described in the Requirements section.

2. Place your test images in the `samples` directory or use the streamlit app to upload images.

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

   Or run the demo script:
   ```bash
   python demo.py
   ```

The application will:
- Process uploaded images (or images in samples directory for demo)
- Show the original and compressed images
- Display compression metrics
- Visualize the Huffman tree and code distribution
- Save the compressed and decompressed versions

## Technical Details

### Compression Process

1. **Image Loading**: 
   - Images are loaded and converted to grayscale
   - Pixel values are extracted as a numpy array

2. **Huffman Coding**:
   - Pixel frequencies are calculated
   - Huffman tree is built based on pixel frequencies
   - Huffman codes are generated for each pixel value

3. **Compression**:
   - Pixels are encoded using the generated Huffman codes
   - Compressed data is stored efficiently
   - Compression metrics are calculated

4. **Visualization**:
   - Original vs. compressed image comparison
   - Huffman code distribution visualization
   - Compression metrics display

### Performance Metrics

The following metrics are calculated and displayed:
- Compression ratio
- Original file size
- Compressed file size
- Percentage of space saved

## Example Output

When you run the application, you'll see:
1. Original image alongside the compressed version
2. Histogram showing the distribution of Huffman codes
3. Interactive Huffman tree visualization
4. Detailed compression metrics

## Contributing

Feel free to contribute to this project by:
1. Adding new features
2. Improving the compression algorithm
3. Enhancing visualizations
4. Fixing bugs
5. Improving documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
