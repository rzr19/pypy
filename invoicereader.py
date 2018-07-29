import pdfquery
import os

#Reads invoice data based on bbox element positions. 
#Works for different PDF invoices from same vendors.
#Prerequisite is to get bbox coordinates with a pdf.tree.write from pdfquery

def startls():
    for file in os.listdir(r"C:\Users\vn_gh\Desktop\PDFs"):
        pdffiles = os.path.join(r"C:\Users\vn_gh\Desktop\PDFs", file)
        if file.startswith( 'Hettich' ):
            hettich(pdffiles)
        elif file.startswith ( 'Bachmann' ):
            bachmann(pdffiles)

def bachmann(files):
    pdf = pdfquery.PDFQuery(files)
    pdf.load()
    blah = pdf.extract( [
        ('with_formatter', 'text'),
        ('Customer: ','LTTextLineHorizontal:in_bbox("396.0, 628.478, 421.161, 637.127")'),
        ('Invoice: ','LTTextLineHorizontal:in_bbox("396.0, 676.478, 444.801, 685.127")'),
        (' Total Amount: ','LTTextLineHorizontal:in_bbox("523.08, 268.838, 550.761, 277.487")')
    ])
    print(blah)

def hettich(files):
    pdf = pdfquery.PDFQuery(files)
    pdf.load()
    blah = pdf.extract( [
        ('with_formatter', 'text'),
        ('Customer: ','LTTextLineHorizontal:in_bbox("493.2, 547.144, 524.336, 556.392")'),
        ('Invoice: ','LTTextLineHorizontal:in_bbox("493.2, 536.844, 537.68, 546.364")'),
    ])
    blah2 = pdf.pq('LTTextLineHorizontal:contains("Total amount ")').next() #or with nextAll and strip everything after.
    blah3 = blah2.next().text()
    blah4 = blah3.split("\n")[0].strip()
#    blah3 = blah2.split('\n', 1)[0].strip()
    blah.update({"Total Amount: ":blah4})
    print(blah)

if __name__ == "__main__":
    startls()
