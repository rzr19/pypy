import re
import csv



def hettichSetMatGet(iterator, matSetPair):
    matSetCorrect = [n[1] for n in matSetPair]
    matSetStr = str(matSetCorrect).strip('[]').replace("'", "").replace(",", "").split("right ", 1)[1]
    firstSpaceInOriginalMatIndex = iterator.find(' ')
    newMaterialWithSet = iterator[:firstSpaceInOriginalMatIndex] + ' ' + matSetStr + iterator[firstSpaceInOriginalMatIndex:]
    return newMaterialWithSet

def hettichMatGet(matRegexText):
    materialMatches = re.findall('((1_[a-zA-Z0-9-_]+.) (CE|TW) \d+(?:\.?\d+)? (SET|PCE) \d{1,3}(.?\d{3})*(\,\d{1,2})? \d{1,6} \d{1,3}(.?\d{3})*(\,\d{1,2})?)', matRegexText)
    materialNumbers = [i[0] for i in materialMatches]
    materialStr = str(materialNumbers).split(', ')
    materialStringed = ';'.join(materialStr).strip('[]').replace("'", "")
    materialSetIterators = materialStringed.split(';')
    i = 0
    for id, iterator in enumerate(materialSetIterators):
        if " SET " in iterator:
            if i + 1 == len(materialSetIterators):
                matSetPair = re.findall('{}(.*)(left ((1_[a-zA-Z0-9-_]+.) and right (1_[a-zA-Z0-9-_]+.)),)(.*)'.format(materialSetIterators[i]), matRegexText)
                materialSetIterators[id] = hettichSetMatGet(iterator, matSetPair)
            else:
                matSetPair = re.findall('{}(.*)(left ((1_[a-zA-Z0-9-_]+.) and right (1_[a-zA-Z0-9-_]+.)),)(.*){}'.format(materialSetIterators[i], materialSetIterators[i+1]), matRegexText)
                materialSetIterators[id] = hettichSetMatGet(iterator, matSetPair)
                i += 1
        else:
            i += 1
    materialStringedWithSets = ';'.join(materialSetIterators).strip('[]').replace("'", "")
    # must remove CE/TW from return
    return materialStringedWithSets

def hettichGet(filename):
    with open(filename, 'r') as invoiceTxt:
        fileContent = invoiceTxt.read().replace('\n', ' ')
        # All the POs
        poNoMatches = re.findall('(?:Your Order:|Votre commande :) 4[0-9]{9}', fileContent)
        poNoStr = str(poNoMatches[0])
        poNo = poNoStr.strip("Your Order: ").strip("Votre commande : ")
        # Nr of invoice
        invoiceNrMatch = re.search('(Invoice:|Facture:) 9[0-9]{9}', fileContent)
        invoiceNrStr = invoiceNrMatch.group(0).strip("Invoice: ").strip("Facture: ")
        # Date of invoice
        invoiceDateMatch = re.search('Date: (\d{2})[\.](\d{2})[\.](\d{4})', fileContent)
        invoiceDateStr = invoiceDateMatch.group(0).strip("Date: ")
        # Total amount
        totalAmountMatch = re.search('(Total amount|Montant total)  \d{1,3}(.?\d{3})*(\,\d{1,2})?', fileContent)
        totalAmountStr = totalAmountMatch.group(0).strip("Total amount  ").strip("Montant total  ")
        # Currency
        currencyMatch = re.search('(Price Per Goods-Value MA:Item Description|Prix Par Prix total Nr. d\'article Description) [a-zA-Z]{3}', fileContent)
        currencyStr = currencyMatch.group(0)
        currencySymbol = currencyStr[-3:]
        if len(poNoMatches) == 1:
            materialStringed = hettichMatGet(fileContent)
            poStringed = poNo + ";" + materialStringed
        elif len(poNoMatches) > 1:
            i = 0
            poComplete = []
            for po in poNoMatches:
                if i + 1 == len(poNoMatches):
                    poMatList = re.findall('{}(.*)'.format(poNoMatches[i]), fileContent)
                    poMatText = str(poMatList)
                    materialStringed = hettichMatGet(poMatText)
                    thisPO = po.strip("Your Order: ").strip("Votre commande : ") + ";" + materialStringed
                    poComplete.append(thisPO)
                else:
                    poMatList = re.findall('{}(.*){}'.format(poNoMatches[i], poNoMatches[i+1]), fileContent)
                    poMatText = str(poMatList)
                    materialStringed = hettichMatGet(poMatText)
                    thisPO = po.strip("Your Order: ").strip("Votre commande : ") + ";" + materialStringed
                    poComplete.append(thisPO)
                    i += 1
            poStringed = ';'.join(poComplete).strip('[]').replace("'", "").replace(" CE ", "")

        row = [invoiceNrStr, invoiceDateStr, totalAmountStr, currencySymbol, poStringed]
        with open(r"C:\path\aMIRO.txt", "a+", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(row)