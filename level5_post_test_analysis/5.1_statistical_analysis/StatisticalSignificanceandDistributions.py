#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
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
    sys.exit(1)

def add_panel_label(image, label_text):
    """Menambahkan label panel ke gambar"""
    try:
        # Convert ke RGB jika perlu
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)  # Font lebih besar untuk Figure 3
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 32)  # Font Linux alternative
            except:
                font = ImageFont.load_default()
        
        # Tambahkan label di pojok kiri atas
        label_bbox = draw.textbbox((0, 0), label_text, font=font)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        
        # Background untuk label
        draw.rectangle([20, 20, 20 + label_width + 25, 20 + label_height + 20], 
                     fill='white')
        draw.rectangle([20, 20, 20 + label_width + 25, 20 + label_height + 20], 
                     outline='black', width=2)
        draw.text((30, 25), label_text, fill='black', font=font)
        
        return image
    except Exception as e:
        print(f"⚠️  Tidak bisa menambahkan label: {e}")
        return image

def resize_to_height(img, target_height):
    """Resize gambar ke tinggi target, maintain aspect ratio"""
    ratio = target_height / img.height
    new_width = int(img.width * ratio)
    return img.resize((new_width, target_height), Image.LANCZOS)

def create_figure3_composite(image_paths, output_name="Figure3_Statistical_Significance.png"):
    """
    Membuat Figure 3: Statistical Significance and Distributions composite
    """
    try:
        # Buka semua gambar
        img1 = Image.open(image_paths[0])  # significance_plot
        img2 = Image.open(image_paths[1])  # confidence_intervals_plot
        img3 = Image.open(image_paths[2])  # throughput_distribution
        
        print("📐 Ukuran gambar asli:")
        print(f"  - Significance Plot: {img1.width} x {img1.height}")
        print(f"  - Confidence Intervals: {img2.width} x {img2.height}")
        print(f"  - Throughput Distribution: {img3.width} x {img3.height}")
        
        # Tentukan tinggi target berdasarkan gambar terkecil
        target_height = min(img1.height, img2.height, img3.height)
        print(f"🎯 Target height: {target_height}")
        
        # Resize semua gambar ke tinggi yang sama
        img1_resized = resize_to_height(img1, target_height)
        img2_resized = resize_to_height(img2, target_height)
        img3_resized = resize_to_height(img3, target_height)
        
        print("📐 Ukuran setelah resize:")
        print(f"  - A: {img1_resized.width} x {img1_resized.height}")
        print(f"  - B: {img2_resized.width} x {img2_resized.height}")
        print(f"  - C: {img3_resized.width} x {img3_resized.height}")
        
        # Tambahkan label panel
        img1_labeled = add_panel_label(img1_resized, "A.")
        img2_labeled = add_panel_label(img2_resized, "B.")
        img3_labeled = add_panel_label(img3_resized, "C.")
        
        # Hitung dimensi total untuk layout horizontal
        total_width = img1_labeled.width + img2_labeled.width + img3_labeled.width
        spacing = 50  # Spacing lebih besar untuk Figure 3
        total_width += 2 * spacing
        
        # Buat canvas putih
        canvas = Image.new('RGB', (total_width, target_height), 'white')
        
        # Tempel gambar dengan spacing
        x_offset = 0
        canvas.paste(img1_labeled, (x_offset, 0))
        x_offset += img1_labeled.width + spacing
        canvas.paste(img2_labeled, (x_offset, 0))
        x_offset += img2_labeled.width + spacing
        canvas.paste(img3_labeled, (x_offset, 0))
        
        # Simpan hasil
        canvas.save(output_name, quality=95)
        print(f"✅ Figure 3 horizontal berhasil dibuat: {output_name}")
        print(f"📐 Ukuran hasil: {total_width} x {target_height} pixels")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_figure3_vertical(image_paths, output_name="Figure3_Vertical_Layout.png"):
    """
    Alternatif layout vertikal untuk Figure 3
    """
    try:
        img1 = Image.open(image_paths[0])
        img2 = Image.open(image_paths[1])
        img3 = Image.open(image_paths[2])
        
        # Tentukan lebar target berdasarkan gambar terlebar
        target_width = max(img1.width, img2.width, img3.width)
        
        # Resize semua gambar ke lebar yang sama
        def resize_to_width(img, width):
            ratio = width / img.width
            height = int(img.height * ratio)
            return img.resize((width, height), Image.LANCZOS)
        
        img1_resized = resize_to_width(img1, target_width)
        img2_resized = resize_to_width(img2, target_width)
        img3_resized = resize_to_width(img3, target_width)
        
        # Tambahkan label panel
        img1_labeled = add_panel_label(img1_resized, "A.")
        img2_labeled = add_panel_label(img2_resized, "B.")
        img3_labeled = add_panel_label(img3_resized, "C.")
        
        # Hitung dimensi total untuk layout vertikal
        total_height = img1_labeled.height + img2_labeled.height + img3_labeled.height
        spacing = 40
        total_height += 2 * spacing
        
        # Buat canvas
        canvas = Image.new('RGB', (target_width, total_height), 'white')
        
        # Tempel gambar
        y_offset = 0
        canvas.paste(img1_labeled, (0, y_offset))
        y_offset += img1_labeled.height + spacing
        canvas.paste(img2_labeled, (0, y_offset))
        y_offset += img2_labeled.height + spacing
        canvas.paste(img3_labeled, (0, y_offset))
        
        canvas.save(output_name, quality=95)
        print(f"✅ Figure 3 vertikal berhasil dibuat: {output_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_figure3_with_header(image_paths, output_name="Figure3_With_Title.png"):
    """
    Versi dengan header/title untuk Figure 3
    """
    try:
        img1 = Image.open(image_paths[0])
        img2 = Image.open(image_paths[1])
        img3 = Image.open(image_paths[2])
        
        # Resize ke tinggi yang sama
        target_height = min(img1.height, img2.height, img3.height)
        img1_resized = resize_to_height(img1, target_height)
        img2_resized = resize_to_height(img2, target_height)
        img3_resized = resize_to_height(img3, target_height)
        
        # Tambahkan label
        img1_labeled = add_panel_label(img1_resized, "A.")
        img2_labeled = add_panel_label(img2_resized, "B.")
        img3_labeled = add_panel_label(img3_resized, "C.")
        
        # Hitung dimensi
        total_width = img1_labeled.width + img2_labeled.width + img3_labeled.width + 100
        header_height = 80
        total_height = target_height + header_height
        
        # Buat canvas
        canvas = Image.new('RGB', (total_width, total_height), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # Tambahkan title
        try:
            font_large = ImageFont.truetype("arial.ttf", 28)
            font_medium = ImageFont.truetype("arial.ttf", 22)
        except:
            try:
                font_large = ImageFont.truetype("DejaVuSans.ttf", 28)
                font_medium = ImageFont.truetype("DejaVuSans.ttf", 22)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
        
        # Judul utama
        title = "Figure 3: Statistical Significance and Distributions"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (total_width - title_width) // 2
        draw.text((title_x, 20), title, fill='black', font=font_large)
        
        # Subtitle
        subtitle = "VPN Protocols Performance Analysis"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (total_width - subtitle_width) // 2
        draw.text((subtitle_x, 55), subtitle, fill='darkblue', font=font_medium)
        
        # Tempel gambar
        x_offset = (total_width - (img1_labeled.width + img2_labeled.width + img3_labeled.width + 80)) // 2
        y_offset = header_height
        
        canvas.paste(img1_labeled, (x_offset, y_offset))
        x_offset += img1_labeled.width + 40
        canvas.paste(img2_labeled, (x_offset, y_offset))
        x_offset += img2_labeled.width + 40
        canvas.paste(img3_labeled, (x_offset, y_offset))
        
        canvas.save(output_name, quality=95)
        print(f"✅ Figure 3 dengan title berhasil dibuat: {output_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Main execution
if __name__ == "__main__":
    # Cek Pillow terinstall
    if not check_pillow():
        install_pillow_ubuntu()
    
    # File gambar untuk Figure 3
    figure3_images = [
        "significance_plot.png",
        "confidence_intervals_plot.png", 
        "throughput_distribution.png"
    ]
    
    # Cek file mana yang ada
    available_images = []
    for img_file in figure3_images:
        if os.path.exists(img_file):
            available_images.append(img_file)
            print(f"✅ Ditemukan: {img_file}")
        else:
            # Coba cari file dengan pattern yang mirip
            possible_names = [
                img_file,
                "significance_plot.png",
                "confidence_intervals.png",
                "throughput_distribution.png",
                "statistical_significance.png"
            ]
            
            found = False
            for possible_name in possible_names:
                if os.path.exists(possible_name):
                    available_images.append(possible_name)
                    print(f"✅ Ditemukan: {possible_name}")
                    found = True
                    break
            
            if not found:
                print(f"❌ Tidak ditemukan: {img_file}")
    
    if len(available_images) == 3:
        print("\n🎨 Membuat Figure 3: Statistical Significance and Distributions...")
        print("📊 Panel Description:")
        print("  • A. Statistical Significance of Pairwise Comparisons")
        print("  • B. Mean Throughput with 95% Confidence Intervals") 
        print("  • C. Throughput Distribution by Protocol")
        
        # Buat berbagai versi Figure 3
        create_figure3_composite(available_images, "Figure3_Statistical_Significance.png")
        create_figure3_vertical(available_images, "Figure3_Vertical_Layout.png")
        create_figure3_with_header(available_images, "Figure3_With_Title.png")
        
        print("\n📋 Hasil yang dibuat:")
        print("• Figure3_Statistical_Significance.png - Layout horizontal")
        print("• Figure3_Vertical_Layout.png - Layout vertikal")
        print("• Figure3_With_Title.png - Dengan judul Figure 3")
        
        print("\n✅ Fitur yang diterapkan:")
        print("  ✓ Label A, B, C konsisten di semua gambar")
        print("  ✓ Ukuran gambar disesuaikan untuk konsistensi")
        print("  ✓ Multiple layout options")
        print("  ✓ Kualitas tinggi (95% quality)")
        
    elif available_images:
        print(f"\n⚠️  Hanya ditemukan {len(available_images)} gambar dari 3")
        print("Membuat composite dengan gambar yang tersedia...")
        create_figure3_composite(available_images, "Figure3_Partial.png")
    else:
        print("\n❌ Tidak ada gambar yang ditemukan!")
        print("Pastikan file gambar berada di folder yang sama dengan script ini.")