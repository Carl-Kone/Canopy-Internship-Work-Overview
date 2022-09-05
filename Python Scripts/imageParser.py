import pdfParser as pdf
import fitz


def extractImages():
    assets = pdf.readPdf('sample.pdf')

    file = fitz.open('sample.pdf')
    assetCount = 1
    count = 298
    for i in range(len(file)):
        page = file[i]
        images = page.get_images()
        if len(images) != 6 or images[0][0] != 11:  # Not a valid page
            continue
        xrefList = []
        for j in range(len(images)):
            xrefList.append(images[j][0])

        xrefList = xrefList[2:4]

        print(xrefList)

        xrefFirstImage = images[0][0]
        j = 1
        for xref in xrefList:
            img = file.extract_image(xref)
            pix = fitz.Pixmap(file, xref)
            assetName = assets[assetCount - 1]['name']
            pix.save(f'00{count}_{assetName}_00{j}.png')
            j += 1

        j = 1
        assetCount += 1
        count += 1
