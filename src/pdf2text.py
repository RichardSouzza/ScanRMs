import camelot
import PyPDF2
import regex
from camelot.core import TableList

from utils import wrapper


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
