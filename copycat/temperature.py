import math


class Temperature(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.actual_value = 100.0
        self.last_unclamped_value = 100.0
        self.clamped = True
        self.clampTime = 30

    def update(self, value):
        self.last_unclamped_value = value
        if self.clamped:
            self.actual_value = 100.0
        else:
            self.actual_value = value

    def clampUntil(self, when):
        self.clamped = True
        self.clampTime = when
        # but do not modify self.actual_value until someone calls update()

    def tryUnclamp(self, currentTime):
        if self.clamped and currentTime >= self.clampTime:
            self.clamped = False

    def value(self):
        return 100.0 if self.clamped else self.actual_value

    def getAdjustedValue(self, value):
        return value ** (((100.0 - self.value()) / 30.0) + 0.5)

    """
    def getAdjustedProbability(self, value):
        if value == 0 or value == 0.5 or self.value() == 0:
            return value
        if value < 0.5:
            return 1.0 - self.getAdjustedProbability(1.0 - value)
        coldness = 100.0 - self.value()
        a = math.sqrt(coldness)
        c = (10 - a) / 100
        f = (c + 1) * value
        return max(f, 0.5)
    """

    def getAdjustedProbability(self, value):
        """
        This function returns the probability for a decision.
        Copied above.

        Please look at the last line of it.  Strangely, it was
        return max(f, 0.5).  Does that make sense? Let's compare
        some results.  Where it was (0.5), we obtained, for example:

        iiijjjlll: 670 (avg time 1108.5, avg temp 23.6)
        iiijjjd: 2 (avg time 1156.0, avg temp 35.0)
        iiijjjkkl: 315 (avg time 1194.4, avg temp 35.5)
        iiijjjkll: 8 (avg time 2096.8, avg temp 44.1)
        iiijjjkkd: 5 (avg time 837.2, avg temp 48.0)

        wyz: 5 (avg time 2275.2, avg temp 14.9)
        xyd: 982 (avg time 2794.4, avg temp 17.5)
        yyz: 7 (avg time 2731.9, avg temp 25.1)
        dyz: 2 (avg time 3320.0, avg temp 27.1)
        xyy: 2 (avg time 4084.5, avg temp 31.1)
        xyz: 2 (avg time 1873.5, avg temp 52.1)

        Now, let's see what return max(f, 0.0000) does:

        wyz: 7 (avg time 3192.9, avg temp 13.1)
        xyd: 985 (avg time 2849.1, avg temp 17.5)
        yyz: 6 (avg time 3836.7, avg temp 18.6)
        xyy: 1 (avg time 1421.0, avg temp 19.5)
        xyz: 1 (avg time 7350.0, avg temp 48.3)

        They *seem* better (in the strict sense that we've obtained both
        lower T and more times of wyz.)  But they're *not* statistically
        significant (for 1000 runs).

        Now... looking at the code... it seems to be a mess... what does
        function f() even mean in intuitive terms?

        Work it does, but dude... quite a hack.

        Another run, with return f @line89:

        wyz: 8 (avg time 4140.5, avg temp 13.3)
        yyz: 6 (avg time 2905.2, avg temp 14.5)
        xyd: 982 (avg time 3025.4, avg temp 17.6)
        dyz: 4 (avg time 4265.0, avg temp 17.7)

        Does it even matter? Another (quick) run, I think with return (0.5):

        dyz: 1 (avg time 5198.0, avg temp 15.3)
        wyz: 3 (avg time 4043.7, avg temp 17.1)
        yyz: 9 (avg time 3373.6, avg temp 21.0)
        xyd: 84 (avg time 5011.1, avg temp 23.3)
        xyy: 3 (avg time 4752.0, avg temp 27.9)

        Compared to return(0.99):

        xyd: 1000 (avg time 1625.2, avg temp 17.3)

        Comparing to return f --> Statistically significant.
        Comparing to return(0.5) --> same, so this return value does something.

        Now running return(0.0):

        xyz: 3 (avg time 3996.7, avg temp 81.1)
        dyz: 46 (avg time 5931.7, avg temp 82.6)
        xd: 17 (avg time 6090.3, avg temp 83.8)
        xyd: 934 (avg time 7699.8, avg temp 88.1)

        It's bad overall, but at least it's statistically significant!
        """
        if value == 0 or value == 0.5 or self.value() == 0:
            return value
        if value < 0.5:
            return 1.0 - self.getAdjustedProbability(1.0 - value)
        coldness = 100.0 - self.value()
        a = math.sqrt(coldness)
        c = (10 - a) / 100
        f = (c + 1) * value
        return (0.0)  # f  # max(f, 0.0000)
