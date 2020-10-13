#include "../include/Robot.h"
#include "../include/Misc.h"

class GlutClass{
public: 
    static GlutClass* getInstance();

    void initialize();
    void process();
    void terminate();
    void setRobot(Robot* r);

private:
    GlutClass();
    static GlutClass* instance; 
    Robot* robot_; 


};