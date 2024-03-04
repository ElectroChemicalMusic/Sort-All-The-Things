# WE MUST SORT

The project requires python, and the dependencies are managed by pipenv. If you don't use that then the relevant
installations are:

```bash
pip install tkinter
pip install pillow
pip install librosa
pip install tkinterdnd2
pip install numpy
```

## How do I sort?
If you run the main.py file it presents a drag and drop window that accepts audio files, images, or directories 
containing either. All files are exported to their respective output folder within the project,

If a folder contains many audio files, it will sum them in to one audio stream before sorting and export a single file. 
Images are done individually, so a folder containing many input images will produce an equal number of output images.