from conf.db_session import create_session

# Insert parte 1
from models.aditivo_nutritivo import AditivoNutritivo
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole
from models.ingrediente import Ingrediente
from models.conservante import Conservante
from models.revendedor import Revendedor
# Insert parte 2
from models.lote import Lote
from models.nota_fiscal import NotaFiscal
from models.picole import Picole


# 1 Aditivo Nutritivo
def insert_aditivo_nutritivo() -> AditivoNutritivo:
    print('Cadastrando Atditivo Nutritivo')

    nome: str = input('Informe o nome do aditivo nutritivo: ')
    formula_quimica: str = input('Informe a fórmula química do aditivo nutritivo: ')

    an: AditivoNutritivo = AditivoNutritivo(nome=nome, formula_quimica=formula_quimica)

    with create_session() as session:
        session.add(an)

        session.commit()

        return an
    
    # print('Aditivo Nutritivo cadastrado com sucesso')
    # print(f'ID: {an.id}')
    # print(f'Data: {an.data_criacao}')
    # print(f'Nome: {an.nome}')
    # print(f'Fórmula Química: {an.formula_quimica}')


# 2 Sabor
def insert_sabor() -> None:
    print('Cadastrando Sabor')

    nome: str = input('Informe o nome do sabor: ')

    sabor: Sabor = Sabor(nome=nome)

    with create_session() as session:
        session.add(sabor)

        session.commit()
    
    print('Sabor cadastrado com sucesso')
    print(f'ID: {sabor.id}')
    print(f'Data: {sabor.data_criacao}')
    print(f'Nome: {sabor.nome}')



# 3 Tipo Embalagem
def insert_tipo_embalagem() -> None:
    print('Cadastrando Tipo Embalagem')

    nome: str = input('Informe o nome do Tipo Embalagem: ')

    te: TipoEmbalagem = TipoEmbalagem(nome=nome)

    with create_session() as session:
        session.add(te)

        session.commit()
    
    print('Tipo Embalagem cadastrado com sucesso')
    print(f'ID: {te.id}')
    print(f'Data: {te.data_criacao}')
    print(f'Nome: {te.nome}')


# 4 Tipo Picole
def insert_tipo_picole() -> None:
    print('Cadastrando Tipo Picole')

    nome: str = input('Informe o nome do Tipo Picole: ')

    tp: TipoPicole = TipoPicole(nome=nome)

    with create_session() as session:
        session.add(tp)

        session.commit()
    
    print('Tipo Picole cadastrado com sucesso')
    print(f'ID: {tp.id}')
    print(f'Data: {tp.data_criacao}')
    print(f'Nome: {tp.nome}')


# 5 Ingrediente
def insert_ingrediente() -> Ingrediente:
    print('Cadastrando Ingrediente')

    nome: str = input('Informe o nome do Ingrediente: ')

    ingrediente: Ingrediente = Ingrediente(nome=nome)

    with create_session() as session:
        session.add(ingrediente)

        session.commit()

        return ingrediente
    
    # print('Ingrediente cadastrado com sucesso')
    # print(f'ID: {ingrediente.id}')
    # print(f'Data: {ingrediente.data_criacao}')
    # print(f'Nome: {ingrediente.nome}')


# 6 Conservante
def insert_conservante() -> Conservante:
    print('Cadastrando Conservante')

    nome: str = input('Informe o nome do Conservante: ')
    descricao: str = input('Informe a descrição do Conservante: ')

    conservante: Conservante = Conservante(nome=nome, descricao=descricao)

    with create_session() as session:
        session.add(conservante)

        session.commit()

        return conservante
    
    # print('Conservante cadastrado com sucesso')
    # print(f'ID: {conservante.id}')
    # print(f'Data: {conservante.data_criacao}')
    # print(f'Nome: {conservante.nome}')
    # print(f'Descrição: {conservante.descricao}')


# 7 Revendedor
def insert_revendedor() -> Revendedor:
    print('Cadastrando Revendedor')

    cnpj: str = input('Informe o CNPJ do Revendedor: ')
    razao_social: str = input('Informe a Razão Social do Revendedor: ')
    contato: str = input('Informe o Contato do Revendedor: ')

    revendedor: Revendedor = Revendedor(cnpj=cnpj, razao_social=razao_social, contato=contato)

    with create_session() as session:
        session.add(revendedor)

        session.commit()
    
    return revendedor


# 8 Lote
def insert_lote() -> Lote:
    print('Cadastrando Lote')

    id_tipo_picole: int = input('Informe o ID do tipo do picole: ')
    quantidade: int = input('Informe a quantidade de picole: ')
    

    lote: Lote = Lote(id_tipo_picole=id_tipo_picole, quantidade=quantidade)

    with create_session() as session:
        session.add(lote)

        session.commit()
    
    return lote

# 9 Nota Fiscal
def insert_nota_fical() -> None:
    print('Cadastrando Nota Fiscal')

    valor: float = input('Informe o valor da nota fiscal: ')
    numero_serie: str = input('Informe o número de série: ')
    descricao: str = input('Informe a descrição: ')

    rev = insert_revendedor()
    id_revendedor = rev.id

    nf: NotaFiscal = NotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao, id_revendedor=id_revendedor)

    lote1 = insert_lote()
    nf.lotes.append(lote1)

    lote2 = insert_lote()
    nf.lotes.append(lote2)

    with create_session() as session:
        session.add(nf)

        session.commit()
    
        print('Nota Fiscal cadastrada com sucesso')
        print(f'ID: {nf.id}')
        print(f'Data: {nf.data_criacao}')
        print(f'Valor: {nf.valor}')
        print(f'Número de Série: {nf.numero_serie}')
        print(f'Descrição: {nf.descricao}')
        print(f'ID Revendedor: {nf.id_revendedor}')
        print(f'Revendedor: {nf.revendedor.razao_social}')


# 10 Picole
def insert_picole() -> None:
    print('Cadastrando Picole')

    preco: float = input('Informe o preço do picole: ')
    id_sabor: int = input('Informe o ID do sabor: ')
    id_tipo_picole: int = input('Informe o ID do tipo de picole: ')
    id_tipo_embalagem: int = input('Informe o ID do tipo da embalagem: ')

    picole: Picole = Picole(id_sabor=id_sabor, id_tipo_embalagem=id_tipo_embalagem, id_tipo_picole=id_tipo_picole, preco=preco)

    ingrediente1 = insert_ingrediente()
    picole.ingredientes.append(ingrediente1)

    ingrediente2 = insert_ingrediente()
    picole.ingredientes.append(ingrediente2)

    # Tem conservantes?
    conservante = insert_conservante()
    picole.conservantes.append(conservante)

    # Tem aditivos nutritivos?
    aditivo_nutritivo = insert_aditivo_nutritivo()
    picole.aditivos_nutritivos.append(aditivo_nutritivo)

    with create_session() as session:
        session.add(picole)

        session.commit()
    
        print('Picole cadastrado com sucesso')
        print(f'ID: {picole.id}')
        print(f'Data: {picole.data_criacao}')
        print(f'Preço: {picole.preco}')
        print(f'Sabor: {picole.sabor.nome}')
        print(f'Tipo Picole: {picole.tipo_picole.nome}')
        print(f'Tipo Embalagem: {picole.tipo_embalagem.nome}')
        print(f'Ingredientes: {picole.ingredientes}')
        print(f'Conservantes: {picole.conservantes}')
        print(f'Aditivos Nutritivos: {picole.aditivos_nutritivos}')


if __name__ == '__main__':
    # 1 Aditivo Nutritivo
    # insert_aditivo_nutritivo()

    # 2 Sabor
    # insert_sabor()

    # 3 Tipo Embalagem
    # insert_tipo_embalagem()

    # 4 Tipo Picole
    # insert_tipo_picole()

    # 5 Ingrediente
    # insert_ingrediente()

    # 6 Conservante
    # insert_conservante()

    # 7 Revendedor
    # rev = insert_revendedor()
    # print(f'ID: {rev.id}')
    # print(f'Data: {rev.data_criacao}')
    # print(f'CNPJ: {rev.cnpj}')
    # print(f'Razão Social: {rev.razao_social}')
    # print(f'Contato: {rev.contato}')

    # 8 Lote
    # lot = insert_lote()
    # print(f'ID: {lot.id}')
    # print(f'Data: {lot.data_criacao}')
    # print(f'ID Tipo Picole: {lot.id_tipo_picole}')
    # print(f'Quantidade: {lot.quantidade}')

    # 9 Nota Fiscal
    # insert_nota_fical()

    # 10 Picole
    insert_picole()
