from abc import ABC, abstractmethod
import textwrap


class Account:
    def __init__(self, client=None, balance=0.0, number=None, agency="0001", history=None):
        self._client = client  # cls: Client
        self._balance = float(balance)  # float
        self._number = number  # int
        self._agency = agency  # str
        self._history = history if history is not None else History()  # cls: History

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return self._history

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @classmethod
    def new_account(cls, client, number, agency="0001"):
        return cls(client=client, number=number, agency=agency)

    def deposit(self, value):
        if value <= 0:
            return False
        self._balance += value
        return True

    def withdrawal(self, value):
        if value <= 0:
            return False
        if value > self._balance:
            return False
        self._balance -= value
        return True


class CurrentAccount(Account):
    def __init__(self, client=None, balance=0.0, number=None, agency="0001", history=None, limit=500.0, withdrawals_limit=3):
        super().__init__(client=client, balance=balance, number=number, agency=agency, history=history)
        self._limit = float(limit)
        self._withdrawals_limit = int(withdrawals_limit)

    @property
    def limit(self):
        return self._limit

    @property
    def withdrawals_limit(self):
        return self._withdrawals_limit

    @property
    def withdrawals_done(self):
        return sum(1 for transaction in self._history.history if transaction.get("type") == "Withdrawal")

    def withdrawal(self, value):
        withdrawals_today = sum(
            1 for transaction in self._history.history if transaction.get("type") == "Withdrawal"
        )

        if value > self._limit:
            return False

        if withdrawals_today >= self._withdrawals_limit:
            return False

        return super().withdrawal(value)


class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success = account.deposit(self.value)
        if success:
            account.history.add_transaction({"type": "Deposit", "value": self.value})
        return success


class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success = account.withdrawal(self.value)
        if success:
            account.history.add_transaction({"type": "Withdrawal", "value": self.value})
        return success


class History:
    def __init__(self):
        self._history = []

    @property
    def history(self):
        return self._history

    def add_transaction(self, transaction):
        self._history.append(transaction)


class Client:
    def __init__(self, address, bank_accounts=None):
        self._address = address
        self._bank_accounts = bank_accounts if bank_accounts is not None else []

    def make_transaction(self, account, transaction):
        return transaction.register(account)

    def add_account(self, account):
        self._bank_accounts.append(account)

    @property
    def bank_accounts(self):
        return self._bank_accounts

    @property
    def address(self):
        return self._address


class NaturalPerson(Client):
    def __init__(self, cpf, name, born_date, address):
        super().__init__(address=address)
        self._cpf = cpf
        self._name = name
        self._born_date = born_date

    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuario
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text)).strip().lower()


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def recuperar_conta_usuario(usuario):
    if not usuario.bank_accounts:
        print("\n@@@ Usuario nao possui conta cadastrada. @@@")
        return None

    if len(usuario.bank_accounts) == 1:
        return usuario.bank_accounts[0]

    print("\nContas disponiveis:")
    for conta in usuario.bank_accounts:
        print(f"- Conta {conta.number} / Agencia {conta.agency}")

    numero_conta = input("Informe o numero da conta para movimentacao: ").strip()
    if not numero_conta.isdigit():
        print("\n@@@ Numero de conta invalido. @@@")
        return None

    numero_conta = int(numero_conta)
    for conta in usuario.bank_accounts:
        if conta.number == numero_conta:
            return conta

    print("\n@@@ Conta nao encontrada para este usuario. @@@")
    return None


def selecionar_conta(usuarios):
    cpf = input("Informe o CPF do usuario: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuario nao encontrado. @@@")
        return None, None

    conta = recuperar_conta_usuario(usuario)
    return usuario, conta


def depositar(usuarios):
    usuario, conta = selecionar_conta(usuarios)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do deposito: "))
    except ValueError:
        print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")
        return

    transacao = Deposit(valor)
    if usuario.make_transaction(conta, transacao):
        print("\n=== Deposito realizado com sucesso! ===")
    else:
        print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")


def sacar(usuarios):
    usuario, conta = selecionar_conta(usuarios)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")
        return

    if valor <= 0:
        print("\n@@@ Operacao falhou! O valor informado e invalido. @@@")
        return

    if valor > conta.balance:
        print("\n@@@ Operacao falhou! Voce nao tem saldo suficiente. @@@")
        return

    if isinstance(conta, CurrentAccount) and valor > conta.limit:
        print("\n@@@ Operacao falhou! O valor do saque excede o limite. @@@")
        return

    if isinstance(conta, CurrentAccount) and conta.withdrawals_done >= conta.withdrawals_limit:
        print("\n@@@ Operacao falhou! Numero maximo de saques excedido. @@@")
        return

    transacao = Withdrawal(valor)
    if usuario.make_transaction(conta, transacao):
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operacao falhou! Nao foi possivel realizar o saque. @@@")


def exibir_extrato(usuarios):
    _, conta = selecionar_conta(usuarios)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    if not conta.history.history:
        print("Nao foram realizadas movimentacoes.")
    else:
        for transacao in conta.history.history:
            tipo = "Deposito" if transacao["type"] == "Deposit" else "Saque"
            print(f"{tipo}:\t\tR$ {transacao['value']:.2f}")

    print(f"\nSaldo:\t\tR$ {conta.balance:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente numero): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Ja existe usuario com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    usuarios.append(NaturalPerson(cpf=cpf, name=nome, born_date=data_nascimento, address=endereco))
    print("=== Usuario criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuario: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuario nao encontrado, fluxo de criacao de conta encerrado! @@@")
        return

    conta = CurrentAccount.new_account(client=usuario, number=numero_conta, agency=agencia)
    usuario.add_account(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        linha = f"""\
            Agencia:\t{conta.agency}
            C/C:\t\t{conta.number}
            Titular:\t{conta.client.name}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    agencia = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(usuarios)

        elif opcao == "s":
            sacar(usuarios)

        elif opcao == "e":
            exibir_extrato(usuarios)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(agencia, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operacao invalida, por favor selecione novamente a operacao desejada.")


if __name__ == "__main__":
    main()