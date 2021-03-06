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

class PoissonGenerator(Generator):

    def __init__(self, lamb):
        Generator.__init__(self)
        self.lamb = lamb

    def reset(self, currentTime):
        Generator.reset(self)
        self.computeNextRequestArrival(currentTime)

    def computeNextRequestArrival(self, currentTime):
        Generator.computeNextRequestArrival(self, currentTime)
        self.nextRequestArrival = currentTime + numpy.random.exponential(1.0 / self.lamb)

