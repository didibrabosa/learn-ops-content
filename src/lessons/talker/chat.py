# -*- coding: utf-8 -*-
from operator import le
import os
import random
from time import sleep
import time
import sys
from pprint import pformat
from typing import Any
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer, BashLexer, DockerLexer, JsonLexer, YamlLexer
import getpass

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

lexers = {
    "python": PythonLexer(),
    "shell": BashLexer(),
    "bash": BashLexer(),
    "docker": DockerLexer(),
    "dockerfile": DockerLexer(),
    "json": JsonLexer(),
    "yaml": YamlLexer(),
    "yml": YamlLexer(),
}


nextStepMessages = [
    """Ok, entendi...""",
    """Certo, vamos ver esse negócio""",
    """Hummm... interessante!""",
    """Vamos falar sobre isso...""",
    """Bom ponto! Vamos falar disso aí...""",
    """Não é complexo, vamos olhar de perto...""",
    """Vamos ver isso aí...""",
    """Olha... vc tem razão, um passo de cada vez, vamos explicar essa parte...""",
    """Estamos indo bem, vamos chegar lá...""",
    """Vamos com calma... vou te explicar isso...""",
    """Um passo de cada vez querido Doença...""",
    """Vamos chegar nesse dia...""",
    """Qual problema você quer resolver? (tenho q dizer isso... rs...)""",
    """Vamos ver isso aí...""",
]

pressEnterMessages = [
    """Para continuar, aperta o ENTER aí...""",
    """ENTER e vamos em frente...""",
    """Será que hoje vai chover? Aperta o ENTER aí para seguir...""",
    """Aperta o ENTER aí vai...""",
    """Manda um ENTER pra continuarmos...""",
    """Só estou esperando vc apertar o ENTER para seguirmos...""",
    """No seu tempo campeão... aperta o ENTER aí quando vc quiser...""",
    """E aí? td bem com vc? quando estiver de boa, aperta o ENTER aí que continuamos... """,
    """Tá divertido? quando quiser, aperta o ENTER que vamos em frente...""",
    """Vamos com calma...mas vc precisa apertar o ENTER para continuarmos...""",    
    """Aperta o ENTER aí...""",
    """Quando vc estiver de boa, aperta o ENTER aí que continuamos...""",
    """Aperta o ENTER aí que vamos em frente...""",
    """Vamos lá, aperta o ENTER aí...""",
    """CTRL+C para tudo, mas se vc quiser continuar, aperta o ENTER aí...""",
    """Tá com preguiça? aperta o ENTER aí que continuamos...""",
    """Eu tbm tô cansado, mas aperta o ENTER aí que continuamos...""",
    """Sei que é muita coisa, mas temos que continuar, aperta o ENTER aí...""",
    """Ah... nem é tão complicado assim, sei que vc já fez coisa pior.. aperta o ENTER aí...""",
    """Se precisar, vai buscar um café e depois aperta o ENTER aí...""",
]

def ClearScreen():
    # Linux
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # windows
        _ = os.system('cls')


class Chat:
    _teacher = ""
    _student = ""
    _wait = 1
    _fastMode = False

    def __init__(self, teacher="Fino", student=getpass.getuser(), wait=1, fastMode=False):
        if student is None or student == "" or student == "root":
            student = "Doença"

        self._student = student
        self._teacher = teacher
        self._wait = 0
        self._fastMode = True

        # Lista os comandos básicos
        self.Speak(f"Olá, eu sou o {self._teacher} e estou aqui para tentar ajudar um pouco...")
        self.Speak(f"Temos alguns comandos:")
        self.Speak("Caso queira sair, aperte CTRL+C a qualquer momento")
        self.Speak(f"No momento em que te pedirem para teclar um 'ENTER', você pode:")
        self.Speak(" - Apertar a tecla ENTER para continuar")
        self.Speak(" - Apertar a tecla 'Q' para sair")
        self.Speak(" - Apertar a tecla 'F' para ativar o modo rápido")
        self.Speak(" - Apertar a tecla 'S' para desativar o modo rápido")
        self._wait = wait
        self._fastMode = fastMode

        self.AskEnter()

    def Teacher(self) -> str:
        return self._teacher
    
    def Student(self) -> str:
        return self._student
    
    def SetFastMode(self, fast: bool):
        self._fastMode = fast
    
    def Wait(self, wait: float):
        if self._fastMode:
            return
        time.sleep(wait)

    def slowPrint(self, msg):
        for char in msg:     
            sys.stdout.write(char)
            sys.stdout.flush()
            if char == " ":
                wait = 0.01*(random.randint(0,8))
            else:
                wait = 0.001*(random.randint(0,80))
            self.Wait(wait)

    def Speak(self, msg):
        for line in msg.splitlines():
            print(color.END + color.PURPLE + color.BOLD + "# [{0}] ".format(self._teacher) +
                  color.END + color.GREEN, end="")
            self.slowPrint(line)
            print(color.END)

            # Espera um pouquinho para cada linha poder ser lida...
            self.Wait(len(line)/200)

    def StudentComment(self, msg):
        print(color.END + color.DARKCYAN + color.BOLD +
              "# [{0}] ".format(self._student) + color.END + color.YELLOW, end="")
        self.slowPrint(msg)
        print(color.END)
        self.Wait(self._wait)

    def Question(self, msg, wait=True):
        print(color.END + color.DARKCYAN + color.BOLD +
              "# [{0}] ".format(self._student) + color.END + color.YELLOW, end="")
        self.slowPrint(msg)
        print(color.END)
        self.Wait(self._wait)
        if wait:
            self.NextStep()
    
    def getLexer(self, lang):
        if lang.lower() in lexers:
            return lexers[lang]
        
        if not lang:
            return lexers["python"]
        
        try:
            ret = get_lexer_by_name(lang)
        except:
            return lexers["python"]
                
        return ret
                
    
    def isEmpty(self, line) -> bool:
            if line == "" or line.isspace() or line == "\n" or line == "\r" or line == "\r\n" or line == "\n\r" or line == "\r\n":
                return True
            
            return False
    
    def ShowCode(self, code, wait=True, lexer="python"):
        print(color.END + color.BOLD + f"# [{lexer} code]:" + color.END)
        ln = 1
        self.printBar()
        for line in code.splitlines():
            if self.isEmpty(line):
                continue

            print(color.END + color.BOLD + color.BLUE + "| {:03d} ".format(ln) + color.END + highlight(line, self.getLexer(lexer), Terminal256Formatter()), end="")
            ln += 1

        self.printBar()
        if wait:
            self.AskEnter()

    def printBar(self):
        print(color.END + color.BOLD + color.BLUE + " ", end="")
        width = os.get_terminal_size().columns
        for s in range(width - 2):
            print(chr(3196), end="")
        print(color.END)

    def ShowCodeAndRun(self, code, wait=True, lexer="python"):
        self.ShowCode(code, wait=False, lexer=lexer)
        
        print(color.END + color.BOLD +
                f"# [{lexer} code] Result:" + color.END)
        exec(code)
        print(color.END, end="")

        if wait:
            self.AskEnter()

    def ShowCommand(self, command, wait=True, run=False):
        print(color.END + color.BOLD + "# [shell command]:" + color.END)
        self.printBar()
        for line in command.splitlines():
            if self.isEmpty(line):
                continue

            print(color.END + color.BOLD + color.BLUE + "| " + color.END + color.GREEN + color.BOLD + "$> " + color.END, end="")
            print(highlight(line, BashLexer(), Terminal256Formatter()), end="")
        self.printBar()
        if run:
            print(color.END + color.BOLD +
                  "# [shell command] Result:" + color.END)
            os.system(command)
        
        if wait:
            self.AskEnter()

    def PrintResult(self, msg):
        print(color.END + color.CYAN + "# Result: {}".format(msg) + color.END)

    def AskEnter(self):
        key = input(color.END + color.PURPLE + color.BOLD + "# [{0}] ".format(self._teacher) +
              color.END + color.BOLD + pressEnterMessages[random.randint(0, len(pressEnterMessages)-1)] + color.END)
        
        if key is not None and key != "":
            key = key.lower()

        if key == "q":
            self.Speak("Espero que você volte logo...")
            exit()
        
        if key == "f":
            self.SetFastMode(True)
            self.Speak(f"Modo rápido ativado... tá com pressa {self._student}?")

        if key == "s":
            self.SetFastMode(False)
            self.Speak("Modo rápido desativado... melhor ir devagar né?")

    def NextStep(self):
        self.Speak(nextStepMessages[random.randint(
            0, len(nextStepMessages)-1)])
        self.AskEnter()
