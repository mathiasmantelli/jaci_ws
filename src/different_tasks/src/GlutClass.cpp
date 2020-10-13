#include <GL/glut.h>
#include <FreeImage.h>
#include <iomanip>
#include <sstream>
#include <iostream>
#include <cmath>
#include <unistd.h>
#include "../include/GlutClass.h"

GlutClass::GlutClass(){

}

GlutClass* GlutClass::instance = 0;

GlutClass* GlutClass::getInstance(){
    if(instance == 0)
        instance = new GlutClass;
    return instance;
}

void GlutClass::initialize(){

}

void GlutClass::process(){

}

void GlutClass::setRobot(Robot* r){
    
}

