import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from groq import Groq
import time
import pygame

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3;*.wav;*.ogg")])
    if caminho_arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho_arquivo)
        botao_transcrever.config(state=tk.NORMAL)
        botao_reproduzir.config(state=tk.NORMAL)

def transcrever_audio():
    caminho_arquivo = entrada_arquivo.get()
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "Arquivo não encontrado.")
        return

    try:
        client = Groq()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inicializar cliente Groq: {str(e)}")
        return

    try:
        with open(caminho_arquivo, "rb") as file:
            progresso["maximum"] = 100
            for i in range(101):
                progresso["value"] = i
                janela.update_idletasks()
                time.sleep(0.01)

            audio_file = file.read()

        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(caminho_arquivo), audio_file),
            model="whisper-large-v3",  # Verifique o nome correto do modelo
            language="pt",
            response_format="verbose_json",
            temperature=0.0
        )

        palavras_com_tempo = []
        for segmento in transcription.segments:
            if hasattr(segmento, 'words'):
                for palavra in segmento.words:
                    palavras_com_tempo.append({
                        "palavra": palavra.word,
                        "inicio": palavra.start,
                        "fim": palavra.end
                    })
            else:
                print(f"Aviso: Segmento sem 'words': {segmento}")

        caixa_texto.delete("1.0", tk.END)
        caixa_texto.insert(tk.END, transcription.text)

        janela.palavras_com_tempo = palavras_com_tempo

        texto_completo = ""
        for i, p in enumerate(palavras_com_tempo):
            if i > 0 and not (p["palavra"].startswith(',') or p["palavra"].startswith('.') or p["palavra"].startswith(';')):
                texto_completo += " "
            texto_completo += p["palavra"]

        janela.texto_completo = texto_completo

        # Exibe o texto no frame do karaokê
        exibir_texto_karaoke(texto_completo)  # Passa o texto completo diretamente

        botao_reproduzir.config(state=tk.NORMAL)

        messagebox.showinfo("Concluído", "Transcrição concluída com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro na transcrição: {str(e)}")
        print(f"Erro detalhado: {e}")

def exibir_texto_karaoke(texto, destaque_inicio=None, destaque_fim=None):
    # Limpa o frame do karaokê
    for widget in frame_karaoke.winfo_children():
        widget.destroy()

    if not texto:
        label_vazio = tk.Label(frame_karaoke, text="Sem texto disponível", bg="black", fg="white", font=("Arial", 16))
        label_vazio.pack(pady=80)
        return

    # Cria um widget Text para exibir o texto
    texto_widget = tk.Text(frame_karaoke, bg="black", fg="white", font=("Arial", 16), wrap=tk.WORD, height=10)
    texto_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    texto_widget.insert("1.0", texto)

    # Configura a tag para destacar a palavra atual
    texto_widget.tag_config("destaque", foreground="yellow", font=("Arial", 16, "bold"))

    # Aplica o destaque se os índices forem válidos
    if destaque_inicio is not None and destaque_fim is not None:
        try:
            texto_widget.tag_add("destaque", f"1.{destaque_inicio}", f"1.{destaque_fim}")
        except tk.TclError:
            print(f"Erro ao destacar texto: índices inválidos {destaque_inicio} a {destaque_fim}")

    # Impede a edição do texto
    texto_widget.config(state=tk.DISABLED)

def reproduzir_audio():
    caminho_arquivo = entrada_arquivo.get()
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "Arquivo não encontrado.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(caminho_arquivo)
        pygame.mixer.music.play()

        janela.tempo_inicio = time.time()
        janela.playing = True

        if hasattr(janela, 'palavras_com_tempo') and janela.palavras_com_tempo:
            if hasattr(janela, 'texto_completo') and janela.texto_completo:
                exibir_texto_karaoke(janela.texto_completo)
            sincronizar_letras()
        else:
            atualizar_tempo()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao reproduzir áudio: {str(e)}")
        print(f"Erro detalhado: {e}")

def atualizar_tempo():
    if not hasattr(janela, 'playing') or not janela.playing:
        return

    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        janela.playing = False
        label_tempo.config(text="Tempo: 0.00s")
        return

    tempo_decorrido = pygame.mixer.music.get_pos() / 1000.0
    label_tempo.config(text=f"Tempo: {tempo_decorrido:.2f}s")

    janela.after(50, atualizar_tempo)

def parar_audio():
    if pygame.mixer.get_init():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    janela.playing = False
    label_tempo.config(text="Tempo: 0.00s")

    if hasattr(janela, 'texto_completo') and janela.texto_completo:
        exibir_texto_karaoke(janela.texto_completo)

def sincronizar_letras():
    if not hasattr(janela, 'playing') or not janela.playing:
        return

    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        janela.playing = False
        label_tempo.config(text="Tempo: 0.00s")
        return

    if not hasattr(janela, 'palavras_com_tempo') or not janela.palavras_com_tempo:
        janela.after(50, sincronizar_letras)
        return

    tempo_decorrido = pygame.mixer.music.get_pos() / 1000.0
    if tempo_decorrido < 0:
        janela.after(50, sincronizar_letras)
        return

    palavras = janela.palavras_com_tempo

    label_tempo.config(text=f"Tempo: {tempo_decorrido:.2f}s")

    if not hasattr(janela, 'texto_completo') or not janela.texto_completo:
        janela.after(50, sincronizar_letras)
        return

    palavra_atual = None
    indice_atual = -1

    # Encontra a palavra atual com base no tempo decorrido
    for i, palavra in enumerate(palavras):
        if palavra["inicio"] <= tempo_decorrido <= palavra["fim"]:
            palavra_atual = palavra
            indice_atual = i
            break

    if palavra_atual:
        try:
            texto_ate_palavra = ""

            # Constrói o texto até a palavra atual
            for i in range(indice_atual):
                texto_ate_palavra += palavras[i]["palavra"]
                if i + 1 < len(palavras) and not (palavras[i+1]["palavra"].startswith(',') or
                                                palavras[i+1]["palavra"].startswith('.') or
                                                palavras[i+1]["palavra"].startswith(';')):
                    texto_ate_palavra += " "

            # Calcula os índices de destaque
            destaque_inicio = len(texto_ate_palavra)
            if destaque_inicio > 0 and texto_ate_palavra[-1] != " " and not palavra_atual["palavra"].startswith((',', '.', ';')):
                destaque_inicio += 1

            destaque_fim = destaque_inicio + len(palavra_atual["palavra"])

            # Exibe o texto com a palavra atual destacada
            exibir_texto_karaoke(janela.texto_completo, destaque_inicio, destaque_fim)
        except Exception as e:
            print(f"Erro ao destacar palavra: {e}")

    # Agenda a próxima atualização
    janela.after(50, sincronizar_letras)

# Interface gráfica
janela = tk.Tk()
janela.title("Karaokê com Groq")
janela.geometry("850x600")

janela.playing = False

frame_principal = tk.Frame(janela)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_arquivo = tk.Frame(frame_principal)
frame_arquivo.pack(fill=tk.X, pady=5)

label_arquivo = tk.Label(frame_arquivo, text="Arquivo de áudio:")
label_arquivo.pack(side=tk.LEFT)

entrada_arquivo = tk.Entry(frame_arquivo, width=50)
entrada_arquivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

botao_selecionar = tk.Button(frame_arquivo, text="Selecionar", command=selecionar_arquivo)
botao_selecionar.pack(side=tk.RIGHT)

frame_transcricao = tk.Frame(frame_principal)
frame_transcricao.pack(fill=tk.X, pady=5)

botao_transcrever = tk.Button(frame_transcricao, text="Transcrever", command=transcrever_audio, state=tk.DISABLED)
botao_transcrever.pack(side=tk.LEFT)

progresso = ttk.Progressbar(frame_transcricao, orient=tk.HORIZONTAL, length=300, mode="determinate")
progresso.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

label_texto = tk.Label(frame_principal, text="Transcrição:")
label_texto.pack(anchor=tk.W, pady=(10, 0))

caixa_texto = tk.Text(frame_principal, height=5, width=80)
caixa_texto.pack(fill=tk.X, expand=False, pady=5)

frame_controles = tk.Frame(frame_principal)
frame_controles.pack(fill=tk.X, pady=5)

botao_reproduzir = tk.Button(frame_controles, text="Reproduzir", command=reproduzir_audio, state=tk.DISABLED)
botao_reproduzir.pack(side=tk.LEFT, padx=5)

botao_parar = tk.Button(frame_controles, text="Parar", command=parar_audio)
botao_parar.pack(side=tk.LEFT, padx=5)

label_tempo = tk.Label(frame_controles, text="Tempo: 0.00s")
label_tempo.pack(side=tk.RIGHT, padx=5)

label_karaoke = tk.Label(frame_principal, text="Karaokê:")
label_karaoke.pack(anchor=tk.W, pady=(10, 0))

frame_karaoke = tk.Frame(frame_principal, bg="black", height=200)
frame_karaoke.pack(fill=tk.BOTH, expand=True, pady=5)

label_vazio = tk.Label(frame_karaoke, text="Selecione um arquivo e faça a transcrição", bg="black", fg="white", font=("Arial", 16))
label_vazio.pack(pady=80)

pygame.init()

janela.mainloop()