import ImageDraw
import ImageFont
import random
import string
import qrcode
import zbar


class QRImage(object):
    """
    QRImage; Lightweight tool to create QR code with company's logo
    """

    def __init__(self):
        self.HEIGHT = 4
        self.WIDTH = 8
        self.BORDER = 4
        self.BOX_W = 8
        self.TEXT = "This is default text"
        self.IMAGE_SQUARE = 0
        self.BLOCK_SQUARE = 0
        self.error_count = 0

    def generate(self, height=None, width=None, text=None, label=None):

        """ initialize the height and width of the user text block """

        if not height:
            HEIGHT = self.HEIGHT
        else:
            HEIGHT = height

        if not width:
            WIDTH = self.WIDTH
        else:
            WIDTH = width

        # calculate the square of the user block in pixels
        self.BLOCK_SQUARE = WIDTH * HEIGHT

        BOX_W = self.BOX_W
        BORDER = self.BORDER

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=BOX_W,
            border=BORDER,
        )

        # check the passed text
        if not text:
            text = self.TEXT

        # add the text to qr code
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image()
        pil_img = img._img
        img_w, img_h = pil_img.size

        # calculate the square of the whole image in pixels
        self.IMAGE_SQUARE = (img_h - BORDER * BOX_W) * (img_w - BORDER * BOX_W)

        # PIL Draw initial.
        draw = ImageDraw.Draw(pil_img)

        # quantity of all cubes(8*8px) in one line
        cubes = img_w/BOX_W

        left = (cubes/2 - WIDTH/2) * BOX_W
        top = (cubes/2 - HEIGHT/2) * BOX_W
        right = (cubes/2 + WIDTH/2) * BOX_W
        bottom = (cubes/2 + HEIGHT/2) * BOX_W

        draw.rectangle([left, top, right, bottom], fill=255)
        draw.rectangle([left, top, right, bottom])

        if label:
            left_text = left + len(label)/2 * BOX_W  # text left offset
            top_text = top + HEIGHT/3 * BOX_W  # text top offset
            f = ImageFont.load_default()  # font settings
            draw.text((left_text, top_text), label, font=f)  # draw text

        pil_img.show()
        self.check_text(text)
        self.decode(pil_img)

    def decode(self,img):
        # create a reader
        scanner = zbar.ImageScanner()

        # configure the reader
        scanner.parse_config('enable')

        # obtain image data
        pil = img.convert('L')
        width, height = pil.size
        raw = pil.tostring()

        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)

        # scan the image for qrcodes
        scanner.scan(image)

        # extract results
        for symbol in image:
            # do something useful with results
            if symbol.type and symbol.data:
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            else:
                print "can't decode".capitalize()
                self.error_count += 1

    def check_text(self, text):
        length = len(text)
        print "length is",length
        ratio = float(self.BLOCK_SQUARE)/self.IMAGE_SQUARE*100


qr = QRImage()
qr.generate(height=15, width=15, text="t" * 36)

