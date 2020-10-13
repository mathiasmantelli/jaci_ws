#include "../include/Robot.h"
#include <GL/glut.h>
#include <cmath>
#include <iostream>

Robot::Robot(){
    ready_ = false;
    running_ = true; 
}

Robot::~Robot(){

}

void Robot::initialize(ConnectionMode cmode, LogReport lmode, std::string fname){

}

void Robot::run(){

}

bool Robot::isRunning(){
    return running_;
}
