import os
from hettich import hettichGet
from lehmann import lehmannGet
import warnings
import datetime
import re
import csv

def startls():
    filesProcessed = 0
    for file in os.listdir(r"C:\Users\VGHEORGH\Desktop\PDFs"):
        txtfile = os.path.join(r"C:\Users\VGHEORGH\Desktop\PDFs", file)
        if file.startswith( 'RE_' ) and file.endswith( 'txt' ):
            lehmannResults = lehmannGet(txtfile)
            filesProcessed += 1
        elif file.endswith( 'txt' ):
            hettichResults = hettichGet(txtfile)
            filesProcessed += 1
    print("Total files processed: ", filesProcessed)

def startcp():
    invoiceFile = r"C:\Users\VGHEORGH\Desktop\PDFs\MIRO.txt"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host="", username="", password="", cnopts=cnopts) as sftpSAP:
        sftpSAP.chdir('/tmp')
        sftpSAP.put(invoiceFile)
        sftpSAP.chmod('/tmp/MIRO.txt', 666)
        
def hettichMatGet(regexText):
    materialMatches = re.findall('((1_[a-zA-Z0-9-_]+.) (CE|TW) \d+(?:\.?\d+)? (SET|PCE) \d{1,3}(.?\d{3})*(\,\d{1,2})? \d{1,6} \d{1,3}(.?\d{3})*(\,\d{1,2})?)', regexText)
    materialNumbers = [i[0] for i in materialMatches]
    materialStr = str(materialNumbers).split(', ')
    materialStringed = ';'.join(materialStr).strip('[]').replace("'", "")
    return materialStringed

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
            poStringed = poNo + ";" + materialStringed.replace("'", "")
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
            poStringed = ';'.join(poComplete).strip('[]').replace("'", "")

        row = [invoiceNrStr, invoiceDateStr, totalAmountStr, currencySymbol, poStringed]
        with open(r"C:\Users\me\Desktop\PDFs\aMIRO.txt", "a+", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(row)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print('Started at: ', datetime.datetime.now().strftime('%H:%M:%S'))
    startls()
    print('Ended at: ', datetime.datetime.now().strftime('%H:%M:%S'))
#    startcp()
