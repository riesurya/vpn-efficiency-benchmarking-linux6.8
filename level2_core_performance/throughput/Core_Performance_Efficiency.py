#!/usr/bin/env python3
from PIL import Image
import os
import sys

def check_pillow():
    """Cek apakah Pillow terinstall"""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False

def install_pillow_ubuntu():
    """Instruksi install Pillow untuk Ubuntu"""
    print("❌ Pillow tidak terinstall!")
    print("\n📦 Silakan install dengan salah satu cara berikut:")
    print("\n1. Via apt (recommended):")
    print("   sudo apt update && sudo apt install python3-pil")
    print("\n2. Via pip3:")
    print("   pip3 install Pillow")
    print("\n3. Untuk Python virtual environment:")
    print("   pip install Pillow")
    sys.exit(1)

def create_3_panel_composite(image_paths, output_name="vpn_performance_composite.png"):
    """
    Membuat 3-panel composite dari tiga gambar
    """
    try:
        # Buka semua gambar
        images = [Image.open(img) for img in image_paths]
        
        # Cek ukuran gambar
        widths, heights = zip(*(img.size for img in images))
        
        # Buat canvas baru untuk layout vertikal
        max_width = max(widths)
        total_height = sum(heights)
        
        # Tambahkan spacing antara gambar
        spacing = 20
        total_height += 2 * spacing
        
        # Buat canvas putih
        canvas = Image.new('RGB', (max_width, total_height), 'white')
        
        # Tempel gambar dengan spacing
        y_offset = 0
        for i, img in enumerate(images):
            # Center gambar jika lebarnya lebih kecil
            x_offset = (max_width - img.width) // 2
            canvas.paste(img, (x_offset, y_offset))
            y_offset += img.height + spacing
        
        # Simpan hasil
        canvas.save(output_name, quality=95)
        print(f"✅ Composite berhasil dibuat: {output_name}")
        print(f"📐 Ukuran hasil: {max_width} x {total_height} pixels")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_3_panel_horizontal(image_paths, output_name="vpn_performance_horizontal.png"):
    """
    Alternatif: layout horizontal untuk 3 panel
    """
    try:
        images = [Image.open(img) for img in image_paths]
        
        # Sesuaikan tinggi gambar agar sama
        min_height = min(img.height for img in images)
        images_resized = []
        
        for img in images:
            if img.height != min_height:
                # Resize maintaining aspect ratio
                ratio = min_height / img.height
                new_width = int(img.width * ratio)
                img = img.resize((new_width, min_height), Image.LANCZOS)
            images_resized.append(img)
        
        widths = [img.width for img in images_resized]
        total_width = sum(widths)
        max_height = min_height
        
        # Tambahkan spacing
        spacing = 15
        total_width += 2 * spacing
        
        canvas = Image.new('RGB', (total_width, max_height), 'white')
        
        x_offset = 0
        for img in images_resized:
            canvas.paste(img, (x_offset, 0))
            x_offset += img.width + spacing
        
        canvas.save(output_name, quality=95)
        print(f"✅ Horizontal composite berhasil dibuat: {output_name}")
        print(f"📐 Ukuran hasil: {total_width} x {max_height} pixels")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Main execution
if __name__ == "__main__":
    # Cek Pillow terinstall
    if not check_pillow():
        install_pillow_ubuntu()
    
    # File gambar - sesuaikan dengan nama file yang sebenarnya
    image_files = [
        "throughputStabilityAnalysis:UnidirectionalSingleStreamPerformanceOverTime.png",
        "averageThroughputPerformance:WireGuardVsIPSecVsOpenVPNByTrafficDirection.png",
        "cpuUtilizationComparison:WireGuardVsIPSecVsOpenVPNByTestConfiguration.png"
    ]
    
    # Cek file mana yang ada
    available_images = []
    for img_file in image_files:
        if os.path.exists(img_file):
            available_images.append(img_file)
            print(f"✅ Ditemukan: {img_file}")
        else:
            # Coba dengan nama yang disederhanakan
            simplified_name = img_file.split(':')[0] + ".png" if ':' in img_file else img_file
            if os.path.exists(simplified_name):
                available_images.append(simplified_name)
                print(f"✅ Ditemukan: {simplified_name}")
            else:
                print(f"❌ Tidak ditemukan: {img_file}")
    
    if len(available_images) == 3:
        print("\n🎨 Membuat composite gambar...")
        
        # Buat versi vertikal
        create_3_panel_composite(available_images, "vpn_composite_vertical.png")
        
        # Buat versi horizontal  
        create_3_panel_horizontal(available_images, "vpn_composite_horizontal.png")
        
        print("\n📋 Hasil yang dibuat:")
        print("• vpn_composite_vertical.png - Layout vertikal")
        print("• vpn_composite_horizontal.png - Layout horizontal")
        
    elif available_images:
        print(f"\n⚠️  Hanya ditemukan {len(available_images)} gambar dari 3")
        print("Membuat composite dengan gambar yang tersedia...")
        create_3_panel_composite(available_images, "vpn_composite_partial.png")
    else:
        print("\n❌ Tidak ada gambar yang ditemukan!")
        print("Pastikan:")
        print("1. File gambar berada di folder yang sama dengan script")
        print("2. Nama file sesuai")
        print("3. Ekstensi file adalah .png")

