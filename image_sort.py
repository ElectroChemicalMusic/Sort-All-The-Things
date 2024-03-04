import numpy as np
from PIL import Image
from util import get_filename
import threading


def block_brightness(block):
    luminance = np.dot(block, [0.2126, 0.7152, 0.0722])
    return luminance.mean()


def sort_blocks_by_brightness(image_paths, block_height, block_width, widget):
    widget.config(text="Images are pretty quick compared to songs, so you should see a result soon. \n"
                       "Drag more on to here to sort more!")
    for filename in image_paths:
        if not filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            image_paths.remove(filename)
    block_size = (block_height, block_width)
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = np.array(img)
        img_title = (
            image_path.replace(".jpg", "")
            .replace(".webp", "")
            .replace(".png", "")
            .replace("input_images/", "")
        )

        height, width, _ = pixels.shape
        block_height, block_width = block_size

        num_blocks_vertical = height // block_height
        num_blocks_horizontal = width // block_width
        blocks = []

        for y in range(0, num_blocks_vertical):
            for x in range(0, num_blocks_horizontal):
                block = pixels[
                    y * block_height : (y + 1) * block_height,
                    x * block_width : (x + 1) * block_width,
                ]
                avg_brightness = block_brightness(block)
                blocks.append((avg_brightness, block))

        blocks.sort(key=lambda x: x[0])

        new_img = np.zeros_like(pixels)

        for y in range(0, num_blocks_vertical):
            for x in range(0, num_blocks_horizontal):
                index = y * num_blocks_horizontal + x
                block = blocks[index][1]
                new_img[
                    y * block_height : (y + 1) * block_height,
                    x * block_width : (x + 1) * block_width,
                ] = block

        new_img = Image.fromarray(new_img)

        new_img_path = f"output_images/{(get_filename(img_title))} Sorted.png"
        new_img.save(new_img_path)
        new_img.show()

    return new_img_path

def start_image_sorting_in_thread(filenames, slices_per_second, wav_or_mp3, output_filename, widget):
    def worker():
        sort_blocks_by_brightness(filenames, slices_per_second, wav_or_mp3.result, output_filename, widget)

    thread = threading.Thread(target=worker)
    thread.start()
