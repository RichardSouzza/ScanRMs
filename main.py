import os
import sys
from glob import glob

import camelot
import PyPDF2
import pyperclip as pc 
import regex
from camelot.core import TableList

from utils import suppress_output, wrapper


pdfs = glob(os.path.join("pdfs", "*.pdf"))


def get_requisition_number(pdf_title: str) -> str:
    with open(pdf_title, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[0]
        content = page.extract_text()
        
        pattern = regex.compile(r"\bRM:\s+\K\S+")
        rm = pattern.search(content)
        
        if rm: return rm.group()
        return "Não encontrada"


def get_tables_from_pdf(pdf_title: str) -> TableList:
    tables = camelot.read_pdf(pdf_title, pages=str("all")) # type: ignore
    return tables


def get_serial_numbers_from_table(tables: TableList) -> tuple[str]:
    serial_numbers = []

    for table in tables:
        dataframe = table.df
        for row in dataframe.iterrows():
            serial_numbers.append(row[1][1])

    try: serial_numbers.remove("NÚMERO DE SÉRIE")
    except ValueError: pass

    return tuple(serial_numbers)


def generate_sql(rm: str, serial_numbers: tuple[str]) -> str:
    select = f"select destino_estrutura_adm_fk  from semap.tb_requisicao_material trm where id = {rm};"

    update1 = (f"update semap.tb_tombamento set estrutura_adm_local_fk = {rm}\n"
               f"where numero_serie in {serial_numbers};")
    
    update2 = (f"UPDATE public.tb_dispositivo SET cd_estrutura_adm_fk = {rm}\n"
               f"WHERE nr_serie in {serial_numbers};")

    sql = f"{select}\n{update1}\n{update2}"
    sql = wrapper.wrap(sql)
    sql = "\n".join(sql).replace(";", ";\n\n\n")
    return sql


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