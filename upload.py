import dropbox
import sys
import os

# Uploads a pdf to dropbox and returns a shared link


def upload(pdf_filename, kursdato, TOKEN):
    dbx = dropbox.Dropbox(TOKEN)
    print(f"Forsoeker aa laste opp {pdf_filename}")
    to_path = os.path.join(
        '/Apps/EssentialsDiplomas/Diplomer/', kursdato, pdf_filename)

    try:
        with open(pdf_filename, 'rb') as f:
            dbx.files_upload(f.read(), to_path, autorename=True)
    except Exception as err:
        print("Opplastningen feilet %s\n%s" % (pdf_filename, err))

    shared_link_metadata = dbx.sharing_create_shared_link(
        to_path)
    print("Vellykket opplastning, se paa: " + shared_link_metadata.url)
    lenke = shared_link_metadata.url
    return lenke
