"""
    Copyright (C) 2016 Wojciech Kuprianowicz

    This file is a part of Simple Queueing System Simulator (SQSS).

    SQSS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SQSS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SQSS. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy
from generator import Generator

class OnOffGenerator(Generator):

    def __init__(self, lamb, onAverageTime, offAverageTime, initialState = 1):
        Generator.__init__(self)
        self.lamb = lamb
        self.averageTime = [offAverageTime, onAverageTime]
        self.initialState = initialState
        self.failSafeCounterMax = 100

    def reset(self, currentTime):
        Generator.reset(self)
        self.currentState = self.initialState
        self.currentStateEnd = currentTime + numpy.random.exponential(self.averageTime[self.currentState])
        self.computeNextRequestArrival(currentTime)

    def computeNextRequestArrival(self, currentTime):
        Generator.computeNextRequestArrival(self, currentTime)
        self.nextRequestArrival = currentTime + numpy.random.exponential(1.0 / self.lamb)
        self.failSafeCounter = 0
        while True:
            if self.currentState == 0:
                if self.nextRequestArrival < self.currentStateEnd:
                    self.nextRequestArrival += numpy.random.exponential(1.0 / self.lamb)
                    continue
                else:
                    self.currentState = 1
                    self.currentStateEnd += numpy.random.exponential(self.averageTime[self.currentState])
            else: #self.currentState == 1:
                if self.nextRequestArrival < self.currentStateEnd:
                    break
                else:
                    self.failSafeCounter += 1
                    if self.failSafeCounter == self.failSafeCounterMax:
                        raise Exception("Simulation seems to have entered a loop. Likely culprit: both lambda and t_on are small.")
                    self.currentState = 0
                    self.currentStateEnd += numpy.random.exponential(self.averageTime[self.currentState])

