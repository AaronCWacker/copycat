from .coderack import Coderack
from .randomness import Randomness
from .slipnet import Slipnet
from .temperature import Temperature
from .workspace import Workspace
from .gui import GUI


class Reporter(object):
    """Do-nothing base class for defining new reporter types"""
    def report_answer(self, answer):
        pass

    def report_coderack(self, coderack):
        pass

    def report_slipnet(self, slipnet):
        pass

    def report_temperature(self, temperature):
        pass

    def report_workspace(self, workspace):
        pass


class Copycat(object):
    def __init__(self, rng_seed=None, reporter=None, showgui=True):
        self.coderack = Coderack(self)
        self.random = Randomness(rng_seed)
        self.slipnet = Slipnet()
        self.temperature = Temperature()
        self.workspace = Workspace(self)
        self.reporter = reporter or Reporter()
        self.gui = GUI('Copycat')
        self.lastUpdate = float('-inf')

    def step(self):
        self.coderack.chooseAndRunCodelet()
        self.reporter.report_coderack(self.coderack)
        self.reporter.report_temperature(self.temperature)
        self.reporter.report_workspace(self.workspace)

    def update_workspace(self, currentTime):
        self.workspace.updateEverything()
        self.coderack.updateCodelets()
        self.slipnet.update(self.random)
        self.temperature.update(self.workspace.getUpdatedTemperature())
        self.lastUpdate = currentTime
        self.reporter.report_slipnet(self.slipnet)

    def check_reset(self):
        if self.gui.app.primary.control.go:
            initial, modified, target = self.gui.app.primary.control.get_vars()
            self.reset_with_strings(initial, modified, target)
            return True
        else:
            return False

    def reset_with_strings(self, initial, modified, target):
        self.workspace.resetWithStrings(initial, modified, target)
        self.gui.app.reset_with_strings(initial, modified, target)

    def mainLoop(self):
        currentTime = self.coderack.codeletsRun
        self.temperature.tryUnclamp(currentTime)
        # Every 15 codelets, we update the workspace.
        if currentTime >= self.lastUpdate + 15:
            self.update_workspace(currentTime)
        self.step()


    def runTrial(self):
        """Run a trial of the copycat algorithm"""
        self.coderack.reset()
        self.slipnet.reset()
        self.temperature.reset()
        self.workspace.reset()
        while self.workspace.finalAnswer is None:
            self.mainLoop()
        answer = {
            'answer': self.workspace.finalAnswer,
            'temp': self.temperature.last_unclamped_value,
            'time': self.coderack.codeletsRun,
        }
        self.reporter.report_answer(answer)
        return answer

    def runGUI(self):
        while not self.check_reset():
            self.gui.update(self)
            self.gui.refresh()
        answers = {}
        while True:
            if self.check_reset():
                answers = {}
            answer = self.runTrial()
            self.gui.refresh()
            self.gui.update(self)
            d = answers.setdefault(answer['answer'], {
                'count': 0,
                'sumtemp': 0,
                'sumtime': 0
            })
            d['count'] += 1
            d['sumtemp'] += answer['temp']
            d['sumtime'] += answer['time']
            self.gui.add_answers(answers)

        for answer, d in answers.items():
            d['avgtemp'] = d.pop('sumtemp') / d['count']
            d['avgtime'] = d.pop('sumtime') / d['count']

    def run(self, initial, modified, target, iterations):
        self.reset_with_strings(initial, modified, target)
        answers = {}
        for i in range(iterations):
            if self.check_reset():
                answers = {}
            answer = self.runTrial()
            d = answers.setdefault(answer['answer'], {
                'count': 0,
                'sumtemp': 0,
                'sumtime': 0
            })
            d['count'] += 1
            d['sumtemp'] += answer['temp']
            d['sumtime'] += answer['time']

        for answer, d in answers.items():
            d['avgtemp'] = d.pop('sumtemp') / d['count']
            d['avgtime'] = d.pop('sumtime') / d['count']
        return answers

    def run_forever(self, initial, modified, target):
        self.reset_with_strings(initial, modified, target)
        while True:
            self.check_reset()
            self.runTrial()
