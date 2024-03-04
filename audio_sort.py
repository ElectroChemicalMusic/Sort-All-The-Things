from pydub import AudioSegment
import librosa
import numpy as np
import threading


def combine_and_sort_audio(filenames, segment_length, output_filetype, output_filename, widget):
    combined_audio = AudioSegment.empty()
    for filename in filenames:
        if not filename.endswith((".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff")):
            filenames.remove(filename)
    widget.config(text="We gon processs this shit, this is juiceable. Give it time,")
    for song in filenames:
        audio = AudioSegment.from_file(song)
        combined_audio += audio
    widget.config(text="All songs combined")
    segments = [
        combined_audio[i : i + segment_length]
        for i in range(0, len(combined_audio), segment_length)
    ]
    widget.config(text="Segments sliced up, now we be sortin\n")

    segment_volumes = []
    for segment in segments:
        samples = np.array(segment.get_array_of_samples())
        volume = librosa.feature.rms(y=samples.astype(float))[0]
        segment_volumes.append(volume.mean())

    sorted_segments = [
        x
        for _, x in sorted(
            zip(segment_volumes, segments), key=lambda pair: pair[0], reverse=True
        )
    ]
    widget.config(text="Segments sorted, now we be combining back into one. This is the part that may take a while.")

    sorted_audio = sum(sorted_segments[1:], sorted_segments[0])
    widget.config(text=f"We did it!\n")

    sorted_audio.export(
        f"output_songs/{output_filename}_sorted.{output_filetype}", format="wav"
    )
    widget.config(text=f"Segments combined. Congratulations on your newborn! {output_filename}.{output_filetype}\n"
                       f"You can drop more stuff here to be sorted if it pleases you.")


def start_audio_sorting_in_thread(filenames, slices_per_second, wav_or_mp3, output_filename, widget):
    def worker():
        combine_and_sort_audio(filenames, slices_per_second, wav_or_mp3.result, output_filename, widget)

    thread = threading.Thread(target=worker)
    thread.start()
