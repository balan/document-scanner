"""
Application to scan document from photo and save in pdf format.
Optionally you may search target word in text and draw bounding box for it.
"""

import os
from time import time
from argparse import ArgumentParser
from detectors import detect_document


APP_NAME = "document-scanner"
OUTPUT_FOLDER = "./out"
DEFAULT_PDF_NAME = "document.pdf"
DEFAULT_IMG_PATH = "./images/sample_0.jpg"


def callback(arguments):
    """Callback function to process CLI commands"""
    start = time()
    output_path = os.path.join(OUTPUT_FOLDER, arguments.pdf)
    try:
        warped, binarized = detect_document(arguments.image, output_path, arguments.binarize, white=True)
        print("Document is found! Check your pdf file.")
        if arguments.target_words is not None:
            # import only if words are requested
            from detectors import draw_word_boxes
            draw_word_boxes(binarized, arguments.target_words, arguments.lang, output_path)
            print("Target words are found! Check your pdf file.")
    except Exception as e:
        print(e)
    print(f"Running time: {time() - start:.3f} seconds.")


def setup_parser(parser):
    """Parse commands from CLI"""

    parser.add_argument(
        "-i", "--image",
        default=DEFAULT_IMG_PATH,
        help="path to input image",
    )
    parser.add_argument(
        "-p", "--pdf",
        default=DEFAULT_PDF_NAME,
        help="path to store document in pdf format",
    )
    parser.add_argument(
        "--binarize", action="store_false",
        help="save two document versions: original and binarized (stores both by default, only original when false)",
    )
    parser.add_argument(
        "-w", "--words", nargs="*",
        dest="target_words",
        help="list of target words to search in document (no words by default)",
    )
    parser.add_argument(
        "-l", "--lang",
        default="eng",
        help="specify language of text if needed (english by default)",
    )
    parser.set_defaults(callback=callback)


def main():
    parser = ArgumentParser(
        prog=APP_NAME,
        description="scanner for documents: plug photo of your document and get scan in pdf format",
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
