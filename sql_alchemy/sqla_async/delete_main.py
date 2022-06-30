"""
1 - Buscar o registro a ser deletado;
2 - Fazer a deleção do objeto encontrado;
3 - Registrar no banco de dados a deleção;
"""
import asyncio
from sqlalchemy.future import select

from typing import Optional


from conf.db_session import create_session

from models.revendedor import Revendedor
from models.picole import Picole



async def deletar_picole(id_picole: int) -> None:
    async with create_session() as session:
        # Passo 1
        query = select(Picole).filter(Picole.id == id_picole)
        picole: Optional[Picole] = await session.execute(query)
        picole = picole.unique().scalar_one_or_none()

        if picole:
            # Passo 2
            await session.delete(picole)
            # Passo 3
            await session.commit()
        else:
            print(f'Não encontrei picole com id {id_picole}')



async def deletar_revendedor(id_revendedor: int) -> None:
    async with create_session() as session:
        query = select(Revendedor).filter(Revendedor.id == id_revendedor)
        revendedor: Optional[Revendedor] = await session.execute(query)
        revendedor = revendedor.scalar_one_or_none()

        if revendedor:
            await session.delete(revendedor)
            await session.commit()
        else:
            print(f'Não encontrei nenhum revendedor com id {id_revendedor}')


async def select_filtro_revendedor(id_revendedor: int) -> None:
    async with create_session() as session:
        query = select(Revendedor).filter(Revendedor.id == id_revendedor)
        revendedor: Optional[Revendedor] = await session.execute(query)
        revendedor = revendedor.scalar_one_or_none()

        if revendedor:
            print(f'ID: {revendedor.id}')
            print(f'Razão Social: {revendedor.razao_social}')
        else:
            print(f'Não encontrei nenhum revendedor com id {id_revendedor}')


async def deleta_revendedor():
    id_revendedor_nv = 3
    id_revendedor_v = 4

    # Antes
    await select_filtro_revendedor(id_revendedor=id_revendedor_v)

    # Deletar
    await deletar_revendedor(id_revendedor=id_revendedor_v)

    # Depois
    await select_filtro_revendedor(id_revendedor=id_revendedor_v)


async def deleta_picole():
    from update_main import select_filtro_picole

    id_picole = 21

    # # Antes
    await select_filtro_picole(id_picole=id_picole)

    # # Deletar
    await deletar_picole(id_picole=id_picole)

    # # Depois
    await select_filtro_picole(id_picole=id_picole)


if __name__ == '__main__':
    # asyncio.run(deleta_picole())

    asyncio.run(deleta_revendedor())
