import iptc, os, sys
from tkinter import *

def resolvePermissoes():
    euid = os.geteuid()
    if euid != 0:
        sudado = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *sudado)

def addRegra(ipFonte, ipDestino, portaFonte, portaDestino, estado, username, acao, protocolo, chain):
    regra = iptc.Rule()
    
    chains = ["INPUT", "OUTPUT"]
    indiceChain = int(chain)-1
    chain = chains[indiceChain]

    acoes = ["ACCEPT", "DROP"]
    indiceAcao = int(acao)-1
    acao = acoes[indiceAcao]

    protocolos = ["TCP", "UDP", ""]
    indiceProtocolo = int(protocolo)-1
    protocolo = protocolos[indiceProtocolo]

    if(protocolo):
        regra.protocol = protocolo
    if(ipFonte):
        regra.src = ipFonte
    if(ipDestino):
        regra.dst = ipDestino
    if(portaFonte):
        regra.sport = portaFonte
    if(portaDestino):
        regra.dport = portaDestino

    if(username):
        match = iptc.Match(regra, "owner")
        match.uid_owner = username
        regra.add_match(match)
    if(estado):
        match = iptc.Match(regra, "conntrack")
        match.ctstate = estado
        regra.add_match(match)

    target = iptc.Target(regra, acao)
    regra.target = target

    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)
    chain.append_rule(regra)

# Inicialização do script e da janela
resolvePermissoes()

janela = Tk()
janela.title("PythonTables")
janela.resizable(False, False)

# Declaração dos elementos da interface
labelFonte = Label(janela, text="IP+Porta (origem):")
labelDestino = Label(janela, text="IP+Porta (destino):")
labelTipo = Label(janela, text="Chain: ")
labelAcao = Label(janela, text="Ação: ")
labelProtocolo = Label(janela, text="Protocolo: ")
labelUsuario = Label(janela, text="Aplicar ao usuário (opcional): ")
labelEstado = Label(janela, text="Estados (opcional): ")
labelEstado2 = Label(janela, text="(separe-os com vírgulas)")
edIPFonte = Entry(janela,)
edPortaFonte = Entry(janela,)
edIPDestino = Entry(janela,)
edPortaDestino = Entry(janela,)
edUsuario = Entry(janela,)
edEstado = Entry(janela,)


# RADIO BUTTONS DOS CHAINS
sv1 = StringVar(janela, "1") 
tipos = {"INPUT" : "1", 
        "OUTPUT" : "2"}

for (texto, numero) in tipos.items(): 
    Radiobutton(janela, text = texto, variable = sv1, value = numero).grid(row=2, column=numero) 

# RADIO BUTTONS DOS TARGETS
sv2 = StringVar(janela, "1") 
opcoes = {"ACCEPT" : "1", 
        "DROP" : "2"} 
for (texto, numero) in opcoes.items(): 
    Radiobutton(janela, text = texto, variable = sv2, value = numero).grid(row=3, column=numero) 

# RADIO BUTTONS DOS PROTOCOLOS
sv3 = StringVar(janela, "3") 
protocolos = {"TCP" : "1", 
        "UDP" : "2",
        "AMBOS" : "3"} 
for (texto, numero) in protocolos.items(): 
    Radiobutton(janela, text = texto, variable = sv3, value = numero).grid(row=4, column=numero) 

# POSICIONAMENTO DOS BOTÕES
labelFonte.grid(row=0, column=0)
labelDestino.grid(row=1, column=0)
labelTipo.grid(row=2, column=0)
labelAcao.grid(row=3, column=0)
labelProtocolo.grid(row=4, column=0)
labelEstado.grid(row=6, column=0)
labelEstado2.grid(row=6, column=2)
labelUsuario.grid(row=5, column=0)
edIPFonte.grid(row=0, column=1)
edPortaFonte.grid(row=0, column=2)
edIPDestino.grid(row=1, column=1)
edPortaDestino.grid(row=1, column=2)
edUsuario.grid(row=5,column=1)
edEstado.grid(row=6, column=1)

# Obtenção das strings e chamada da função addRegra com passagem de parâmetros
def botaoAddRegra():
    ipFonte = edIPFonte.get()
    ipDestino = edIPDestino.get()
    portaFonte = edPortaFonte.get()
    portaDestino = edPortaDestino.get()
    estado = edEstado.get()
    username = edUsuario.get()
    chain = sv1.get()
    acao = sv2.get()
    protocolo = sv3.get()
    addRegra(ipFonte, ipDestino, portaFonte, portaDestino, estado, username, acao, protocolo, chain)

# Ação de click no botão, posicionamento do botão e fim da janela
bt = Button(janela, text="Adicionar regra", command=botaoAddRegra, bg='#0052cc', fg='#ffffff')
bt.grid(row=8, column=1)
janela.mainloop()