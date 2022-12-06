from pyupload import uploader
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageGrab
from pydub import AudioSegment
from pydub.playback import play
import pyperclip
from os import path, remove


IDLE, UPLOADING = (
    Image.open('./idle.png'),
    Image.open('./uploading.png')
)


def upload(icon: icon, _):
    global uploading
    if uploading:
        return

    img = ImageGrab.grabclipboard()

    if img is None:
        return
    
    if isinstance(img, list):
        img = Image.open(img[0])

    uploading = True
    icon.icon = UPLOADING

    if optimize:
        img.save(
            './temp_image.png',
            optimize=True,
            quality=80
        )
    else:
        img.save('./temp_image.png')

    inst = uploader.CatboxUploader('./temp_image.png')
    link = inst.execute()

    pyperclip.copy(link)

    remove('./temp_image.png')
    icon.icon = IDLE
    uploading = False
    play(AudioSegment.from_wav("./sound.wav"))


def optimize_clicked(icon: icon, _):
    global optimize
    optimize = not optimize
    with open('./optimized', 'w') as f:
        f.write('1' if optimize else '0')


def exit_(icon: icon, _):
    icon.stop()


uploading = False

if not path.isfile('./optimized'):
    with open('./optimized', 'w') as f:
        f.write('0')

with open('./optimized', 'r') as f:
    optimize = bool(int(f.read()))

icon('Clipboard to Catbox', icon=IDLE,
    menu=menu(
        item(
            'Upload',
            upload
        ),
        item(
            'Optimize img',
            optimize_clicked,
            checked=lambda _: optimize
        ),
        item(
            'Exit',
            exit_
        )
    )
).run()