from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """

    return image_size[0] % tile_size[0] == 0 \
       and image_size[1] % tile_size[1] == 0 \
       and len(ordering) == len(set(ordering)) \
       and all(0 <= i < ((image_size[0]/tile_size[0]) * (image_size[1]/tile_size[1])) for i in ordering)


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    # open the image using pillow
    image = Image.open(image_path)

    # check if the input is valid
    if not valid_input(image.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    # split into tiles
    tiles = []
    for y in range(0, image.size[1], tile_size[1]):
        for x in range(0, image.size[0], tile_size[0]):
            tiles.append(image.crop((x, y, x + tile_size[0], y + tile_size[1])))

    # combine into final image
    im: Image = Image.new("RGB", image.size)
    width = 0
    height = 0
    for i in ordering:
        im.paste(tiles[i], (width, height))
        width += tile_size[0]
        if width >= image.size[0]:
            width = 0
            height += tile_size[1]

    # save the image
    im.save(out_path)

