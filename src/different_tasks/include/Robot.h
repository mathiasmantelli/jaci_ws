#ifndef ROBOT_H
#define ROBOT_H

#include <vector> 
#include "Misc.h"

class Robot{
public:
    Robot();
    ~Robot();

    void initialize(ConnectionMode cmode, LogReport lmode, std::string name);
    void run();
    bool isRunning();

    
protected:
    bool ready_;
    bool running_;
};

#endif // ROBOT_H