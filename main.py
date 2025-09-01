import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

historico = []

# ------------------- Cálculos -------------------
def calcular_pegada(respostas):
    resultado = 0
    resultado += (respostas[0] // 20) * 5
    resultado += (5 - (respostas[1] // 20)) * 5
    if respostas[2] <= 2: resultado += 5
    elif respostas[2] <= 5: resultado += 10
    else: resultado += 20
    resultado += respostas[3] * 20
    resultado += (respostas[4] // 20) * 5
    return resultado // 20

def salvar_historico():
    try:
        with open("historico_pegada_ecologica.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write("HISTÓRICO DE TESTES DE PEGADA ECOLÓGICA\n" + "=" * 50 + "\n\n")
            for i, teste in enumerate(historico):
                arquivo.write(f"Teste #{i+1}\nNome: {teste['nome']}\n")
                arquivo.write(f"Resultado: {teste['planetas']} planetas Terra\n" + "=" * 30 + "\n\n")
        return "Histórico salvo em historico_pegada_ecologica.txt"
    except Exception as e:
        return f"Erro ao salvar histórico: {e}"

# ------------------- Funções da Interface -------------------
def realizar_teste():
    def finalizar():
        try:
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite seu nome.")
                return

            respostas = []
            # Pergunta 1: porcentagem (slider)
            respostas.append(slider1.get())
            # Pergunta 2: porcentagem (slider)
            respostas.append(slider2.get())
            # Pergunta 3: número de pessoas (entry)
            valor_pessoas = var_pessoas.get()
            if valor_pessoas < 1:
                messagebox.showerror("Erro", "Número de pessoas deve ser >= 1")
                return
            respostas.append(valor_pessoas)
            # Pergunta 4: energia elétrica (botão)
            respostas.append(var_energia.get())
            # Pergunta 5: porcentagem (slider)
            respostas.append(slider5.get())

            qtd_planetas = calcular_pegada(respostas)
            historico.append({'nome': nome, 'planetas': qtd_planetas, 'respostas': respostas.copy()})

            messagebox.showinfo("Resultado", f"{nome}, sua pegada ecológica equivale a {qtd_planetas} planetas Terra")
            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel(root)
    janela.title("Realizar Teste")

    ttk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="w")
    entry_nome = ttk.Entry(janela, width=30)
    entry_nome.grid(row=0, column=1, pady=5)

    # Pergunta 1: slider
    ttk.Label(janela, text="Com que frequência você consome produtos de origem animal? (0-100%)").grid(row=1, column=0, sticky="w", pady=2)
    slider1 = ttk.Scale(janela, from_=0, to=100, orient="horizontal")
    slider1.set(50)
    slider1.grid(row=1, column=1, pady=2)

    # Pergunta 2: slider
    ttk.Label(janela, text="Qual a percentagem de comida não processada/local? (0-100%)").grid(row=2, column=0, sticky="w", pady=2)
    slider2 = ttk.Scale(janela, from_=0, to=100, orient="horizontal")
    slider2.set(50)
    slider2.grid(row=2, column=1, pady=2)

    # Pergunta 3: número de pessoas (entry)
    ttk.Label(janela, text="Quantas pessoas residem no seu agregado familiar?").grid(row=3, column=0, sticky="w", pady=2)
    var_pessoas = tk.IntVar(value=1)
    entry_pessoas = ttk.Entry(janela, textvariable=var_pessoas, width=10)
    entry_pessoas.grid(row=3, column=1, pady=2)

    # Pergunta 4: energia elétrica (botão)
    ttk.Label(janela, text="Você tem energia elétrica em casa?").grid(row=4, column=0, sticky="w", pady=2)
    var_energia = tk.IntVar(value=1)
    frame_energia = ttk.Frame(janela)
    frame_energia.grid(row=4, column=1, pady=2)
    ttk.Radiobutton(frame_energia, text="Sim", variable=var_energia, value=1).pack(side="left")
    ttk.Radiobutton(frame_energia, text="Não", variable=var_energia, value=0).pack(side="left")

    # Pergunta 5: slider
    ttk.Label(janela, text="Com que frequência você viaja de avião anualmente? (0-100%)").grid(row=5, column=0, sticky="w", pady=2)
    slider5 = ttk.Scale(janela, from_=0, to=100, orient="horizontal")
    slider5.set(0)
    slider5.grid(row=5, column=1, pady=2)

    ttk.Button(janela, text="Finalizar Teste", command=finalizar).grid(row=6, columnspan=2, pady=10)

def mostrar_historico():
    janela = tk.Toplevel(root)
    janela.title("Histórico de Testes")

    if not historico:
        ttk.Label(janela, text="Nenhum teste realizado ainda.").pack(pady=10)
        return

    texto = tk.Text(janela, width=60, height=20)
    texto.pack(padx=10, pady=10)

    for i, teste in enumerate(historico):
        texto.insert(tk.END, f"Teste #{i+1}\nNome: {teste['nome']}\n")
        texto.insert(tk.END, f"Resultado: {teste['planetas']} planetas Terra\n")
        texto.insert(tk.END, "="*40 + "\n\n")

def mostrar_grafico():
    if not historico:
        messagebox.showerror("Erro", "Nenhum dado disponível para gráfico.")
        return

    janela = tk.Toplevel(root)
    janela.title("Gráfico - Pegada Ecológica")

    largura, altura = 700, 400
    janela.geometry(f"{largura}x{altura}")

    ultimos_testes = historico[-10:] if len(historico) > 10 else historico
    nomes = [teste['nome'] for teste in ultimos_testes]
    planetas = [teste['planetas'] for teste in ultimos_testes]

    fig, ax = plt.subplots(figsize=(largura/100, altura/100))
    ax.bar(range(len(nomes)), planetas, color="green", alpha=0.7)
    ax.set_xticks(range(len(nomes)))
    ax.set_xticklabels(nomes, rotation=45)
    ax.set_ylabel("Planetas Terra")
    ax.set_title("Pegada Ecológica")

    for i, v in enumerate(planetas):
        ax.text(i, v + 0.1, str(v), ha="center")

    # Salva o gráfico como imagem PNG
    fig.savefig("grafico_pegada_ecologica.png", bbox_inches="tight")

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def mostrar_arquivo():
    janela = tk.Toplevel(root)
    janela.title("Arquivo de Histórico")

    try:
        msg = salvar_historico()
        texto = tk.Text(janela, width=70, height=25)
        texto.pack(padx=10, pady=10)

        with open("historico_pegada_ecologica.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        texto.insert(tk.END, conteudo)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

# ------------------- Janela Principal -------------------
root = tk.Tk()
root.title("Calculadora de Pegada Ecológica")
root.geometry("400x300")

ttk.Label(root, text="Calculadora de Pegada Ecológica", font=("Arial", 14, "bold")).pack(pady=20)

ttk.Button(root, text="Realizar Teste", command=realizar_teste).pack(pady=5, fill="x", padx=50)
ttk.Button(root, text="Ver Histórico", command=mostrar_historico).pack(pady=5, fill="x", padx=50)
ttk.Button(root, text="Gerar Gráfico", command=mostrar_grafico).pack(pady=5, fill="x", padx=50)
ttk.Button(root, text="Ver Arquivo de Histórico", command=mostrar_arquivo).pack(pady=5, fill="x", padx=50)
ttk.Button(root, text="Sair", command=root.quit).pack(pady=20, fill="x", padx=50)

root.mainloop()
