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

import subprocess
import os
import sys

def run(scenario_name):
    f = open("scenarios/" + scenario_name + ".txt", "r")
    out_d = open("scenarios/" + scenario_name + "_d.txt", "w")
    out_pb = open("scenarios/" + scenario_name + "_pb.txt", "w")

    commonParams = next(f)

    for line in f:
        cmd = "python simulation.py --debug 0 " + commonParams[:-1] + " " + line
        print "Running: " + cmd
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n')

        for l in result:
            if l.startswith("D = "):
                out_d.write(l.replace("D = ", ""))
                out_d.write(os.linesep) 
            if l.startswith("PB = "):
                out_pb.write(l.replace("PB = ", ""))
                out_pb.write(os.linesep) 

    f.close()
    out_d.close()
    out_pb.close()

    print "Results for " + f.name + ":\n" + out_d.name + "\n" + out_pb.name


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Proper use: python run_scenario.py SCENARIO_NAME\nwhere SCENARIO_NAME is a text file placed in the scenario subdir.\n\nEXAMPLE: python run_scenario.py scenario_0"
        sys.exit()
    run(sys.argv[1])
