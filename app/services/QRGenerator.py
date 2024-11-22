import segno
import io

class QRGenerator:
	def __init__(self, link: str):
		self.link = link

	def generate(self):
		qr = segno.make(self.link)
		buff = io.BytesIO()
		qr.save(buff, kind="png", scale=10)
		buff.seek(0)
		return buff