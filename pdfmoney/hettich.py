import re
import csv



def hettichSetMatGet(iterator, matSetPair):
    matSetCorrect = [n[1] for n in matSetPair]
    matSetStr = str(matSetCorrect).strip('[]').replace("'", "").replace(",", "")
    firstSpaceInOriginalMatIndex = iterator.find(' ')
    newMaterialWithSet = iterator[:firstSpaceInOriginalMatIndex] + ' ' + matSetStr + iterator[firstSpaceInOriginalMatIndex:]
    return newMaterialWithSet

def hettichMatGet(matRegexText):
    materialMatches = re.findall('(1_?[a-zA-Z0-9-_]+.)(?:[ \t]+)(\*\*|CE|TW)(?:[ \t]+)(\d+(?:\.?\d+)?)(?:[ \t]+)(SET|PCE)(?:[ \t]+)(\d{0,3}(?:\d{1,3}(?:.?\d{3})*(?:\,\d{1,2})))?(?:[ \t]+)(\d{1,6})(?:[ \t]+)(\d{0,3}(?:\d{1,3}(?:.?\d{3})*(?:\,\d{1,2})))?', matRegexText)
    materialNumbers = [i[0] + ' ' + i[1] + ' ' + i[2] + ' ' + i[3] + ' ' + i[4] + ' ' + i[5] + ' ' + i[6] for i in materialMatches]
    materialStr = str(materialNumbers).split(', ')
    materialStringed = ';'.join(materialStr).strip('[]').replace("'", "")
    materialSetIterators = materialStringed.split(';')
    newMaterialSetIterators = [ mat.split()[0] for mat in materialSetIterators ] #get the page splits for sets
    i = 0
    for id, iterator in enumerate(materialSetIterators):
        if " SET " in iterator:
            if i + 1 == len(materialSetIterators):
                matSetPair = re.findall('{}(?:[.*\s\S]+)left (1_[a-zA-Z0-9-_]+.) and(?:[.*\s\S]+)right (1_[a-zA-Z0-9-_]+.)'.format(newMaterialSetIterators[i]), matRegexText)
                materialSetIterators[id] = hettichSetMatGet(iterator, matSetPair)
            else:
                matSetPair = re.findall('{}(?:[.*\s\S]+)left (1_[a-zA-Z0-9-_]+.) and(?:[.*\s\S]+)right (1_[a-zA-Z0-9-_]+.)(?:[.*\s\S]+){}'.format(newMaterialSetIterators[i], newMaterialSetIterators[i+1]), matRegexText)
                materialSetIterators[id] = hettichSetMatGet(iterator, matSetPair)
                i += 1
        else:
            i += 1
    materialStringedWithSets = ';'.join(materialSetIterators).strip('[]').replace("'", "")
    # must remove CE/TW from return
    return materialStringedWithSets

def hettichGet(filename):
    with open(filename, 'r') as invoiceTxt:
        fileContent = invoiceTxt.read().replace('\n\n', '\n')
        # All the POs
        poNoMatches = re.findall('(?:Your Order:|Votre commande :) 4[0-9]{9}', fileContent)
        poNoStr = str(poNoMatches[0])
        poNo = poNoStr.strip("Your Order: ").strip("Votre commande : ")
        # Nr of invoice
        invoiceNrMatch = re.search('(Invoice:|Facture:)(?:[ \t]+)9[0-9]{9}', fileContent)
        invoiceNrStr = invoiceNrMatch.group(0).strip("Invoice: ").strip("Facture: ")
        # Date of invoice
        invoiceDateMatch = re.search('(?:Date\:[ \t]+)((?:\d{2})[\.](?:\d{2})[\.](?:\d{4}))', fileContent)
        invoiceDateStr = invoiceDateMatch.group(0).strip("Date: ")
        # Total amount
        totalAmountMatch = re.search('(?:Total amount|Montant total)[ \t]+(\d{0,3}(?:\d{1,3}(?:.?\d{3})*(?:\,\d{1,2})))?', fileContent)
        totalAmountStr = totalAmountMatch.group(0).strip("Total amount  ").strip("Montant total  ")
        # Currency
        currencyMatch = re.search('(?:MA:Item(?:[ \t]+?)Description|Nr\. d\'article(?:[ \t]+?)Description)(?:[ \t]+?)([a-zA-Z]{3})', fileContent)
        currencyStr = currencyMatch.group(0)
        currencySymbol = currencyStr[-3:]
        if len(poNoMatches) == 1:
            materialStringed = hettichMatGet(fileContent)
            poStringed = poNo + ";" + materialStringed.replace(" CE ", " ").replace(" TW ", " ").replace("  ", " ")

        elif len(poNoMatches) > 1:
            i = 0
            poComplete = []
            for po in poNoMatches:
                if i + 1 == len(poNoMatches):
                    poMatList = re.findall('{}(.*[\s\S]+)'.format(poNoMatches[i]), fileContent)
                    poMatText = str(poMatList).replace('\\n', '\n')
                    materialStringed = hettichMatGet(poMatText)
                    thisPO = po.strip("Your Order: ").strip("Votre commande : ") + ";" + materialStringed
                    poComplete.append(thisPO)
                else:
                    poMatList = re.findall('{}(.*[\s\S]+){}'.format(poNoMatches[i], poNoMatches[i+1]), fileContent)
                    poMatText = str(poMatList).replace('\\n', '\n')
                    materialStringed = hettichMatGet(poMatText)
                    thisPO = po.strip("Your Order: ").strip("Votre commande : ") + ";" + materialStringed
                    poComplete.append(thisPO)
                    i += 1
            poStringed = ';'.join(poComplete).strip('[]').replace("'", "").replace(" CE ", " ").replace('  ', ' ').replace(" TW ", " ")

#        SAProw = [invoiceNrStr, invoiceDateStr, totalAmountStr, currencySymbol, poStringed]
        SAProw = invoiceNrStr + ';' + invoiceDateStr + ';' + totalAmountStr + ';' + currencySymbol + ';"' + poStringed + '"'
        invoiceTxt.close()
        return(SAProw)
        # with open(r"C:\Users\VGHEORGH\Desktop\PDFs\MIRO.txt", "a+", newline='') as f:
        #     writer = csv.writer(f, delimiter=';')
        #     writer.writerow(row)
