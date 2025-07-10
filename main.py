import os
import sys
from glob import glob

import pyperclip as pc 
from camelot.core import TableList

from src.pdf2text import *
from src.utils import suppress_output, wrapper


pdfs = glob(os.path.join("pdfs", "*.pdf"))


def menu() -> str:
    print("Selecione o arquivo PDF que deseja ler:\n")
    for count, pdf in enumerate(pdfs):
        print(f"{count + 1} - {pdf[5:]}")
    
    print("\nDigite o número do arquivo PDF que deseja ler (ou 'sair' para sair):")

    while True:
        choice = input("Escolha: ").strip()
        
        if choice.lower() == "sair":
            print("Saindo...")
            sys.exit(0)
        
        elif choice.isdigit() and 0 <= int(choice) - 1 < len(pdfs):
            pdf = pdfs[int(choice) - 1]
            return pdf
        
        else: print("Opção inválida.")


if __name__ == "__main__":
    pdf = menu()
    print(f"\nLendo o arquivo \"{pdf[5:]}\".")

    rm = get_requisition_number(pdf)
    print(f"RM: {rm}")

    with suppress_output():
        tables = get_tables_from_pdf(pdf)

    serial_numbers = get_serial_numbers_from_table(tables)

    sql = generate_sql(rm, serial_numbers)
    
    pc.copy(sql)
    print("\nSQL copiado para a área de transferência.")