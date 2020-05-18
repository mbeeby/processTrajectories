#!/usr/bin/python

from optparse import OptionParser
import sys
import math
import numpy

class timeClass:
    def __init__(self):
        self.x_um    = 0
        self.y_um    = 0
        self.z_um    = 0
        self.m0      = 0
        self.m1      = 0
        self.m2      = 0
        self.m3      = 0
        self.m4      = 0
        self.NPscore = 0

    def getDistance(self,otherTimePoint):
        x = self.x_um - otherTimePoint.x_um
        y = self.y_um - otherTimePoint.y_um

        dist = numpy.sqrt((x*x)+(y*y))

        return dist

class trajectoryClass:
    def __init__(self):
        self.times = {}

    def netDisplacement(self):
        maxDist = 0
        for timePoint1 in self.times:
            for timePoint2 in self.times:
                dist = self.times[timePoint1].getDistance(self.times[timePoint2])
                if dist > maxDist:
                    maxDist = dist
        return maxDist

def sqr(x):
    return x*x

def getDist(time1, time2):
    return math.sqrt(sqr(time1.x_um - time2.x_um) + sqr(time1.y_um - time2.y_um))

class trajectoriesClass:
    def __init__(self):
        self.trajectories = {}

    def load(self,csvFilename, pixelSize_um, framesPerSec):
        csvFile = open(csvFilename, 'r')
        header  = csvFile.readline()
        lines   = csvFile.readlines()
        for line in lines:
            data = line.split(",")
            number     = int(data[0])
            Trajectory = int(data[1])
            time_s     = float(data[2]) / framesPerSec

            if not (Trajectory in self.trajectories):
                self.trajectories[Trajectory] = trajectoryClass()
            self.trajectories[Trajectory].times[time_s] = timeClass()

            self.trajectories[Trajectory].times[time_s].x_um    = float(data[3]) * pixelSize_um
            self.trajectories[Trajectory].times[time_s].y_um    = float(data[4]) * pixelSize_um
            self.trajectories[Trajectory].times[time_s].z_um    = float(data[5]) * pixelSize_um
            self.trajectories[Trajectory].times[time_s].m0      = float(data[6])
            self.trajectories[Trajectory].times[time_s].m1      = float(data[7])
            self.trajectories[Trajectory].times[time_s].m2      = float(data[8])
            self.trajectories[Trajectory].times[time_s].m3      = float(data[9])
            self.trajectories[Trajectory].times[time_s].m4      = float(data[10])
            self.trajectories[Trajectory].times[time_s].NPscore = float(data[11])

    def outputStats(self):
        output = ""
        velocities = []
        durations  = []
        if len(self.trajectories) > 2:
            output = output + "Trajectory_ref\tNum.timepoints\tVelocity(um/sec)\tMax net displacment (um)\n"
            trajectoryCount = 0
            for trajectory in self.trajectories:
                trajectoryCount += 1
                sortedTimes = sorted(self.trajectories[trajectory].times.keys())
   
                # To get length: iterate through all but last timepoint
                dist = 0
                time = 0

                for timeCount in range(len(sortedTimes)-1):
                    curTime  = sortedTimes[timeCount]
                    nextTime = sortedTimes[timeCount+1]
                    dist += getDist(self.trajectories[trajectory].times[curTime], self.trajectories[trajectory].times[nextTime])
                    time += (nextTime - curTime)
                velocity = dist/time
                velocities.append(velocity)
                durations.append(time)
                netDisplacement = self.trajectories[trajectory].netDisplacement() 
                output = output + str(trajectory) + "\t" + str(len(self.trajectories[trajectory].times))+ "\t" + str(velocity)+"\t"+str(netDisplacement)+"\n"

            sys.stdout.write("Mean velocity (um/sec)\t"  + str(numpy.mean(velocities))   + "\n")
            sys.stdout.write("Median velocity (um/sec)\t"+ str(numpy.median(velocities)) + "\n")
            sys.stdout.write("Std.dev. velocity (um/sec)\t"+ str(numpy.std(velocities)) + "\n")
            sys.stdout.write("Maximum velocity (um/sec)\t"+ str(numpy.amax(velocities)) + "\n")
            sys.stdout.write("Minimum velocity (um/sec)\t"+ str(numpy.amin(velocities)) + "\n")
            sys.stdout.write("-------\n")
  
            sys.stdout.write("Total trajectories\t"+ str(trajectoryCount) + "\n")
            sys.stdout.write("Mean trajectory duration (sec)\t"  + str(numpy.mean(durations))   + "\n")
            sys.stdout.write("Median trajectory durationvelocity (sec)\t"+ str(numpy.median(durations)) + "\n")
            sys.stdout.write("Std.dev. trajectory durationvelocity (sec)\t"+ str(numpy.std(durations)) + "\n")
            sys.stdout.write("Maximum trajectory durationvelocity (sec)\t"+ str(numpy.amax(durations)) + "\n")
            sys.stdout.write("Minimum trajectory durationvelocity (sec)\t"+ str(numpy.amin(durations)) + "\n")

            sys.stdout.write("-------\n")
            sys.stdout.write(output)
        else:
            sys.stdout.write("Only "+str(len(self.trajectories))+" trajectories, so cannot calculate stats!\n")

def main():
    parser = OptionParser("usage: %prog <csv filename> <pixel size, um> <frames per s>")
    parser.add_option("-t", "--threshold", action="store", type="int", dest="threshold", default=False, help="Minimum number of timepoints to use a trajectory")
    (options,args) = parser.parse_args()

    if len(args) != 3:
        parser.error("Incorrect number of arguments! ("+str(len(args))+": "+", ".join(args)+")")
    csvFilename  = args[0]
    pixelSize_um = float(args[1])
    framesPerSec = float(args[2])

    trajectories = trajectoriesClass()
    trajectories.load(csvFilename, pixelSize_um, framesPerSec)

    if options.threshold:
        tempTrajectories = trajectoriesClass()
        for trajectory in trajectories.trajectories:
            if len(trajectories.trajectories[trajectory].times) >= options.threshold:
                tempTrajectories.trajectories[trajectory] = trajectories.trajectories[trajectory]
        trajectories = tempTrajectories

    trajectories.outputStats()

main()


#  ,Trajectory,Frame,x,y,z,m0,m1,m2,m3,m4,NPscore
# 1,1,0,452.568,2.484,0,4.208,2.083,5.315,15.293,48.155,9.374
# 2,1,2,452.529,2.466,0,4.200,2.088,5.350,15.466,48.951,0.629
# 3,1,5,452.612,2.452,0,4.115,2.062,5.213,14.871,46.483,1.415
# 4,1,7,452.468,2.489,0,4.220,2.094,5.371,15.535,49.172,0.213
# 5,1,12,452.432,2.538,0,4.315,2.136,5.600,16.581,53.750,3.517
# 6,2,0,74.801,27.209,0,7.487,2.687,8.682,31.131,119.765,44.834
# 7,2,1,76.636,26.225,0,7.646,2.755,9.129,33.574,132.359,16.126
# 8,2,2,79.131,23.744,0,7.362,2.726,8.996,33.030,130.168,20.842
# 9,2,3,80.358,22.256,0,7.369,2.690,8.700,31.229,120.300,38.893
