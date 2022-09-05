import PyPDF2
import csv


def readPdf(filename):
    assetList = []
    with open(filename, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        for page in read_pdf.pages:
            page_content = page.extract_text()
            page_content_lines = page_content.split('\n')
            if validPage(page_content_lines):
                tableData = getTableData(page_content_lines)
                nameAndAddress = getNameAndAddress(page_content_lines)
                tableData.update(nameAndAddress)
                assetList.append(tableData)

    return assetList


def validPage(contentLines):
    if len(contentLines) <= 5:
        return False
    if not contentLines[2].startswith('Tenure'):
        return False
    if not contentLines[3].startswith('Year Built (Renovated)'):
        return False
    if not contentLines[4].startswith('Land Area'):
        return False

    return True


def getNameAndAddress(page_content_lines):
    data = {'region': '', 'address': '', 'name': ''}
    regions = ['UK', 'Ireland', 'Germany', 'Netherlands', 'Belgium', 'France', 'Spain', 'Italy', 'Poland']
    for i in range(len(page_content_lines)):
        for region in regions:
            if page_content_lines[i].endswith(', ' + region):
                data['region'] = region
                data['address'] = page_content_lines[i]
                data['name'] = page_content_lines[i - 1]
                break
    return data


def getTableData(page_content_lines):
    assetInfo = {
        'Tenure': '',
        'Year Built (Renovated)': '',
        'Land Area (Site Coverage)': '',
        'Rentable Area (% Office)': '',
        'Doors': '',
        'Clear Height': '',
        'Warehouse Floor Loading': '',
        'Truck Court Depth': '',
        'Parking Spaces': '',
        'Tenant(s)': '',
        'Occupancy': '',
        'Headline Rental Income': '',
        'Stabilised 2022 Income': '',
        'Lease Type': '',
        'Rent Review Provision': '',
        'WAULTB / WAULTE': '',
    }
    keysList = list(assetInfo.keys())
    for i in range(2, 18):
        if page_content_lines[i].startswith(keysList[i - 2]):
            assetInfo[keysList[i - 2]] = page_content_lines[i].replace(keysList[i - 2] + ' ', '')

    return assetInfo


def writeCsv(assetsList):
    with open('pdfCSV.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Region', 'Name', 'Address', 'Tenure', 'Year Built (Renovated)', 'Land Area (Site Coverage)',
                         'Rentable Area (% Office)', 'Doors', 'Clear Height', 'Warehouse Floor Loading',
                         'Truck Court Depth', 'Parking Spaces', 'Tenant(s)', 'Occupancy', 'Headline Rental Income',
                         'Stabilised 2022 Income', 'Lease Type', 'Rent Review Provision', 'WAULTB / WAULTE'])
        for asset in assetsList:
            writer.writerow(
                [asset['region'], asset['name'], asset['address'], asset['Tenure'], asset['Year Built (Renovated)'],
                 asset['Land Area (Site Coverage)'], asset['Rentable Area (% Office)'], asset['Doors'],
                 asset['Clear Height'],
                 asset['Warehouse Floor Loading'], asset['Truck Court Depth'], asset['Parking Spaces'],
                 asset['Tenant(s)'],
                 asset['Occupancy'], asset['Headline Rental Income'], asset['Stabilised 2022 Income'],
                 asset['Lease Type'],
                 asset['Rent Review Provision'], asset['WAULTB / WAULTE']])
