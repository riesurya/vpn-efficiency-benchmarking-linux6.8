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
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        # Tambahkan label di pojok kiri atas
        label_bbox = draw.textbbox((0, 0), label_text, font=font)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        
        # Background untuk label
        draw.rectangle([15, 15, 15 + label_width + 20, 15 + label_height + 15], 
                     fill='white')
        draw.rectangle([15, 15, 15 + label_width + 20, 15 + label_height + 15], 
                     outline='black', width=2)
        draw.text((25, 20), label_text, fill='black', font=font)
        
        return image
    except Exception as e:
        print(f"⚠️  Tidak bisa menambahkan label: {e}")
        return image

def create_final_horizontal_composite(image_paths, output_name="Figure2_Horizontal_Final.png"):
    """
    Membuat 3-panel horizontal final dengan penyesuaian yang diminta
    """
    try:
        # Buka dan proses gambar dengan resize yang sesuai
        img1 = Image.open(image_paths[0])  # CPU Usage
        img2 = Image.open(image_paths[1])  # Latency Degradation
        img3 = Image.open(image_paths[2])  # Resource Efficiency
        
        # Resize gambar Resource Efficiency lebih kecil (50% scale)
        print("🔧 Meresize gambar Resource Efficiency menjadi 50%...")
        new_width = int(img3.width * 0.5)
        new_height = int(img3.height * 0.5)
        img3_resized = img3.resize((new_width, new_height), Image.LANCZOS)
        
        # Sesuaikan tinggi gambar lainnya dengan gambar Resource Efficiency yang sudah di-resize
        target_height = img3_resized.height
        
        # Resize gambar lain ke tinggi yang sama, maintain aspect ratio
        def resize_to_height(img, height):
            ratio = height / img.height
            width = int(img.width * ratio)
            return img.resize((width, height), Image.LANCZOS)
        
        img1_resized = resize_to_height(img1, target_height)
        img2_resized = resize_to_height(img2, target_height)
        
        print(f"📐 Ukuran setelah adjustment:")
        print(f"  - CPU Usage: {img1_resized.width} x {img1_resized.height}")
        print(f"  - Latency Degradation: {img2_resized.width} x {img2_resized.height}")
        print(f"  - Resource Efficiency: {img3_resized.width} x {img3_resized.height}")
        
        # Tambahkan label panel ke setiap gambar
        img1_labeled = add_panel_label(img1_resized, "A.")
        img2_labeled = add_panel_label(img2_resized, "B.")
        img3_labeled = add_panel_label(img3_resized, "C.")
        
        # Hitung dimensi total
        total_width = img1_labeled.width + img2_labeled.width + img3_labeled.width
        spacing = 40  # Spacing lebih besar untuk hasil yang rapi
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
        
        # Simpan hasil dengan kualitas tinggi
        canvas.save(output_name, quality=95)
        print(f"✅ 3-panel horizontal final berhasil dibuat: {output_name}")
        print(f"📐 Ukuran hasil: {total_width} x {target_height} pixels")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_alternative_sizes(image_paths):
    """
    Membuat beberapa alternatif dengan ukuran berbeda
    """
    try:
        img1 = Image.open(image_paths[0])
        img2 = Image.open(image_paths[1])
        img3 = Image.open(image_paths[2])
        
        # Alternatif 1: Resource Efficiency 40% scale
        img3_small = img3.resize((int(img3.width * 0.4), int(img3.height * 0.4)), Image.LANCZOS)
        target_height = img3_small.height
        
        def resize_to_height(img, height):
            ratio = height / img.height
            width = int(img.width * ratio)
            return img.resize((width, height), Image.LANCZOS)
        
        img1_resized = resize_to_height(img1, target_height)
        img2_resized = resize_to_height(img2, target_height)
        
        # Tambahkan label
        img1_labeled = add_panel_label(img1_resized, "A.")
        img2_labeled = add_panel_label(img2_resized, "B.")
        img3_labeled = add_panel_label(img3_small, "C.")
        
        total_width = img1_labeled.width + img2_labeled.width + img3_labeled.width + 80
        canvas = Image.new('RGB', (total_width, target_height), 'white')
        
        x_offset = 0
        canvas.paste(img1_labeled, (x_offset, 0))
        x_offset += img1_labeled.width + 40
        canvas.paste(img2_labeled, (x_offset, 0))
        x_offset += img2_labeled.width + 40
        canvas.paste(img3_labeled, (x_offset, 0))
        
        canvas.save("Figure2_Horizontal_Smaller.png", quality=95)
        print("✅ Alternatif dengan Resource Efficiency 40% scale dibuat: Figure2_Horizontal_Smaller.png")
        
        # Alternatif 2: Semua gambar di-resize ke tinggi terkecil
        min_height = min(img1.height, img2.height, img3.height)
        img1_alt = resize_to_height(img1, min_height)
        img2_alt = resize_to_height(img2, min_height)
        img3_alt = resize_to_height(img3, min_height)
        
        # Resize Resource Efficiency tambahan
        img3_alt_small = img3_alt.resize((int(img3_alt.width * 0.6), int(img3_alt.height * 0.6)), Image.LANCZOS)
        
        img1_alt_labeled = add_panel_label(img1_alt, "A.")
        img2_alt_labeled = add_panel_label(img2_alt, "B.")
        img3_alt_labeled = add_panel_label(img3_alt_small, "C.")
        
        total_width_alt = img1_alt_labeled.width + img2_alt_labeled.width + img3_alt_labeled.width + 80
        canvas_alt = Image.new('RGB', (total_width_alt, min_height), 'white')
        
        x_offset = 0
        canvas_alt.paste(img1_alt_labeled, (x_offset, 0))
        x_offset += img1_alt_labeled.width + 40
        canvas_alt.paste(img2_alt_labeled, (x_offset, 0))
        x_offset += img2_alt_labeled.width + 40
        canvas_alt.paste(img3_alt_labeled, (x_offset, (min_height - img3_alt_labeled.height) // 2))
        
        canvas_alt.save("Figure2_Horizontal_Adjusted.png", quality=95)
        print("✅ Alternatif dengan penyesuaian tinggi dibuat: Figure2_Horizontal_Adjusted.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Error dalam alternatif: {e}")
        return False

# Main execution
if __name__ == "__main__":
    # Cek Pillow terinstall
    if not check_pillow():
        install_pillow_ubuntu()
    
    # File gambar untuk Figure 2
    figure2_images = [
        "CPU Usage Prediction vs Connection Load.png",
        "Latency Degradation (1 to 50 Connections).png", 
        "Comprehensive Resource Efficiency Analysis:VPN Protocols Performance Comparison.png"
    ]
    
    # Cek file mana yang ada
    available_images = []
    for img_file in figure2_images:
        if os.path.exists(img_file):
            available_images.append(img_file)
            print(f"✅ Ditemukan: {img_file}")
        else:
            # Coba cari file dengan pattern yang mirip
            possible_names = [
                img_file,
                img_file.replace(":", ""),
                "CPU Usage Prediction vs Connection Load.png",
                "Latency Degradation.png", 
                "Resource Efficiency Analysis.png",
                "Comprehensive Resource Efficiency Analysis VPN Protocols Performance Comparison.png"
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
        print("\n🎨 Membuat 3-panel horizontal final...")
        print("🔧 Penyesuaian yang dilakukan:")
        print("  • Gambar Resource Efficiency diperkecil 50%")
        print("  • Label A, B, C ditambahkan ke setiap gambar")
        print("  • Tinggi semua gambar disamakan")
        print("  • Tidak ada caption/title tambahan")
        
        # Buat versi final
        create_final_horizontal_composite(available_images, "Figure2_Horizontal_Final.png")
        
        # Buat alternatif ukuran
        create_alternative_sizes(available_images)
        
        print("\n📋 Hasil yang dibuat:")
        print("• Figure2_Horizontal_Final.png - Versi final (50% scale)")
        print("• Figure2_Horizontal_Smaller.png - Resource Efficiency 40% scale") 
        print("• Figure2_Horizontal_Adjusted.png - Dengan penyesuaian tinggi")
        
        print("\n✅ Fitur yang diterapkan:")
        print("  ✓ Gambar Resource Efficiency diperkecil signifikan")
        print("  ✓ Label A, B, C konsisten di semua gambar")
        print("  ✓ Tidak ada caption/title tambahan")
        print("  ✓ Layout horizontal rapi")
        print("  ✓ Legend pada gambar C seharusnya sudah tampak jelas")
        
    elif available_images:
        print(f"\n⚠️  Hanya ditemukan {len(available_images)} gambar dari 3")
        print("Membuat composite dengan gambar yang tersedia...")
        create_final_horizontal_composite(available_images, "Figure2_Partial_Horizontal.png")
    else:
        print("\n❌ Tidak ada gambar yang ditemukan!")
        print("Pastikan file gambar berada di folder yang sama dengan script ini.")