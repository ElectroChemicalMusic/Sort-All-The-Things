from util import list_files_in_directory, is_dir, more_audio_or_image, determine_category
import tkinter as tk
from tkinter import simpledialog
from image_sort import sort_blocks_by_brightness
from audio_sort import start_audio_sorting_in_thread
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD


class AudioFormatDialog(simpledialog.Dialog):
    def body(self, master):
        self.var = tk.StringVar(master)
        self.var.set("mp3")

        tk.Label(master, text="Choose your audio format:").pack()
        tk.Radiobutton(master, text="MP3", variable=self.var, value="mp3").pack(
            anchor=tk.W
        )
        tk.Radiobutton(master, text="WAV", variable=self.var, value="wav").pack(
            anchor=tk.W
        )
        return None

    def apply(self):
        self.result = self.var.get()


def get_inputs_for_image(parent):
    block_width = simpledialog.askinteger("Input", "Enter block width:", parent=parent)
    block_height = simpledialog.askinteger(
        "Input", "Enter block height:", parent=parent
    )
    return block_height, block_width


def get_inputs_for_audio(parent):
    times_per_second = simpledialog.askinteger(
        "Input",
        "Audio chunk size in milliseconds:",
        parent=parent,
    )
    output_filename = simpledialog.askstring(
        "Input",
        "Whatchya wanna call it when it's done?",
        parent=parent,
    )
    wav_or_mp3 = AudioFormatDialog(parent, title="Choose Audio Format")
    return times_per_second, wav_or_mp3, output_filename


def on_drop(event):
    file_path = event.data
    is_directory = False
    file_list = []
    category = ""
    if file_path:
        file_path = file_path.strip("{}")
        is_directory = is_dir(file_path)
        if is_directory:
            file_list = list_files_in_directory(file_path)
            category = more_audio_or_image(file_list)
        else:
            category = determine_category(file_path)
    if category == "" or category == "Wrong filetypes ya doinkus":
        messagebox.showerror("Error", "Wrong filetype(s) ya doinkus.")
    elif category == "audio":
        slices_per_second, wav_or_mp3, output_filename = get_inputs_for_audio(event.widget)
        if is_directory:
            start_audio_sorting_in_thread(file_list, slices_per_second, wav_or_mp3, output_filename, event.widget)
        else:
            start_audio_sorting_in_thread([file_path], slices_per_second, wav_or_mp3, output_filename, event.widget)
    elif category == "image":
        block_height, block_width = get_inputs_for_image(event.widget)
        if is_directory:
            sort_blocks_by_brightness(file_path, block_height, block_width, event.widget)
        else:
            sort_blocks_by_brightness([file_path], block_height, block_width, event.widget)


def create_drag_drop_window():
    root = TkinterDnD.Tk()
    root.title("Sort Stuff!")
    root.geometry("600x600")

    drop_label = tk.Label(
        root, text="HEY FAM YOU WANNA SORT SOME SHIT?\nYou can add audio files, images, or folders containing either. \n"
                   "Folders with multiple audio files will sum them all together into one big honkus",
        relief=tk.SUNKEN, width=40, height=10
    )
    drop_label.pack(expand=True, fill=tk.BOTH)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind("<<Drop>>", on_drop)

    root.mainloop()


if __name__ == "__main__":
    try:
        create_drag_drop_window()
    except Exception as e:
        print(e)
    input("Press Enter to exit...")
