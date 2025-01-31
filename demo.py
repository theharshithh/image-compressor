from image_compressor import ImageCompressor
import os
from PIL import Image
import matplotlib.pyplot as plt

def main():
    if not os.path.exists('samples'):
        os.makedirs('samples')
        print("Please place some test images in the 'samples' directory before running this demo.")
        return

    compressor = ImageCompressor()
    
    for filename in os.listdir('samples'):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join('samples', filename)
            print(f"\nProcessing {filename}...")
            
            compressed_data, compression_ratio = compressor.compress(image_path)
            
            compressed_path = os.path.join('samples', f'{os.path.splitext(filename)[0]}_compressed.npy')
            compressor.save_compressed(compressed_path)
            
            decompressed_image = compressor.decompress()
            
            decompressed_path = os.path.join('samples', f'{os.path.splitext(filename)[0]}_decompressed.png')
            decompressed_image.save(decompressed_path)
            
            plt.figure(figsize=(15, 5))
            
            plt.subplot(121)
            original_img = Image.open(image_path).convert('L')
            plt.imshow(original_img, cmap='gray')
            plt.title('Original Image')
            plt.axis('off')
            
            plt.subplot(122)
            plt.imshow(decompressed_image, cmap='gray')
            plt.title('Decompressed Image')
            plt.axis('off')
            
            plt.suptitle(f'Compression Ratio: {compression_ratio:.2f}x\nSpace Saved: {(1 - 1/compression_ratio)*100:.1f}%')
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main() 