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

from request import Request
from poisson_generator import PoissonGenerator
from onoff_generator import OnOffGenerator
from bucket import Bucket
from queue_wrapper import QueueWrapper
from simulation import Simulation

class MiniTester:

    def runTests(self):
        self.testPoissonGenerator()
        self.testPBAndDIncreaseWithLambda()

    def testPoissonGenerator(self):
        print "======= TEST: Poisson Generator ======="
        lambdas = [1, 2, 4, 5, 10, 20, 40, 80, 100]
        for lamb in lambdas:
            gen = PoissonGenerator(lamb)
            gen.reset(0.0)
            for i in xrange(1, 999):
                gen.computeNextRequestArrival(gen.nextRequestArrival)
            print "Lambda = " + str(lamb) + " => average time between requests = " + str(gen.nextRequestArrival / 1000)
        print "======================================="

    def testPBAndDIncreaseWithLambda(self):
        print "======= TEST: PB and D increase when lambda increases ======="
        lambdas = [10, 20, 40, 80, 100]
        for lamb in lambdas:
            print "Lambda = " + str(lamb)
            sim = Simulation(0, 3, 1000, 20, 5, 30, "poisson", lamb, 0, 0)
            sim.simulate()
            print ""
        print "============================================================="


if __name__ == '__main__':
    mt = MiniTester()
    mt.runTests()

