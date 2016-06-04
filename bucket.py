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

class Bucket:

    def __init__(self, speed, capacity, initialTokenQuantity):
        self.speed = speed
        self.capacity = capacity
        self.initialTokenQuantity = initialTokenQuantity

    def reset(self, currentTime):
        self.tokenNumber = self.initialTokenQuantity
        self.computeNextTokenArrival(currentTime)

    def computeNextTokenArrival(self, currentTime):
        self.nextTokenArrival = currentTime + 1.0 / self.speed

    def addToken(self, currentTime):
        self.tokenNumber = min(self.capacity, self.tokenNumber + 1)
        self.computeNextTokenArrival(currentTime)

    def getToken(self):
        if self.tokenNumber == 0:
            return False
        self.tokenNumber -= 1
        return True

