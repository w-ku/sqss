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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import optparse
import sys
import logging

from request import Request
from poisson_generator import PoissonGenerator
from onoff_generator import OnOffGenerator
from bucket import Bucket
from queue_wrapper import QueueWrapper


class Simulation:

    def __init__(self, debug, samples, requiredAccQty, queueSize, tokenArrivalSpeed, bucketCapacity, generatorType, lamb, tOn, tOff):
        self.debug = debug
        self.samples = samples
        self.requiredAccQty = requiredAccQty
        self.bucket = Bucket(tokenArrivalSpeed, bucketCapacity, bucketCapacity)
        if generatorType == "poisson":
            self.generator = PoissonGenerator(lamb)
        elif generatorType == "onoff":
            self.generator = OnOffGenerator(lamb, tOn, tOff)
        self.queue = QueueWrapper(queueSize)

    def acceptRequest(self, req):
        req.acceptanceTime = self.currentTime
        self.accQty += 1
        self.accTotalWaitTime += req.waitTime()
        logging.debug("Request %d accepted at %f. It waited %f.", req.id, self.currentTime, req.waitTime())

    def rejectRequest(self, req):
        self.rejQty += 1
        logging.debug("Request %d rejected at %f.", req.id, self.currentTime)

    def simulate(self):
        self.samplesTotalAverageWaitTime = 0.0
        self.samplesTotalRejectedRatio = 0.0
        for sample in xrange(0, self.samples):
            logging.debug("Starting the simulation: %d out of %d samples.", sample + 1, self.samples)
            self.currentTime = 0.0
            self.generator.reset(self.currentTime)
            self.bucket.reset(self.currentTime)
            self.queue.reset()
            self.accQty = 0
            self.rejQty = 0
            self.accTotalWaitTime = 0.0
            while self.accQty < self.requiredAccQty:
                self.performStep()
                if self.debug:
                    sys.stdin.read(1)
            self.samplesTotalAverageWaitTime += (self.accTotalWaitTime / self.accQty)
            self.samplesTotalRejectedRatio += (1.0 * self.rejQty / (self.rejQty + self.accQty))
            logging.debug("Sample %d results: D = %f, PB = %f", sample, (self.accTotalWaitTime / self.accQty), (1.0 * self.rejQty / (self.rejQty + self.accQty)))
        print "D = " + str(self.samplesTotalAverageWaitTime / self.samples)
        print "PB = " + str(self.samplesTotalRejectedRatio / self.samples)

    def performStep(self):
        if self.generator.nextRequestArrival < self.bucket.nextTokenArrival:
            self.currentTime = self.generator.nextRequestArrival
            req = self.generator.generateRequest(self.currentTime)
            logging.debug("A new request %d arrived at %f.", req.id, self.currentTime)
            if self.queue.type == "NoQueue":
                if self.bucket.getToken():
                    self.acceptRequest(req)
                else:
                    self.rejectRequest(req)
            elif not self.queue.addRequest(req):
                self.rejectRequest(req)
        else:
            self.currentTime = self.bucket.nextTokenArrival
            self.bucket.addToken(self.currentTime)
        while not self.queue.noRequests():
            if self.bucket.getToken():
                req = self.queue.getRequest()
                self.acceptRequest(req)
            else:
                break


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--debug",   type = "int",    default = 0)
    parser.add_option("--samples", type = "int",    default = 1)
    parser.add_option("--accqty",  type = "int",    default = 1000)
    parser.add_option("--lq",      type = "string", default = "100")
    parser.add_option("--lz",      type = "int",    default = 40)
    parser.add_option("--vz",      type = "int",    default = 5)
    parser.add_option("--gentype", type = "string", default = "poisson")
    parser.add_option("--lamb",    type = "int",    default = 15)
    parser.add_option("--ton",     type = "int",    default = 10)
    parser.add_option("--toff",    type = "int",    default = 20)
    opt, rmd = parser.parse_args()
    if opt.lq != "INF":
        opt.lq = int(opt.lq)
    if opt.debug:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    logging.debug("Passed params: %s", opt.__dict__)

    sim = Simulation(opt.debug, opt.samples, opt.accqty, opt.lq, opt.vz, opt.lz, opt.gentype, opt.lamb, opt.ton, opt.toff)
    sim.simulate()

