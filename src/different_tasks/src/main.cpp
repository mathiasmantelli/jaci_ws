#include <pthread.h>
#include <iostream>
#include "../include/Misc.h"
#include "../include/Robot.h"
#include "../include/GlutClass.h"

using namespace std; 

ConnectionMode theConnection;
LogReport theLog;
MotionMode theMotion;
MovingDirection theMoving;
GraphicalMode theGraphical;
MappingMode theMapping;
/*
enum ConnectionMode {SIMULATION, WIFI};
enum LogReport {WRITING, READING, NONE};
enum MotionMode {WALLFOLLOWING};
enum MovingDirection {FORWARD, BACKWARD, LEFT, RIGHT, STOP};
enum GraphicalMode {ACTIVATE, DEACTIVATE};
*/

pthread_mutex_t* mutex;
std::string filename = ""; 
void* startRobotThread(void* ref){
    Robot* robot = (Robot*) ref; 

    robot->initialize(theConnection, theLog, filename);

    while(robot->isRunning())
        robot->run();

    return 0;
}

void* startGlutThread(void* ref){
    GlutClass* glut = GlutClass::getInstance();
    glut->setRobot((Robot*) ref);

    glut->initialize();

    glut->process();

    return NULL;
}

int main(int argc, char* argv[]){
	theConnection = SIMULATION; 
    theLog = NONE;
    theMotion = WALLFOLLOWING; 
    theMapping = HIMM;
    theGraphical = ACTIVATE;

    cout << "The chosen configuration is: ";
    if(argc > 1){
        if(!strncmp(argv[1], "sim", 3)){
            theConnection = SIMULATION;
            cout << " SIMULATION,";
        }else if(!strncmp(argv[1], "wifi", 4)){
            theConnection = WIFI;
            cout << " WIFI,";
        }
    }

    if(argc > 2){
        if(!strncmp(argv[2], "write", 4)){
            theLog = WRITING;
            cout << " WRITE THE LOG,";
        }else if(!strncmp(argv[2], "read", 4)){
            theLog = READING;
            cout << " READ THE LOG,";
        }else if(!strncmp(argv[2], "none", 4)){
            theLog = NONE;
            cout << " NO LOG,";        
        }    
    }

    if(argc > 3){
        if(!strncmp(argv[3], "wall", 4)){
            theMotion = WALLFOLLOWING;   
            cout << " WALLFOLLOWING,";
        } 
    }   

    if(argc > 4){
        if(!strncmp(argv[4], "himm", 4)){
            theMapping = HIMM;
            cout << " HIMM,";
        }else if(!strncmp(argv[4], "bayes", 5)){
            theMapping = BAYES;
            cout << " BAYES,";
        }
    } 

    if(argc > 5){
        if(!strncmp(argv[5], "show", 4)){
            theGraphical = ACTIVATE;
            cout << " SHOW.";
        }else if(!strncmp(argv[5], "quiet", 5)){
            theGraphical = DEACTIVATE;
            cout << " QUIET.";
        }
    }
    cout << endl;

    Robot* r; 
    r = new Robot();

    pthread_t robotThread, glutThread; 
    mutex = new pthread_mutex_t;
    pthread_mutex_unlock(mutex);

    pthread_create(&(robotThread), NULL, startRobotThread,(void*)r);
    pthread_create(&(glutThread), NULL, startGlutThread, (void*)r);

    pthread_join(robotThread, 0);
    pthread_join(glutThread, 0);

    return 0;
}
