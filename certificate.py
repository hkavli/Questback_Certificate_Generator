import csv
import os
import shutil
import datetime
import pickle

from dotenv import load_dotenv

from generate_certificate import generate_certificate
from send_email import send_email
from generate_diploma import generate_diploma
from send_email_diploma import send_email_diploma
from upload import upload


load_dotenv()

# Required enviroment variables and data files
TOKEN = os.environ.get('API_KEY')
data_file = "participants/kursdeltakere.csv"
certificateID_file = "participants/certificationIDs.p"
antallKursdeltakere = 0


def get_total_certifications():
    if not os.path.exists(certificateID_file):
        certificationIDs = {"certificationID": 100}
        pickle.dump(certificationIDs, open(
            certificateID_file, "wb"))
    f = pickle.load(open(certificateID_file, "rb"))
    attestID = f.get("certificationID")
    return attestID


def get_total_course_particiants(antallKursdeltakere):
    if antallKursdeltakere == 0:
        antallKursdeltakere = 1
    return antallKursdeltakere


# Useful counter variables
attestID = get_total_certifications()
antallKursdeltakers = get_total_course_particiants(antallKursdeltakere)


def update_total_certifications(attestID):
    attestID += antallKursdeltakere
    certificationIDs = {"certificationID": attestID}
    pickle.dump(certificationIDs, open(certificateID_file, "wb"))
    return attestID


def start():
    print("*************************************************")
    print("*********     Starting certificate()    *********")
    print("*************************************************")


def close(antallKursdeltakere, attestID):
    update_total_certifications(attestID)
    clean_folder()
    print(
        f"\nAntall sertifiseringsbevis generert i dag: {get_total_course_particiants(antallKursdeltakere)}")
    print(
        f"\nAntall serifiseringsbevis gjennom tidene: {get_total_certifications()}")


def import_data(data_file, attestID, antallKursdeltakere):
    with open(data_file, "r", encoding='utf-8') as f:
        csvreader = csv.reader(f, delimiter=",")
        for row in csvreader:
            antallKursdeltakere += 1
            navn = row[0]
            firmanavn = row[1]
            email = row[2]
            kursdato = row[3]
            kursnavn = row[4]
            kurssted = row[5]
            kursdato2 = row[6]
            kursnavn2 = row[7]

            stringAttestID = str(attestID)
            pdf_filename = navn.replace(" ", "")+'_' + stringAttestID + '.pdf'

            # ensures filename compability
            navnASCII = navn.encode("ascii", errors="ignore").decode()
            pdf_filename = pdf_filename.encode(
                "ascii", errors="ignore").decode()

            # Diplomas for those that have attended one course
            if len(kursdato2) <= 4 and len(kursnavn2) <= 4:
                attestID = generate_diploma(attestID, navn, firmanavn, kursnavn,
                                            kursdato, kurssted, pdf_filename, navnASCII)
                lenke = upload(pdf_filename, kursdato, TOKEN)
                send_email_diploma(navn, firmanavn, kursnavn, email, kursdato, kurssted,
                                   kursnavn2, kursdato2, pdf_filename, lenke, attestID, navnASCII)
            else:
                # Certifications for those that have attended two courses
                attestID = generate_certificate(
                    attestID, navn, firmanavn, kursnavn, kursdato, kurssted, kursnavn2, kursdato2, pdf_filename, navnASCII)
                lenke = upload(pdf_filename, kursdato, TOKEN)
                send_email(navn, firmanavn, kursnavn, email, kursdato, kurssted,
                           kursnavn2, kursdato2, pdf_filename, lenke, attestID, navnASCII)
    return antallKursdeltakere


def clean_folder():
    # by moving all certificates to the archive
    destination_dir = "archive/"
    source = os.getcwd()

    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    for f in os.listdir(source):
        base, extension = os.path.splitext(f)
        if f.endswith(".pdf"):
            destination_file = os.path.join(destination_dir, f)
            i = 1  # increments duplicate file for distinct naming
            while os.path.exists(destination_file):
                new_name = os.path.join(
                    destination_dir, base + "(" + str(i) + ")" + extension)
                if not os.path.exists(new_name):
                    shutil.move(f, new_name)
                    break
                i += 1
            else:
                shutil.move(f, destination_dir)


def certificate():
    start()
    import_data(data_file, attestID, antallKursdeltakere)
    close(antallKursdeltakere, attestID)
