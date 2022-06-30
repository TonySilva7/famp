"""
1 - Buscar o registro a ser atualizado;
2 - Faz as alterações no registro;
3 - Salva o registro no banco de dados;
"""
import asyncio
from sqlalchemy.future import select

from conf.db_session import create_session

from models.sabor import Sabor
from models.picole import Picole


async def select_filtro_picole(id_picole: int) -> None:
    async with create_session() as session:
        query = select(Picole).where(Picole.id == id_picole)
        picole: Picole = await session.execute(query)
        picole = picole.unique().scalar_one_or_none()

        if picole:
            print(f'ID: {picole.id}')
            print(f'Preço: {picole.preco}')
            print(f'Sabor: {picole.sabor.nome}')
        else:
            print('Não existe o picole com o id informado')



async def atualizar_sabor(id_sabor: int, novo_nome: str) -> None:
    async with create_session() as session:
        # Passo 1
        query = select(Sabor).filter(Sabor.id == id_sabor)
        sabor: Sabor = await session.execute(query)
        sabor = sabor.scalar_one_or_none()

        if sabor:
            # Passo 2
            sabor.nome = novo_nome
            # Passo 3
            await session.commit()
        else:
            print(f'Não existe sabor com ID {id_sabor}')



async def atualizar_picole(id_picole: int, novo_preco: float, novo_sabor: int = None):
    async with create_session() as session:
        # Passo 1
        query = select(Picole).filter(Picole.id == id_picole)
        picole: Picole = await session.execute(query)
        picole = picole.unique().scalar_one_or_none()

        if picole:
            # Passo 2
            picole.preco = novo_preco
            # Se quisermos alterar o sabor também....
            if novo_sabor:
                picole.id_sabor = novo_sabor
            # Passo 3
            await session.commit()
        else:
            print(f'Não existe picole com id {id_picole}')


async def atualiza_sabor():
    from select_main import select_filtro_sabor

    id_sabor = 42

    # # Antes
    await select_filtro_sabor(id_sabor=id_sabor)

    # # Atualizando
    await atualizar_sabor(id_sabor=id_sabor, novo_nome='Abacate')

    # # Depois
    await select_filtro_sabor(id_sabor=id_sabor)


async def atualia_picole():
    id_picole = 21
    novo_preco = 1.99
    id_novo_sabor = 42

    # Antes
    await select_filtro_picole(id_picole=id_picole)

    # Atualizando
    await atualizar_picole(id_picole=id_picole, novo_preco=novo_preco, novo_sabor=id_novo_sabor)

    # Depois
    await select_filtro_picole(id_picole=id_picole)


if __name__ == '__main__':
    # asyncio.run(atualiza_sabor())

    asyncio.run(atualia_picole())
