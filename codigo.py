

import flet as ft

def main(pagina):
    texto = ft.Text("Nimcord Live Chat")
    
    chat = ft.Column()
    
    nome_usuario = ft.TextField(label="Digite seu nome de usuario")
    
    #enviar as mensagens, o q aparece p todos (Front passo 4)
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size=12, italic=True, color=ft.colors.PURPLE))
        pagina.update()
        
    #Publish and Subscrub, integrando o Backend ao Frontend que ja tenho (Back passo 1)
    pagina.pubsub.subscribe(enviar_mensagem_tunel)
    
    #enviar as mensagens e limpa o campo de mensagem p mim (Front passo 5)
    def enviar_mensagem (evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})
        campo_mensagem.value = "" 
        pagina.update()    
    
    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)
    
    #fechar o popup e entrar no chat (Front passo 3)
    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo":"entrada"})
        pagina.add(chat)
        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
            ))
        pagina.update()
    
    #popup para definir o usuario e entrar no chat com o nome (Front passo 2)
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Seja bem vindo ao Nimcord"),
        content= nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )
    
    #botão pra entrar no chat na pagina inicial (Front passo 1)
    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()
    
    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)
    
    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=5912) 