# see: https://toptechboy.com/9-axis-imu-lesson-19-vpython-visualization-of-pitch-and-yaw/
import vpython as vp
import time
import numpy as np
import serial

vp.scene.range=5
toRad=2*np.pi/360
toDeg=1/toRad
vp.scene.forward=vp.vector(-1,-1,-1)

vp.scene.width=600
vp.scene.height=600

xarrow=vp.arrow(length=2, shaftwidth=.1, color=vp.color.red, axis=vp.vector(1,0,0))
yarrow=vp.arrow(length=2, shaftwidth=.1, color=vp.color.green, axis=vp.vector(0,1,0))
zarrow=vp.arrow(length=4, shaftwidth=.1, color=vp.color.blue, axis=vp.vector(0,0,1))

frontarrow=vp.arrow(length=4, shaftwidth=.1, color=vp.color.purple, axis=vp.vector(1,0,0))
uparrow=vp.arrow(length=1, shaftwidth=.1, color=vp.color.magenta, axis=vp.vector(0,1,0))
sidearrow=vp.arrow(length=2, shaftwidth=.1, color=vp.color.orange, axis=vp.vector(0,0,1))

# bBoard=vp.box(length=6,width=2,height=.2,opacity=.8, pos=vp.vector(0,0,0,))
# bn=vp.box(length=1,width=.75,height=.1, pos=vp.vector(-.5,.1+.05,0), color=vp.color.blue)
# nano=vp.box(lenght=1.75,width=.6,height=.1, pos=vp.vector(-2,.1+.05,0), color=vp.color.green)
# myObj=vp.compound([bBoard,bn,nano])
# myObj=vp.compound([bBoard])


with serial.Serial('com2',115200) as ad:
    time.sleep(1)
    while (True):
        while (ad.inWaiting()==0):
            pass
        dataPacket=ad.readline()
        dataPacket=str(dataPacket,'utf-8')
        splitPacket=dataPacket.split(",")
        roll=float(splitPacket[2])*toRad+np.pi/2
        pitch=float(splitPacket[1])*toRad
        yaw=float(splitPacket[0])*toRad+0*np.pi

        print("Roll=",roll*toDeg," Pitch=",pitch*toDeg,"Yaw=",yaw*toDeg)
        vp.rate(200)

        k=vp.vector(-vp.cos(yaw)*vp.sin(pitch)*vp.sin(roll)-vp.sin(yaw)*vp.cos(roll),
                    -vp.sin(yaw)*vp.sin(pitch)*vp.sin(roll)+vp.cos(yaw)*vp.cos(roll),
                    vp.cos(pitch)*vp.sin(roll))

        y=vp.vector(0,1,0)
        s=vp.cross(k,y)
        v=vp.cross(s,k)

        frontarrow.axis=k
        sidearrow.axis=s
        uparrow.axis=v
        # myObj.axis=k
        # myObj.up=v
        sidearrow.length=2
        frontarrow.length=4
        uparrow.length=1