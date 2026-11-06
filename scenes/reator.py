"""Cena: sala do reator R-2 (onde o acidente aconteceu)."""
import answers
import ids
import lessons
import ui
import art
from engine import Action, Scene, lacks, simple_action, travel_action

WRONG_ANSWER_PENALTY = 6

DESCRIPTION = """
A sala está enegrecida. No centro, o reator R-2, com o disco de ruptura estourado. Num canto, um painel de controle com um LED vermelho: EXAUSTÃO OFF. Um jaleco branco está pendurado num gancho, ao lado de uma válvula de emergência.
"""


def examine_reactor(game):
    game.state.add(ids.REACTOR_SEEN)
    ui.narrate("O metal ainda emana calor. Marcas de queimadura e resíduos de um líquido viscoso cobrem o chão. Algo deu muito errado aqui.")
    game.remember("acidente")
    ui.lesson(lessons.RUNAWAY)


def use_panel(game):
    state = game.state
    if state.has(ids.VENTILATION):
        ui.success("O LED está verde e a exaustão ronca em segundo plano.")
        return
    ui.narrate('O painel exibe: "EXAUSTÃO DESLIGADA. Para o protocolo de purga, informe a massa molar do polietileno do lote em teste (g/mol)."')
    if not state.has(ids.WHITEBOARD):
        ui.info("Você não lembra de que lote se trata. O registro do lote deve estar anotado em algum lugar do laboratório.")
    raw = ui.prompt("Massa molar em g/mol (ENTER para desistir)")
    if not raw:
        game.free()
        return
    if raw.replace(".", "").isdigit() and int(raw.replace(".", "")) == answers.PE_MOLAR_MASS:
        state.add(ids.VENTILATION)
        ui.success("Bip! O LED fica verde e os exaustores rugem. O ar começa a circular.")
        ui.lesson(lessons.PANEL_SOLVED)
        return
    attempts = state.bump("panel_wrong")
    ui.danger("O painel emite um bipe de erro.")
    game.lose_time(WRONG_ANSWER_PENALTY)
    if attempts == 1:
        ui.info("Dica: calcule a massa de UMA unidade repetitiva (C2H4) e multiplique por n.")
    else:
        ui.info("Dica: C = 12 e H = 1, então C2H4 = 2 x 12 + 4 x 1 = 28 g/mol. Agora multiplique por n.")


def search_coat(game):
    game.state.add(ids.BADGE)
    ui.narrate("No bolso do jaleco, você encontra um crachá de acesso reserva do laboratório.")
    ui.item("Crachá de acesso")


def build() -> Scene:
    return Scene(
        id=ids.REACTOR,
        title="SALA DO REATOR",
        description=DESCRIPTION,
        actions=[
            Action("Examinar o reator R-2", examine_reactor, 4, lacks(ids.REACTOR_SEEN)),
            Action("Usar o painel de controle", use_panel, 3),
            Action("Revistar o jaleco pendurado", search_coat, 3, lacks(ids.BADGE)),
            simple_action(
                "Tentar fechar a válvula de emergência",
                "O metal está quente demais. Você queima a mão e a válvula nem se move. Tempo perdido.",
                cost=8),
            travel_action("Voltar ao laboratório", ids.LAB, "Você volta pelo corredor curto."),
        ],
        art=art.REATOR
    )
