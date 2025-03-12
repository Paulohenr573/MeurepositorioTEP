import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from groq import Groq
import time

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3;*.wav;*.ogg")])
    if caminho_arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho_arquivo)
        botao_transcrever.config(state=tk.NORMAL)

def transcrever_audio():
    caminho_arquivo = entrada_arquivo.get()
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "Arquivo não encontrado.")
        return

    client = Groq()

    try:
        with open(caminho_arquivo, "rb") as file:
            progresso["maximum"] = 100
            for i in range(101):
                progresso["value"] = i
                janela.update_idletasks()
                time.sleep(0.05)

            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(caminho_arquivo), file.read()),
                model="whisper-large-v3-turbo",
                language="pt",
                response_format="verbose_json",
                temperature=0.0
            )

            caixa_texto.delete("1.0", tk.END)
            caixa_texto.insert(tk.END, transcription.text)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na transcrição: {e}")

janela = tk.Tk()
janela.title("Transcrição de áudio com Groq")

label_arquivo = tk.Label(janela, text="Caminho do arquivo:")
label_arquivo.pack()
entrada_arquivo = tk.Entry(janela, width=50)
entrada_arquivo.pack()

botao_selecionar = tk.Button(janela, text="Selecionar arquivo", command=selecionar_arquivo)
botao_selecionar.pack()

botao_transcrever = tk.Button(janela, text="Transcrever", command=transcrever_audio, state=tk.DISABLED)
botao_transcrever.pack()

caixa_texto = tk.Text(janela, height=10, width=50)
caixa_texto.pack()

progresso = ttk.Progressbar(janela, orient=tk.HORIZONTAL, length=200, mode="determinate")
progresso.pack()

janela.mainloop()