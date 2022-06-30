from socket import SO_BINDTODEVICE
from typing import List

from sqlalchemy import func # Funções de agregação 

from conf.helpers import formata_data
from conf.db_session import create_session



# Select Simples
from models.aditivo_nutritivo import AditivoNutritivo
from models.sabor import Sabor
from models.revendedor import Revendedor

# Select Compostos / Complexos
from models.picole import Picole

## Select simples -> SELECT * FROM aditivos_nutritivos;
def select_todos_aditivos_nutritivos() -> None:
    with create_session() as session:
        # Forma 1
        # aditivos_nutritivos: List[AditivoNutritivo] = session.query(AditivoNutritivo)

        # Forma 2
        aditivos_nutritivos: List[AditivoNutritivo] = session.query(AditivoNutritivo).all()


        for an in aditivos_nutritivos:
            print(f'ID: {an.id}')
            print(f'Data: {formata_data(an.data_criacao)}')
            print(f'Nome: {an.nome}')
            print(f'Fórmula Química: {an.formula_quimica}')


# SELECT * FROM sabores WHERE sabor.id == 21;
def select_filtro_sabor(id_sabor: int) -> None:
    with create_session() as session:
        # Forma 1 # Retorna None caso não encontre
        # sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).first()

        # Forma 2 # Retorna None caso não encontre (Recomendado)
        # sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one_or_none()

        # Forma 3 # exec.NoResultFound caso não encontre
        # sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one()

        # Forma 4 # Usando where ao invés de filter (one(), one_or_none(), first())
        sabor: Sabor = session.query(Sabor).where(Sabor.id == id_sabor).one_or_none()

        print(f'ID: {sabor.id}')
        print(f'Data: {formata_data(sabor.data_criacao)}')
        print(f'Nome: {sabor.nome}')


def select_complexo_picole() -> None:
    with create_session() as session:
        picoles: List[Picole] = session.query(Picole).all()

        for picole in picoles:
            print(f'ID: {picole.id}')
            print(f'Data: {formata_data(picole.data_criacao)}')
            print(f'Preço: {picole.preco}')

            print(f'ID Sabor: {picole.id_sabor}')
            print(f'Sabor: {picole.sabor.nome}')

            print(f'ID Embalagem: {picole.id_tipo_embalagem}')
            print(f'Embalagem: {picole.tipo_embalagem.nome}')

            print(f'ID Tipo Picole: {picole.id_tipo_picole}')
            print(f'Tipo Picole: {picole.tipo_embalagem.nome}')

            print(f'Ingredientes: {picole.ingredientes}')
            print(f'Aditivos Nutritivos: {picole.aditivos_nutritivos}')
            print(f'Conservantes: {picole.conservantes}')


def select_order_by_sabor() -> None:
    with create_session() as session:
        sabores: List[Sabor] = session.query(Sabor).order_by(Sabor.data_criacao.desc()).all()

        for sabor in sabores:
            print(f'ID: {sabor.id}')
            print(f'Nome: {sabor.nome}')


def select_group_by_picole() -> None:
    with create_session() as session:
        picoles: List[Picole] = session.query(Picole).group_by(Picole.id, Picole.id_tipo_picole).all()

        for picole in picoles:
            print(f'ID: {picole.id}')
            print(f'Tipo Picole: {picole.tipo_picole.nome}')
            print(f'Sabor: {picole.sabor.nome}')
            print(f'Preço: {picole.preco}')


def select_limit() -> None:
    with create_session() as session:
        sabores: List[Sabor] = session.query(Sabor).limit(25)

        for sabor in sabores:
            print(f'ID: {sabor.id}')
            print(f'Sabor: {sabor.nome}')


def select_count_revendedor() -> None:
    with create_session() as session:
        qtd: int = session.query(Revendedor).count()

        print(f'Quantidade de revendedores: {qtd}')



def select_agregacao() -> None:
    with create_session() as session:
        resultado: List = session.query(
            func.sum(Picole.preco).label('soma'),
            func.avg(Picole.preco).label('media'),
            func.min(Picole.preco).label('mais_barato'),
            func.max(Picole.preco).label('mais_caro'),
        ).all()

        print(f'Resultado: {resultado}')

        print(f'A soma de todos os picolés é: {resultado[0][0]}')
        print(f'A média de todos os picolés é: {resultado[0][1]}')
        print(f'O picolé mais barato é: {resultado[0][2]}')
        print(f'O picolé mais caro é: {resultado[0][3]}')



if __name__ == '__main__':
    # select_todos_aditivos_nutritivos()
    # select_filtro_sabor(21)

    select_complexo_picole()

    # select_order_by_sabor()

    # select_group_by_picole()

    # select_limit()

    # select_count_revendedor()

    # select_agregacao()
