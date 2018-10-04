import os
import subprocess
from hettich import hettichGet
from lehmann import lehmannGet
import re
import pyrfc

#original author vgheorgh
##to do
##1. add logger of activity to run.log file
##2. add class for RFC signal handling
##3. think of monitoring and alerting


def get_env(filename):
    filepath = os.getcwd() + "/" + filename
    cfglines = tuple(open(filepath, 'r'))
    for i, a in enumerate(cfglines):
        if 'server' in a:
            global server
            server = a[a.find('=') + 1:a.find(';')]
        elif 'pdfpath' in a:
            global pdfpath
            pdfpath = a[a.find('=') + 1:a.find(';')]
        elif 'ashost' in a:
            global ashost
            ashost = a[a.find('=') + 1:a.find(';')]
        elif 'sysnr' in a:
            global sysnr
            sysnr = a[a.find('=') + 1:a.find(';')]
        elif 'client' in a:
            global client
            client = a[a.find('=') + 1:a.find(';')]
        elif 'user' in a:
            global user
            user = a[a.find('=') + 1:a.find(';')]
        elif 'password' in a:
            global password
            password = a[a.find('=') + 1:a.find(';')]
        elif 'testRFCname' in a:
            global testRFCname
            testRFCname = a[a.find('=') + 1:a.find(';')]
        elif 'realRFCname' in a:
            global realRFCname
            realRFCname = a[a.find('=') + 1:a.find(';')]
        else:
            print('Unknown parameter in main.cfg')

class Invoice:
    ProcessedFilesCounter = 0
    def __init__(self, txtname):
        self.txtname = txtname
        self.fullname = pdfpath + txtname
        Invoice.ProcessedFilesCounter += 1

    @property
    def poNo(self):
        with open(self.fullname, 'r') as invoiceTxt:
            fileContent = invoiceTxt.read()
            if re.match("Hettich Marketing- u\. Vertriebs GmbH & Co\.KG Â·", fileContent):
                return hettichGet(self.fullname)
            elif re.match("LEHMANN Vertriebsgesellschaft mbH & Co\. KG â€¢", fileContent):
                return lehmannGet(self.fullname)
            else:
                return None

class callRFC:
    def __init__(self, ashost, sysnr, client, user, password):
        self.ashost = ashost
        self.sysnr = sysnr
        self.client = client
        self.user = user
        self.password = password

    def helloRFC(self):
        try:
            rfcConn = pyrfc.Connection(ashost=self.ashost, sysnr=self.sysnr, client=self.client, user=self.user, passwd=self.password)
            result = rfcConn.call(testRFCname, REQUTEXT='test')
            return result
        except pyrfc.RFCError as rfcerror:
            return rfcerror

    def realRFC(self, poString):
        try:
            rfcConn = pyrfc.Connection(ashost=self.ashost, sysnr=self.sysnr, client=self.client, user=self.user, passwd=self.password)
            result = rfcConn.call(realRFCname, IV_IMPORT=poString)
            return result
        except pyrfc.RFCError as rfcerror:
            return rfcerror

if __name__ == "__main__":

    get_env('main.cfg')
########################################################################################################################
########################### NOT USED IN PRODUCTION ONLY ON LOCAL WINDOWS MACHINE #######################################

    if server == 'local':
        def dockertxt():
            try:
                subprocess.check_output("docker run -v" + " " + pdfpath + ":\data" + " " + "mypdftotxt", shell=True)
            except subprocess.CalledProcessError as error:
                return error
        dockertxt()

########################### NOT USED IN PRODUCTION ONLY ON LOCAL WINDOWS MACHINE #######################################
########################################################################################################################

    elif server == 'server':
        def simpletxt():
            try:
                subprocess.check_output("/bin/bash /projects/git/pdfmoney/run_pdftotext.sh", shell=True)
            except subprocess.CalledProcessError as error:
                return error
        simpletxt()
    else:
        print('Edit the main.cfg to either run local or on server. There\'s no other way.')

    testconn = callRFC(ashost, sysnr, client, user, password).helloRFC()
    if type(testconn) is not dict:
        print('ERP is unreachable. Proceed to exit hard.')
        exit(99) #exit hard

    for file in os.listdir(pdfpath):
        if file.endswith(".txt"):
            txtFile = Invoice(file)
            if txtFile.poNo:
                poStringed = str(txtFile.poNo)
                realconn = callRFC(ashost, sysnr, client, user, password).realRFC(poStringed)
                print(realconn)
            os.remove(txtFile.fullname)
