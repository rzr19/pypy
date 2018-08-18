import re
import csv



def lehmannMatGet(matRegexText):
    pageMatAttrsIndexed = re.findall('(\d{5,25})(?:[ \t]+)(\d{1,5} PCS \d{1,5})(?:[ \t]+)(\d{0,3}(?:\d{1,3}(.?\d{3})*(?:\,\d{1,2})))(?:[ \t]+)(\d{0,3}(?:\d{1,3}(.?\d{3})*(?:\,\d{1,2})))', matRegexText)
    pageMatAttrList = [ i[1] + ' ' + i[2] + ' ' + i[3] + ' ' + i[4] for i in pageMatAttrsIndexed ]
    pageMatIndexes = [ i[0] for i in pageMatAttrsIndexed ]
    pageMatIds = []
    n = 0
    for index in pageMatIndexes:
        if n + 1 < len(pageMatIndexes):
            thisIndexMaterialSearch = re.findall('{}([.\s\S]+){}'.format(pageMatIndexes[n], pageMatIndexes[n+1]), matRegexText)
            str2 = re.sub('\s+', ' ', str(thisIndexMaterialSearch).strip('[]').replace("'", ""))
            thisIndexMaterialSearch2 = str2.replace("\\n ", "\n")
            thisIndexMaterial = re.search('^(\d[-_a-zA-Z0-9]{4,25})$', thisIndexMaterialSearch2, flags=re.MULTILINE)
            if thisIndexMaterial: # if match re.search
                if pageMatIndexes[n] == pageMatIndexes[n + 1]:
                    matRegexText = matRegexText.split(str(thisIndexMaterial.group(0)))[1]
                pageMatIds.append(thisIndexMaterial.group(0))
            n += 1

        else:
            thisIndexMaterialSearch = re.findall('{}(.*[\s\S]+){}'.format(pageMatIndexes[n], 'carry over'), matRegexText)
            str2 = re.sub('\s+', ' ', str(thisIndexMaterialSearch).strip('[]').replace("'", ""))
            thisIndexMaterialSearch2 = str2.replace("\\n ", "\n")
            thisIndexMaterial = re.search('^(\d[-_a-zA-Z0-9]{4,25})$', thisIndexMaterialSearch2, flags=re.MULTILINE)
            if thisIndexMaterial: # if match re.search
                pageMatIds.append(thisIndexMaterial.group(0))
    thisPageMaterials = [id + ' ' + attr for id, attr in zip(pageMatIds, pageMatAttrList)]
    if len(pageMatIds) < len(pageMatAttrList): # some materials ids don't appear on same page as material attributes. Can't regex them from page 2 in this current logic.
                                               # marking them as missing for now.dd
        thisPageMaterials.append("missingMatId" + ' ' + pageMatAttrList[len(pageMatAttrList) - 1])
    pageMaterials = str(thisPageMaterials).strip('[]').replace("', '", ";").replace("'", "").replace("  ", " ")
    return pageMaterials

def lehmannGet(filename):
    with open(filename, 'r') as invoiceTxt:
        # For Lehmann we do line by line instead of one-big-string i.e. Hettich. The re.findall regex is 10 times faster nowo in MULTILINE mode
        fileContent = invoiceTxt.read().replace('\n\n', '\n')
        # Nr of invoice
        invoiceNrMatch = re.search('INVOICE NO\.: [0-9]{6}', fileContent)
        invoiceNrStr = invoiceNrMatch.group(0).strip("INVOICE NO\.: ")
        # Date of invoice
        invoiceDateMatch = re.search('(?:Date[ \t]+\: )((\d{2})[\.](\d{2})[\.](\d{4}))', fileContent)
        invoiceDateStr = invoiceDateMatch.group(1)
        poNoMatch = re.search('(?:Order[ \t]+\: )(4[0-9]{9})', fileContent)
        if poNoMatch:
            poNo = poNoMatch.group(1)
        else:
            poNo = ''
        # Pages to scan for Materials
        listedPagesMatch = re.findall('Page \d{1,4}\\n', fileContent)
        # First page is not "Paged". These go without iteration over listedPagesMatch.
        pageOneContent = fileContent.split('Page 2\n')[0]
        pageOneMaterialsStr = lehmannMatGet(pageOneContent)
        poMatList = []
        poMatList.append(pageOneMaterialsStr)
        i = 0
        for page in listedPagesMatch:
            if i + 1 < len(listedPagesMatch):
                thisPageString = re.findall('{}(.*[\s\S]+){}'.format(listedPagesMatch[i], listedPagesMatch[i+1]), fileContent, flags=re.MULTILINE)
                thisPageStringed = str(thisPageString).replace('\\n', '\n')
                thisPageMaterialStr = lehmannMatGet(thisPageStringed)
                poMatList.append(thisPageMaterialStr)
                i += 1
            else:
                lastPageString = re.findall('{}(.*[\s\S]+)'.format(listedPagesMatch[i]), fileContent, flags=re.MULTILINE)
                lastPageStringed = str(lastPageString).replace('\\n', '\n')
                lastPageMaterialStr = lehmannMatGet(lastPageStringed)
                # Total Amount & currency
                lastPageForTotal = lastPageStringed.split('Total value')[1]
                totalAmountMatch = re.search('(\d{0,3}(?:\d{1,3}(.?\d{3})*(?:\,\d{1,2})))$(?<!0,00)', lastPageForTotal, flags=re.MULTILINE)
                currencyStr = 'EUR'
                if totalAmountMatch:
                    totalAmountStr = totalAmountMatch.group(1)
                if lastPageMaterialStr:
                    poMatList.append(lastPageMaterialStr)

        totalMaterialsListed = ';'.join(poMatList)
        poStringed = poNo + ';' + totalMaterialsListed
        row = [invoiceNrStr, invoiceDateStr, totalAmountStr, currencyStr, poStringed]
        with open(r"C:\path\aMIRO.txt", "a+", newline='') as f:
             writer = csv.writer(f, delimiter=';')
             writer.writerow(row)