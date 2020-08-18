import argparse
import tempfile
import shutil
import os
import zipfile
import pyunpack
import img2pdf
import pathlib


def parse_arguments():
    parser = argparse.ArgumentParser(description="Converts comic book format to pdf format", prog="comic2pdf")
    parser.add_argument("input", nargs="+", help="specify the input file(s)")
    parser.add_argument("-o", "--output", help="specifiy the output directory", type=str, action="store", dest="output")
    parser.add_argument("--version", action="version", version="comic2pdf 1.0")
    return parser.parse_args()


def unpack_zip(archive, output):
    with zipfile.ZipFile(archive, "r") as zip_file:
        for zip_info in zip_file.infolist():
            if zip_info.filename[-1] == "/":
                continue
            zip_info.filename = os.path.basename(zip_info.filename)
            zip_file.extract(zip_info, output)


def unpack_rar(archive, output):
    rar = pyunpack.Archive(archive)
    rar.extractall(directory=output)


def process_comic_file(input_file, output_file):
    with tempfile.TemporaryDirectory() as tempdir:
        temp_comic_path = shutil.copy(input_file, tempdir)
        file_extension = os.path.splitext(temp_comic_path)[1]

        if file_extension.lower() == ".cbz":
            unpack_zip(temp_comic_path, tempdir)
        elif file_extension.lower() == ".cbr":
            temp_rar_path = shutil.copy(temp_comic_path, os.path.join(tempdir, os.path.splitext(
                os.path.basename(temp_comic_path))[0] + ".rar"))
            unpack_rar(temp_rar_path, tempdir)
        else:
            print("File extension not supported")
            exit(1)

        image_files = []
        for file in os.listdir(tempdir):
            if os.path.isfile(os.path.join(tempdir, file)) and file.lower().endswith((".jpg", ".jpeg")):
                image_files.append(os.path.join(tempdir, file))

        pdf_name = os.path.splitext(os.path.basename(input_file))[0] + ".pdf"

        if output_file is not None:
            pathlib.Path(os.path.abspath(output_file)).mkdir(parents=True, exist_ok=True)
            output_directory = os.path.abspath(
                output_file if os.path.isdir(output_file) else input_file)

        pdf_file = os.path.join(tempdir, pdf_name)
        with open(pdf_file, "wb") as pdf:
            pdf.write(img2pdf.convert(image_files))

        shutil.copy(pdf_file, output_directory)


if __name__ == "__main__":
    args = parse_arguments()

    for input_file in args.input:
        if not os.path.exists(input_file):
            print("File " + str(input_file) + "not found")
            exit(1)

    for input_file in args.input:
        process_comic_file(input_file, args.output)
