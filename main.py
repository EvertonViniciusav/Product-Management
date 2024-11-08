import flet as ft

produtos = []

def main(page: ft.Page):
    page.title = "Sistema de Gestão de Produtos"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1800
    page.window_height = 900

    def view(view_name):
        page.views.clear()
        if view_name == "home":
            page.views.append(
                ft.View(
                    controls=[
                        ft.AppBar(title=ft.Text("Home")),
                        home
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        elif view_name == "cadastro":
            page.views.append(
                ft.View(
                    controls=[
                        ft.AppBar(title=ft.Text("Cadastro de Produto")),
                        cadastroProduto
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        elif view_name == "produtos":
            page.views.append(
                ft.View(
                    controls=[
                        ft.AppBar(title=ft.Text("Lista de Produtos")),
                        listaProdutos()
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        page.update()

    def acaoDrawer(e):
        match (drawer.selected_index + 1):
            case 1:
                view("home")
            case 2:
                view("cadastro")
            case 3:
                view("produtos")

    appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU, on_click=lambda e: page.open(drawer)),
        leading_width=40,
        title=ft.Text("Gestão de Produtos"),
        actions=[ft.PopupMenuButton(items=[ft.PopupMenuItem("Configurações")])]
    )

    drawer = ft.NavigationDrawer(
        on_change=acaoDrawer,
        controls=[
            ft.NavigationDrawerDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDrawerDestination(icon=ft.icons.ADD, label="Cadastro de Produto"),
            ft.NavigationDrawerDestination(icon=ft.icons.LIST, label="Lista de Produtos")
        ]
    )

    tf_nomeProduto = ft.TextField(label="Nome do Produto")
    tf_categoria = ft.TextField(label="Categoria")
    tf_preco = ft.TextField(label="Preço")
    tf_quantidade = ft.TextField(label="Quantidade em Estoque")
    msgErro = ft.Text("", size=16, color="red")

    def salvarProduto(e):
        msgErro.value = ""

        nome = tf_nomeProduto.value.strip()
        categoria = tf_categoria.value.strip()
        preco = tf_preco.value.strip()
        quantidade = tf_quantidade.value.strip()

        if not nome:
            msgErro.value = "O campo 'Nome do Produto' é obrigatório!"
        elif not categoria:
            msgErro.value = "O campo 'Categoria' é obrigatório!"
        elif not preco:
            msgErro.value = "O campo 'Preço' é obrigatório!"
        elif not quantidade:
            msgErro.value = "O campo 'Quantidade' é obrigatório!"
        else:
            try:
                preco = float(preco)
                quantidade = int(quantidade)

                produto = {
                    "nome": nome,
                    "categoria": categoria,
                    "preco": preco,
                    "quantidade": quantidade
                }
                produtos.append(produto)

                tf_nomeProduto.value = ""
                tf_categoria.value = ""
                tf_preco.value = ""
                tf_quantidade.value = ""

                view("produtos")

            except ValueError:
                msgErro.value = "Preço ou Quantidade inválidos!"

        page.update()

    cadastroProduto = ft.Column(
        controls=[
            ft.Text("Cadastrar Novo Produto"),
            tf_nomeProduto,
            tf_categoria,
            tf_preco,
            tf_quantidade,
            msgErro,
            ft.ElevatedButton("Salvar", on_click=salvarProduto)
        ]
    )

    def TabelaProdutos():
        rows = []
        for produto in produtos:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto["nome"])),
                        ft.DataCell(ft.Text(produto["categoria"])),
                        ft.DataCell(ft.Text(f"R$ {produto['preco']:.2f}")),
                        ft.DataCell(ft.Text(str(produto["quantidade"])))
                    ]
                )
            )
        return rows

    def listaProdutos():
        return ft.Column(
            controls=[
                ft.Text("Lista de Produtos Cadastrados"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Categoria")),
                        ft.DataColumn(ft.Text("Preço")),
                        ft.DataColumn(ft.Text("Quantidade"))
                    ],
                    rows=TabelaProdutos()
                ),
                ft.ElevatedButton("Adicionar Novo Produto", on_click=lambda e: view("cadastro"))
            ]
        )

    home = ft.Column(
        controls=[
            ft.Text("Bem-vindo ao Sistema de Gestão de Produtos!", size=24, weight="bold", color="orange"),
            ft.Text("Este sistema permite cadastrar, listar e gerenciar seus produtos de maneira eficiente."),
            ft.Divider(),
            ft.Text("Para começar:", size=18, weight="bold", color="orange"),
            ft.Text("1. Acesse a página 'Cadastro de Produto' para adicionar novos produtos."),
            ft.Text("2. Veja os produtos cadastrados na página 'Lista de Produtos'."),
            ft.Divider(),
            ft.Text("Benefícios do Sistema:", size=18, weight="bold", color="orange"),
            ft.Text("• Cadastro de produtos com nome, categoria, preço e quantidade."),
            ft.Text("• Visualização clara dos produtos cadastrados."),
            ft.Text("• Sistema simples e de fácil utilização."),
        ]
    )

    view("home")

ft.app(main, view=ft.AppView.WEB_BROWSER)
