from PIL import Image, ImageDraw, ImageFont
import sys

def create_watermark_image(text, font_size, line_spacing=10):
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    lines = text.split('\n')
    max_width = 0
    total_height = 0

    for line in lines:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]

        max_width = max(max_width, line_width)
        total_height += line_height + line_spacing

    total_height -= line_spacing 

    watermark_image = Image.new("RGBA", (max_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_image)

    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=(255, 255, 255, 128))
        y += font.getbbox(line)[3] - font.getbbox(line)[1] + line_spacing

    return watermark_image

def add_watermark(image_path, watermark_text, output_path, font_size=50):
    try:
        image = Image.open(image_path).convert("RGBA")
        width, height = image.size

        
        watermark_image = create_watermark_image(watermark_text, font_size)
        wm_width, wm_height = watermark_image.size

        
        watermark_tiling = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        for x in range(0, width, wm_width):
            for y in range(0, height, wm_height):
                watermark_tiling.paste(watermark_image, (x, y), watermark_image)

        
        watermarked_image = Image.alpha_composite(image, watermark_tiling)

        
        watermarked_image = watermarked_image.convert("RGB") 
        watermarked_image.save(output_path)
        print(f"Watermark berhasil ditambahkan dan disimpan di {output_path}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Penggunaan: python3 watermark.py <lokasi_gambar> <watermark_text> <lokasi_output>")
    else:
        image_path = sys.argv[1]
        watermark_text = sys.argv[2]
        output_path = sys.argv[3]
        add_watermark(image_path, watermark_text, output_path)
