import webbrowser

from pytube import YouTube

progresso = 0


def cria_txt():
    with open('links.txt', 'w') as f:
        f.write('Coloque os links que deseja baixar aqui!!\nE abra novamente o programa')
    abre_txt()


def verifica_link(urls):
    for i in urls:
        if 'youtube.com' in i:
            ok = True
    if not ok:
        print('Coloque os links que deseja baixar no arquivo links.txt')
        webbrowser.open('links.txt')
        ok = False
    return ok


def abre_txt():
    print('Coloque os links que deseja baixar no arquivo links.txt')
    webbrowser.open('links.txt')


def on_progress(stream, chunk, bytes_remaining):
    global progresso

    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = int(bytes_downloaded / total_size * 100)
    if liveprogress > progresso:
        progresso = liveprogress
        print(f'Baixando {progresso}%')


def yt_download(url):
    if 'youtube.com' in url:
        try:
            yt = YouTube(url[:-1])
            print(f'\nBaixando agora : {yt.title}')
            yt.register_on_progress_callback(on_progress)
            yt.streams.get_highest_resolution().download()

        except Exception as e:
            print("Ocorreu um erro!   " + str(e))


# tenta executar se o arquivo links.txt existir
try:
    with open('links.txt', 'r') as f:
        print(f'{"-" * 50}\nYouTubeDownloader by Christian 2021\n{"-" * 50}')
        urls = f.readlines()
        ok = verifica_link(urls)
        # se a variavel ok (existir o arquivo links.txt) for true
        if ok:
            print(f'Links na fila para download : ')
            for i in urls:
                print(i)
            # verifica se existe algum link do youtube dentro do arquivo
            for i in urls:
                if 'youtube.com' in i:
                    # print(f'\n{i[:-1]}')
                    yt_download(i)
                    progresso = 0
            fim = input('Download Terminado...')
        else:
            abre_txt()
except Exception as e:
    print('Não existe o arquivo com os links dentro da pasta')
    print('Criando o arquivo')
    cria_txt()
    print('Por favor execute novamente o programa')
