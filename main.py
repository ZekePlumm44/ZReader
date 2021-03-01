import PyPDF2  # Allows for the manipulating pdfs
import pyttsx3
import csv
import pathlib
import sys
import os


class Book:
    def __init__(self, path, author, creator, producer, subject, title, num_of_pages):
        self.path = path
        self.author = author
        self.creator = creator
        self.producer = producer
        self.subject = subject
        self.title = title
        self.num_of_pages = num_of_pages


def extract_info(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    txt = f"""
    Information about {pdf_path}:

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of Pages: {number_of_pages}
    """
    print(txt)
    b = Book(pdf_path, information.author, information.creator, information.producer, information.subject,
             information.title, number_of_pages)
    return b


def print_to_csv(pdf_path):
    data = extract_info(pdf_path)
    if os.path.isfile(pdf_path):
        data = [["Path", "Author", "Creator", "Producer", "Subject", "Title", "Number of Pages"],
                [pdf_path, data.author, data.creator, data.producer, data.subject, data.title, data.num_of_pages]]
    else:
        data = [pdf_path, data.author, data.creator, data.producer, data.subject, data.title, data.num_of_pages]
    library = open('library.csv', 'w')
    with library:
        writer = csv.writer(library)
        writer.writerows(data)
    print("Writing Complete")


def read_from_csv():
    try:
        csv_file = open('library.csv')
    except IOError:
        print("library.csv not created. Must have library to browse library")
        return 0
    reader = csv.DictReader(csv_file)
    library_info = list(reader)
    return library_info


def get_new_path():
    while True:
        f = input("Please enter PDF file path: (Hint use: jackson_lottery.pdf as it works)")
        try:
            PyPDF2.PdfFileReader(open(f, 'rb'))
        except PyPDF2.utils.PdfReadError:
            print("Invalid PDF file")
        else:
            break
    return f


if __name__ == "__main__":
    __location__ = pathlib.Path(__file__).parent.absolute()
    print("Welcome to Zeke's Reader!")
    if input("Enter new book(1) or browse from library(0):"):
        path = get_new_path()
        enter_book = input("Would you like to enter book to library(y/n)?")
        if enter_book == 'y':
            print_to_csv(path)
    else:
        lib_info = read_from_csv()
        if lib_info == 0:
            sys.exit()
        else:
            lib_dictionary = {i: lib_info[i] for i in range(0, len(lib_info))}
            print(lib_dictionary)
            book = input("Select book number: ")
            path = lib_dictionary.get(book)[0]
    file = open(path, "rb")
    pdf_reader = PyPDF2.PdfFileReader(file)
    speaker = pyttsx3.init()
    #Change rate volume to change speed
    speaker.setProperty('rate', 125)
    for page_num in range(pdf_reader.numPages):
        text = pdf_reader.getPage(page_num).extractText()
        speaker.say(text)
        speaker.runAndWait()
    speaker.save_to_file(text, 'audio.mp3')
    speaker.runAndWait()
