import os


def clean_path_list(list_of_paths):
    clean_list = []
    for path in list_of_paths:
        if path.endswith((".png", ".jpg", ".jpeg", ".gif", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma",
                          ".alac", ".aiff")):
            clean_list.append(path)
    return clean_list


def list_files_in_directory(directory_path):
    list_of_paths = [
        os.path.join(directory_path, f)
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]
    return clean_path_list(list_of_paths)


def get_filename(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension


def is_dir(file_path):
    if os.path.isdir(file_path):
        return True
    else:
        return False


def determine_category(filename):
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
        return "image"
    elif filename.endswith(
        (".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff")
    ):
        return "audio"
    else:
        return "Wrong filetypes ya doinkus"


def more_audio_or_image(filenames):
    img_count = 0
    audio_count = 0
    for filename in filenames:
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            img_count += 1
        elif filename.endswith(
            (".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff")
        ):
            audio_count += 1
    if img_count > audio_count:
        return "image"
    elif audio_count > img_count:
        return "audio"
    elif audio_count == 0 and img_count == 0:
        return "Wrong filetypes ya doinkus"
