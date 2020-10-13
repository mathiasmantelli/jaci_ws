#ifndef MISC_H
#define MISC_H


#include <sys/time.h>
#include <fstream>
#include <iostream>
#include <cmath>
#include <vector>
#include <string.h> 


enum ConnectionMode {SIMULATION, WIFI};
enum LogReport {WRITING, READING, NONE};
enum MotionMode {WALLFOLLOWING};
enum MovingDirection {FORWARD, BACKWARD, LEFT, RIGHT, STOP};
enum GraphicalMode {ACTIVATE, DEACTIVATE};
enum MappingMode {HIMM, BAYES};

#define DEG2RAD(x) x*M_PI/180.0
#define RAD2DEG(x) x*180.0/M_PI

class Pose{
	public: 
		Pose(); 
		Pose(float a, float b, float c);
		float x, y, theta;
};

#endif // MISC_H