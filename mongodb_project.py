import pymongo
from bson.objectid import ObjectId

#mongodb + pymongo project for NoSQL databases

try:
    client = pymongo.MongoClient('192.168.99.100:32768')
    db = client.eabd
except pymongo.errors.ConnectionFailure:
    print("Could not connect to MongoDB")

db.users.drop()
db.ptypes.drop()
db.prod.drop()
db.ads.drop()
db.msg.drop()
db.tranz.drop()

list_users = [
        {"_id": "1", "nume": "Gheorghe", "prenume" : "Vlad", "telefon" : "0755488705", "email" : "gheorghexvlad@gmail.com"},
        {"_id": "2", "nume": "User", "prenume": "Userinho", "telefon": "0755488706", "email": "user@gmail.com" },
        {"_id": "3", "nume": "Hello", "prenume": "World", "telefon": "0755488707", "email": "hello@gmail.com" },
        {"_id": "4", "nume": "test", "prenume": "test2", "telefon": "0755488708", "email": "test@gmail.com"},
        {"_id": "5", "nume": "Boo", "prenume": "Boo", "telefon": "0755488709", "email": "boo@gmail.com"}
]
insert_users = db.users.insert_many(list_users)
list_ptypes = [
        { "_id":"auto", "tipuri": "Autoturisme"},
        { "_id":"electro", "tipuri" : "Electronice"},
        { "_id":"consum", "tipuri" : "Consumabile"},
        { "_id":"haine", "tipuri" : "Imbracaminte"},
        { "_id":"papuci", "tipuri" : "Incaltaminte"}
]
insert_ptypes = db.ptypes.insert_many(list_ptypes)
list_prod = [
        { "_id": "1", "numeProd" : "Adidasi 320 RON", "pozaProd" : "/var/www/htdocs/images/12345.jpg"},
        { "_id": "2", "numeProd" : "Iphone 6S  NOU NOUT", "pozaProd" : "/var/www/htdocs/images/123456.jpg'" },
        { "_id": "3", "numeProd" : "'Tricou ZARA MARIMEA L", "pozaProd" : "/var/www/htdocs/images/612345.jpg"},
        { "_id": "4", "numeProd" : "Dacia 1310 ca noua", "pozaProd" : "/var/www/htdocs/images/6123456.jpg'"},
        { "_id": "5", "numeProd" : "Manusi de portar, folosite", "pozaProd" : "/var/www/htdocs/images/312345.jpg"}
]
insert_prod = db.prod.insert_many(list_prod)
list_ads = [
        { "_id": "1", "idUser" : "1", "idTip" : "papuci", "idProd" : 1, "titlu" : "Incaltaminte de sala", "descriere" : "’Vand o pereche de adidasi. Se afla in starea ireprosabila, dupa cum se vede in poza atasata la anunt. Rog seriozitate.", "pret" : 320},
        { "_id": "2", "idUser" : "2", "idTip" : "electro", "idProd" : 1, "title" : "Telefon frumos", "descriere" : "Se vinde urgent", "pret" : 800 },
        { "_id": "3", "idUser" : "1", "idTip" : "haine", "idProd" : 3, "title" : "Tricou ZARA", "descriere" : "'Pretul este negociabil.", "pret" : 35},
        { "_id": "4", "idUser" : "3", "idTip" : "auto", "idProd" : 4, "title" : "automobil Dacia de vanzare" , "descriere" : "'Pretul este negociabil. Nu ma intereseaza schimburile.", "pret" : 10},
        { "_id": "5", "idUser" : "4", "idTip" : "haine", "idProd" : 5, "title" : "Echipament de fotbal", "descriere" : "'Nu au fost folosite decat o singura data. Se vede din poza ca sunt aproape noi. Pretul este fix!", "pret" : 109}
]
insert_ads = db.ads.insert_many(list_ads)
list_msg = [
        {"_id" : "1", "from_idUser" : "5", "to_idUser" : "5", "idAnunt" : "1" , "titluMsg" : "Sunt interesat de produs. La ce ora va pot suna pt detalii? Stima" ,"trimisLa" : "111111"},
        {"_id" : "2", "from_idUser" : "5", "to_idUser" : "1", "idAnunt" : "2" , "titluMsg" : "MA puteti suna la 0755488705 dupa ora 20. Stima" ,"trimisLa" : "222222"},
        {"_id" : "3", "from_idUser" : "5", "to_idUser" : "1", "idAnunt" : "3" , "titluMsg" : "Azi nu pot raspunde la telefon. Vorbim Luni." ,"trimisLa" : "333333"},
        {"_id" : "4", "from_idUser" : "1", "to_idUser" : "5", "idAnunt" : "4" , "titluMsg" : "Ok ne auzim pe luni. Numai bine" ,"trimisLa" : "444444"}
]
insert_msg = db.msg.insert_many(list_msg)
list_tranz = [
        {"_id" : "1", "from_idUser" : "1", "to_idUser" : "5", "sumaTranz" : "1"},
        {"_id" : "2", "from_idUser" : "1", "to_idUser" : "5", "sumaTranz" : "12"},
        {"_id" : "3", "from_idUser" : "1", "to_idUser" : "5", "sumaTranz" : "13"},
        {"_id" : "4", "from_idUser" : "1", "to_idUser" : "5", "sumaTranz" : "14"}
]
insert_tranz = db.tranz.insert_many(list_tranz)

#Stergere de #anunt care cauta si in celelealte documente referinta anuntul sters.
def deleteAnunt():
    try:
        deletedId = input("Introduceti anuntul care trebuie sters\n")
        for i in db.ads.find({"_id": deletedId}):
            for j in db.msg.find({"idAnunt": deletedId}):
                db.ads.delete_many({"_id": deletedId})
                db.msg.delete_many({"idAnunt": deletedId})
        print("Anuntul si referintele la el au fost sterse")
    except:
        print("Error at delete")

#Update nr de telefon din users
def updateTelefon():
    try:
        updateId = input("Introduceti numele userului la care trebuie schimbat numarul de telefon\n")
        updateValue = input("Introduceti numarul de telefon nou\n")
        db.users.update_one(
            {"_id": updateId},
            {"$set":
                 {"telefon": updateValue}
            }
        )
        print("Numarul de telefon s-a modificat cu succes.")
    except:
        print("Error at update")

#Inserare a doua noi documente in colectia ptypes cu o structura usor modificata
insert1 = db.ptypes.insert_one({"_id": "tipnou1", "tipuri": "Motociclete", "subtipAl": "Autoturisme"})
insert2 = db.ptypes.insert_one({"_id": "tipnou2", "tipuri": "Biciclete", "subtipAl": "Autoturisme"})

#Crearea a doi indecsi, unul simplu si unul compus
newSimpleIndex = db.ptypes.create_index([( 'tipuri', pymongo.ASCENDING)], background=True, unique=True)
newComplexIndex = db.users.create_index([("nume", pymongo.ASCENDING),("prenume", pymongo.DESCENDING)], background=True, unique=True)

#1. Returneaza numele primului utilizator
def numelePrimului():
    for i in db.users.find({'_id':'1'}):
        return i['nume'] + '', i['prenume']
#2. Returneaza anunturile scumpe (peste 500 lei)
def anunturileScumpe():
    for i in db.ads.find({'pret': { '$gt': 500 } } ):
        return i['title'] + '.', i['descriere'] + ' la pretul de', str(i['pret']) + '' + ' lei.'
#3.	Cate anuturi din categoria „Imbracaminte” sunt in baza de date
def numarImbracaminte():
    number = 0
    for i in db.ads.find({'idTip':'haine'}):
        number += 1
    return number
#4. Care este ultimul mesaj din db?
def ultimulMesaj():
    messages = db.msg.find({}, sort=[('_id', pymongo.DESCENDING)])
    elements = messages.next()
    return elements['titluMsg']
#5.

print("Optiunile pe care le ofera acest program sunt urmatoarele")
print("=========================================================")
print("1. Functie pentru Stergere a unui anunt din baza de date.")
print("2. Functie pentru Actualizare a unui numar de telefon. ")
print("3. Interogare pentru numele primului utilizator.")
print("4. Interogare pentru anunturi scumpe.")
print("5. Interogare pentru numarul articolelor de imbracaminte.")
print("6. Interogare pentru ultimul mesaj din baza de date.")
print("7. Oprire a programului din executie.")
print("=========================================================")
print("Va rugam sa selectati una din optiunile de mai sus (1-6).")

while True:
    optiune = int(input())
    if optiune == 1:
        deleteAnunt()
    elif optiune == 2:
        updateTelefon()
    elif optiune == 3:
        print(' '.join(numelePrimului()))
    elif optiune == 4:
        print(' '.join(anunturileScumpe()))
    elif optiune == 5:
        print(numarImbracaminte())
    elif optiune == 6:
        print(ultimulMesaj())
    elif optiune == 7:
        break