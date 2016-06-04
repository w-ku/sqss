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

import Queue
import logging

class QueueWrapper:

    def __init__(self, size):
        if type(size) is str and size == "INF":
            self.type = "INF"
            self.queue = Queue.Queue()
        else:
            if size == 0:
                self.type = "NoQueue"
            else:
                self.type = "FIN"
                self.maxSize = size
                self.queue = Queue.Queue(size)

    def reset(self):
        logging.debug("Queue: Reset. Queue's type is %s.", self.type)
        if self.type == "NoQueue":
            return
        while not self.queue.empty():
            self.queue.get()

    def noRequests(self):
        return self.type == "NoQueue" or self.queue.empty()

    def addRequest(self, req):
        if self.type == "NoQueue":
            logging.debug("Queue: Request %d not added, because no queue exist.", req.id)
            return False
        if self.type == "INF":
            self.queue.put(req)
            logging.debug("Queue: Request %d added, there are %d / INF requests in the queue.", req.id, self.queue.qsize())
            return True
        if self.queue.full():
            logging.debug("Queue: Request %d not added, there are %d / %d requests in the queue.", req.id, self.queue.qsize(), self.maxSize)
            return False
        self.queue.put(req)
        logging.debug("Queue: Request %d added, there are %d / %d requests in the queue.", req.id, self.queue.qsize(), self.maxSize)
        return True

    def getRequest(self):
        if self.noRequests():
            return None
        return self.queue.get()

