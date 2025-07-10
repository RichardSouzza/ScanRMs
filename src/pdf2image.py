import os
from glob import glob

from spire.pdf import PdfDocument, PdfImageHelper


temp_dir = os.path.join(os.path.dirname(__file__), "..\\images")


def extract_image_from_pdf(pdf_path: str):
    print(f"Extracting image from {pdf_path}")

    doc = PdfDocument()
    doc.LoadFromFile(pdf_path)

    page = doc.Pages.get_Item(0)

    imageHelper = PdfImageHelper()
    imageInfo = imageHelper.GetImagesInfo(page)

    for i in range(0, len(imageInfo)):
        imageFileName = f"{temp_dir}/image.png".format(i)
        image = imageInfo[i].Image
        image.Save(imageFileName)

    doc.Dispose()


pdfs = glob(os.path.join("..\\pdfs", "*.pdf"))

for pdf in pdfs:
    extract_image_from_pdf(pdf)
