JPEG_MATCHING_1 = b"\xff\xd8\xff"
JPEG_MATCHING_2 = b'JFIF\0'
PNG_MATCHING = b'PNG'
BMP_MATCHING = b'BM'

def guess_image_mime_type(img_data: bytes) -> str:
    '''
    Function guesses an image mime type.
    Supported filetypes are JPG, BMP, PNG.
    '''
    if img_data[:3] == JPEG_MATCHING_1 or img_data[6:] == JPEG_MATCHING_2:
        return 'image/jpeg'
    elif img_data[1:4] == PNG_MATCHING:
        return 'image/png'
    elif img_data[:2] == BMP_MATCHING:
        return 'image/x-ms-bmp'
    else:
        return 'image/unknown-type'