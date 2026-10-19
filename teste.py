import sys
import json
from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class OrcamentoDialog(QDialog):
    """Janela para criar, editar, importar e salvar um orçamento."""

    def __init__(self, parent=None, dados=None, caminho_arquivo=None):
        super().__init__(parent)

        self.caminho_arquivo = caminho_arquivo
        self.setWindowTitle("Editor do orçamento")
        self.resize(760, 520)

        layout_principal = QVBoxLayout(self)

        # Nome do orçamento
        formulario = QFormLayout()
        self.nome_orcamento = QLineEdit()
        self.nome_orcamento.setPlaceholderText("Ex.: compras_outubro")
        formulario.addRow("Nome do orçamento:", self.nome_orcamento)
        layout_principal.addLayout(formulario)

        # Campos para adicionar alimentos
        formulario_alimento = QFormLayout()

        self.nome_alimento = QLineEdit()
        self.nome_alimento.setPlaceholderText("Ex.: Arroz")

        self.quantidade = QSpinBox()
        self.quantidade.setRange(1, 100000)
        self.quantidade.setValue(1)

        self.preco = QDoubleSpinBox()
        self.preco.setRange(0, 100000000)
        self.preco.setDecimals(2)
        self.preco.setPrefix("R$ ")
        self.preco.setValue(0)

        formulario_alimento.addRow("Alimento:", self.nome_alimento)
        formulario_alimento.addRow("Quantidade:", self.quantidade)
        formulario_alimento.addRow("Preço unitário:", self.preco)
        layout_principal.addLayout(formulario_alimento)

        botoes_alimento = QHBoxLayout()
        self.botao_adicionar = QPushButton("Adicionar alimento")
        self.botao_atualizar = QPushButton("Atualizar selecionado")
        self.botao_remover = QPushButton("Remover selecionado")
        botoes_alimento.addWidget(self.botao_adicionar)
        botoes_alimento.addWidget(self.botao_atualizar)
        botoes_alimento.addWidget(self.botao_remover)
        layout_principal.addLayout(botoes_alimento)

        # Tabela de alimentos
        self.tabela = QTableWidget(0, 4)
        self.tabela.setHorizontalHeaderLabels(
            ["Alimento", "Quantidade", "Preço unitário", "Subtotal"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        for coluna in (1, 2, 3):
            self.tabela.horizontalHeader().setSectionResizeMode(
                coluna, QHeaderView.ResizeToContents
            )
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        layout_principal.addWidget(self.tabela)

        self.total_label = QLabel("Total do orçamento: R$ 0,00")
        self.total_label.setAlignment(Qt.AlignRight)
        fonte = self.total_label.font()
        fonte.setBold(True)
        fonte.setPointSize(fonte.pointSize() + 2)
        self.total_label.setFont(fonte)
        layout_principal.addWidget(self.total_label)

        # Botões para salvar
        botoes_arquivo = QHBoxLayout()
        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar_como = QPushButton("Salvar como...")
        self.botao_fechar = QPushButton("Fechar")
        botoes_arquivo.addWidget(self.botao_salvar)
        botoes_arquivo.addWidget(self.botao_salvar_como)
        botoes_arquivo.addStretch()
        botoes_arquivo.addWidget(self.botao_fechar)
        layout_principal.addLayout(botoes_arquivo)

        # Ligações dos botões
        self.botao_adicionar.clicked.connect(self.adicionar_alimento)
        self.botao_atualizar.clicked.connect(self.atualizar_alimento)
        self.botao_remover.clicked.connect(self.remover_alimento)
        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_salvar_como.clicked.connect(self.salvar_como)
        self.botao_fechar.clicked.connect(self.close)
        self.tabela.itemSelectionChanged.connect(self.carregar_selecao)

        # Preenche a janela quando um orçamento foi importado
        if dados:
            self.nome_orcamento.setText(dados.get("nome", ""))
            for alimento in dados.get("alimentos", []):
                self.inserir_linha(
                    alimento.get("nome", ""),
                    alimento.get("quantidade", 1),
                    alimento.get("preco", 0.0),
                )
            self.atualizar_total()
        elif caminho_arquivo:
            self.nome_orcamento.setText(
                Path(caminho_arquivo).stem
            )

    def inserir_linha(self, nome, quantidade, preco):
        linha = self.tabela.rowCount()
        self.tabela.insertRow(linha)

        subtotal = int(quantidade) * float(preco)
        valores = [
            str(nome),
            str(int(quantidade)),
            f"{float(preco):.2f}",
            f"{subtotal:.2f}",
        ]

        for coluna, valor in enumerate(valores):
            item = QTableWidgetItem(valor)
            if coluna > 0:
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela.setItem(linha, coluna, item)

    def adicionar_alimento(self):
        nome = self.nome_alimento.text().strip()
        if not nome:
            QMessageBox.warning(
                self, "Campo obrigatório",
                "Escreva o nome do alimento antes de adicionar."
            )
            self.nome_alimento.setFocus()
            return

        self.inserir_linha(
            nome, self.quantidade.value(), self.preco.value()
        )
        self.atualizar_total()

        self.nome_alimento.clear()
        self.quantidade.setValue(1)
        self.preco.setValue(0)
        self.nome_alimento.setFocus()

    def carregar_selecao(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            return

        self.nome_alimento.setText(self.tabela.item(linha, 0).text())
        self.quantidade.setValue(int(self.tabela.item(linha, 1).text()))
        self.preco.setValue(float(self.tabela.item(linha, 2).text()))

    def atualizar_alimento(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.information(
                self, "Selecionar alimento",
                "Selecione uma linha da tabela para atualizar."
            )
            return

        nome = self.nome_alimento.text().strip()
        if not nome:
            QMessageBox.warning(
                self, "Campo obrigatório",
                "O nome do alimento não pode ficar vazio."
            )
            return

        self.tabela.removeRow(linha)
        self.tabela.insertRow(linha)
        quantidade = self.quantidade.value()
        preco = self.preco.value()
        valores = [
            nome,
            str(quantidade),
            f"{preco:.2f}",
            f"{quantidade * preco:.2f}",
        ]

        for coluna, valor in enumerate(valores):
            item = QTableWidgetItem(valor)
            if coluna > 0:
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela.setItem(linha, coluna, item)

        self.tabela.selectRow(linha)
        self.atualizar_total()

    def remover_alimento(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.information(
                self, "Selecionar alimento",
                "Selecione uma linha da tabela para remover."
            )
            return

        self.tabela.removeRow(linha)
        self.atualizar_total()
        self.nome_alimento.clear()
        self.quantidade.setValue(1)
        self.preco.setValue(0)

    def atualizar_total(self):
        total = 0.0
        for linha in range(self.tabela.rowCount()):
            total += float(self.tabela.item(linha, 3).text())

        self.total_label.setText(
            f"Total do orçamento: R$ {total:,.2f}".replace(",", "X")
            .replace(".", ",").replace("X", ".")
        )

    def obter_dados(self):
        alimentos = []
        for linha in range(self.tabela.rowCount()):
            alimentos.append({
                "nome": self.tabela.item(linha, 0).text(),
                "quantidade": int(self.tabela.item(linha, 1).text()),
                "preco": float(self.tabela.item(linha, 2).text()),
            })

        return {
            "nome": self.nome_orcamento.text().strip(),
            "alimentos": alimentos,
        }

    def salvar(self):
        if self.caminho_arquivo:
            self.salvar_no_caminho(self.caminho_arquivo)
        else:
            self.salvar_como()

    def salvar_como(self):
        nome = self.nome_orcamento.text().strip()
        if not nome:
            QMessageBox.warning(
                self, "Nome obrigatório",
                "Digite o nome do orçamento antes de salvar."
            )
            self.nome_orcamento.setFocus()
            return

        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar orçamento",
            f"{nome}.txt",
            "Arquivos de texto (*.txt)"
        )
        if not caminho:
            return

        if not caminho.lower().endswith(".txt"):
            caminho += ".txt"

        self.salvar_no_caminho(caminho)

    def salvar_no_caminho(self, caminho):
        dados = self.obter_dados()
        if not dados["nome"]:
            QMessageBox.warning(
                self, "Nome obrigatório",
                "Digite o nome do orçamento antes de salvar."
            )
            return

        try:
            # JSON é texto legível e mantém nomes, quantidades e preços
            # para que o programa possa importar e editar depois.
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)

            self.caminho_arquivo = caminho
            QMessageBox.information(
                self, "Orçamento salvo",
                f"Orçamento salvo com sucesso em:\n{caminho}"
            )
        except OSError as erro:
            QMessageBox.critical(
                self, "Erro ao salvar",
                f"Não foi possível salvar o arquivo:\n{erro}"
            )


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meu orçamento")
        self.setMinimumSize(400, 300)

        self.lista = QListWidget()
        self.lista.addItems(["Criar Lista", "Importar Lista"])
        self.setCentralWidget(self.lista)

        self.lista.itemClicked.connect(self.ao_clicar_na_opcao)

    def ao_clicar_na_opcao(self, item):
        if item.text() == "Criar Lista":
            self.criar_lista()
        elif item.text() == "Importar Lista":
            self.importar_lista()

    def criar_lista(self):
        janela = OrcamentoDialog(self)
        janela.exec_()

    def importar_lista(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Importar orçamento",
            "",
            "Arquivos de texto (*.txt)"
        )
        if not caminho:
            return

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, dict) or "alimentos" not in dados:
                raise ValueError(
                    "O arquivo não tem o formato de um orçamento criado "
                    "por este programa."
                )

            janela = OrcamentoDialog(
                self, dados=dados, caminho_arquivo=caminho
            )
            janela.exec_()

        except (OSError, json.JSONDecodeError, ValueError, TypeError) as erro:
            QMessageBox.critical(
                self,
                "Não foi possível importar",
                "Não consegui abrir esse orçamento.\n\n"
                f"Detalhes: {erro}\n\n"
                "Importe um TXT salvo por este programa."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())
