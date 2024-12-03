"""
This block takes as input:
 - xArm5 IP [ROBOT_IP]
 - boolean variable indicating the presence of a component [OPCUA_GRAB] 
 - three boolean variables indicating the presence of a piece to unload [UNLOAD_{1,2,3}]
If OPCUA_GRAB is True the robot starts the pick-and-place movement,
transporting the wood piece from the Processing and Validation Station to the Sorting Station.
If UNLOAD_X is True the robot starts the unload warehouse movement,
transporting the wood piece from the Sorting Station to the conveyor.
"""

import time
import traceback
from xarm import version
from xarm.wrapper import XArmAPI

PLUS_OFFSET = 55

# xArm5 Poses (UNLOAD)
PICK_POSE = [-585,-2,177,180,0,-180]
PICK_POSE_PLUS = PICK_POSE[:]
PICK_POSE_PLUS[2] += PLUS_OFFSET

MIDDLE_POSE = [0,-325.5,207.5,180,0,-90]

PLACE_POSE = [435,4,135,180,0,6.3]
PLACE_POSE_PLUS = PLACE_POSE[:]
PLACE_POSE_PLUS[2] += PLUS_OFFSET

# xArm5 Poses (SORTING)
START_POSE = [0, -325.5, 207.5, 180, 0, -90]
START_POSE_JOINTS = [-90.0, -27.2, -31.1, 58.3, 0.0]

PICK_POSE_1 = [458.0, 255.0, 47.0, 180, 0, 90]
PICK_POSE_2 = [541.0, 255.0, 47.0, 180, 0, 90]
PICK_POSE_3 = [624.0, 255.0, 47.0, 180, 0, 90]

MIDDLE_POSE_SORTING = [325.7, 0, 200, 180, 0, 0]

PLACE_POSE_1 = [-125.9, 437.6, 1, 180, 0, 90]
PLACE_POSE_2 = [-125.9, 497.6, 1, 180, 0, 90]
PLACE_POSE_3 = [-125.9, 557.6, 1, 180, 0, 90]

# xArm5 Poses (REPLACE)
MIDDLE_POSE_REPLACE = [543.7, 159.2, 138.0, 180, 0, 90]

REPLACE_POSE_1 = [462.1, 59.0, 135.0, 180, 0, 90]
REPLACE_POSE_2 = [544.0, 59.0, 135.0, 180, 0, 90]
REPLACE_POSE_3 = [623.0, 59.0, 135.0, 180, 0, 90]


class XARM5_ROBOT:

    def __init__(self):
        self.robot_ip = ""

    def schedule(self, event_name, event_value, robot_ip, opcua_grab, unload_1, unload_2, unload_3):            

        if event_name == 'INIT':
            if not robot_ip:
                print("Error, xArm5 ip not specified")
            else:
                self.robot_ip = robot_ip
                RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
                self.arm = XArmAPI(self.robot_ip, baud_checkset=False)
                self.robot_main = RobotMain(self.arm)
                self.robot_main.config()
            return [event_value, event_value]

        elif event_name == 'READ':
            # From Validation Station to Sorting Station
            if opcua_grab:
                self.robot_main.pick_and_place() 
            # From Sorting Station to Sorting Station (Rearrange)
            elif unload_1 == 2:
                self.robot_main.unload_piece(PICK_POSE_1, MIDDLE_POSE_REPLACE, REPLACE_POSE_2)
            elif unload_1 == 3:
                self.robot_main.unload_piece(PICK_POSE_1, MIDDLE_POSE_REPLACE, REPLACE_POSE_3)
            elif unload_2 == 1:
                self.robot_main.unload_piece(PICK_POSE_2, MIDDLE_POSE_REPLACE, REPLACE_POSE_1)
            elif unload_2 == 3:
                self.robot_main.unload_piece(PICK_POSE_2, MIDDLE_POSE_REPLACE, REPLACE_POSE_3)
            elif unload_3 == 1:
                self.robot_main.unload_piece(PICK_POSE_3, MIDDLE_POSE_REPLACE, REPLACE_POSE_1)
            elif unload_3 == 2:
                self.robot_main.unload_piece(PICK_POSE_3, MIDDLE_POSE_REPLACE, REPLACE_POSE_2)
            # From Sorting Station to Conveyor
            elif unload_1 == 1:
                self.robot_main.unload_piece(PICK_POSE_1, MIDDLE_POSE_SORTING, PLACE_POSE_1)
            elif unload_2 == 2:
                self.robot_main.unload_piece(PICK_POSE_2, MIDDLE_POSE_SORTING, PLACE_POSE_2)
            elif unload_3 == 3:
                self.robot_main.unload_piece(PICK_POSE_3, MIDDLE_POSE_SORTING, PLACE_POSE_3)
                        
            return [None, event_value]
                    


class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._ignore_exit_state = False
        # SET ROBOT SPEED HERE #
        self._tcp_speed = 350     # MAX =  1000 mm/s
        self._tcp_acc = 1000      # MAX = 50000 mm/s²
        self._angle_speed = 180   # MAX =  180 degrees/s
        self._angle_acc = 500     # MAX = 1145 degrees/s²   
        # # # # # # # # # # # # #
        self._vars = {}
        self._funcs = {}
        self._robot_init()

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if not self._ignore_exit_state and data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def arm(self):
        return self._arm

    @property
    def VARS(self):
        return self._vars

    @property
    def FUNCS(self):
        return self._funcs

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._ignore_exit_state:
                return True
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False
        
    # Set Robot configurations
    def config(self):
        try:
            # Set xArm5 configurations
            code = self._arm.set_tcp_load(0.61, [0, 0, 53])
            if not self._check_code(code, 'set_tcp_load'): return

            code = self._arm.set_tcp_offset([0, 0, 126, 0, 0, 0], wait=True)
            self._arm.set_state(0)
            if not self._check_code(code, 'set_tcp_offset'): return

            time.sleep(0.5)

            code = self._arm.set_world_offset([0, 0, 0, 0, 0, 0])
            self._arm.set_state(0)
            if not self._check_code(code, 'set_world_offset'): return

            time.sleep(0.5)

            current_angle = self._arm.angles
            angle = -(current_angle[1] + current_angle[2])
            code = self._arm.set_servo_angle(servo_id=4, angle=angle)
            if not self._check_code(code, 'set_end_level'): return

            # Moving xArm5 to initial position
            self.go_to_initial_pose()

        except Exception as e:
            self.pprint('MainException: {}'.format(e))


    # Robot Main Run
    def pick_and_place(self):
        try:   
            # Moving xArm5 to initial position
            code = self._arm.set_position(*START_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
            if not self._check_code(code, 'set_position'): return

            # Picking
            code = self._arm.set_position(*PICK_POSE_PLUS, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
            if not self._check_code(code, 'set_position'): return

            code = self._arm.set_position(*PICK_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1, wait=True)
            if not self._check_code(code, 'set_position'): return

            code = self._arm.set_suction_cup(True, wait=False, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'): return

            # Check if picked
            if self._arm.arm.check_air_pump_state(1, timeout=2.0):
                print("Object picked")

                # Placing
                code = self._arm.set_position(*PICK_POSE_PLUS, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_position(*MIDDLE_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=250, wait=False)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_position(*PLACE_POSE_PLUS, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_position(*PLACE_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1, wait=True)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_suction_cup(False, wait=False, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'): return

                code = self._arm.set_position(*PLACE_POSE_PLUS, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                if not self._check_code(code, 'set_position'): return

            else:
                print("Object not picked")
                
                # Returning to initial position
                code = self._arm.set_suction_cup(False, wait=False, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'): return
                
                code = self._arm.set_position(*PICK_POSE_PLUS, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                if not self._check_code(code, 'set_position'): return

            code = self._arm.set_position(*MIDDLE_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1, wait=True)
            if not self._check_code(code, 'set_position'): return  

        except Exception as e:
            self.pprint('MainException: {}'.format(e))


    def unload_piece(self, pick_pose, middle_pose, place_pose):
        try:            
            # Start control
            if self.is_alive:
                pick_pose_plus = pick_pose[:]
                pick_pose_plus[2] += PLUS_OFFSET
                if pick_pose_plus[2] < 150:
                    pick_pose_plus[2] = 150
                place_pose_plus = place_pose[:]
                place_pose_plus[2] += PLUS_OFFSET
                # Picking
                code = self._arm.set_position(*pick_pose_plus, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_position(*pick_pose, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=True)
                if not self._check_code(code, 'set_position'): return

                code = self._arm.set_suction_cup(True, wait=False, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'): return

                # Check if picked
                if self._arm.arm.check_air_pump_state(1, timeout=2.0):
                    print("Object picked")

                    # Placing
                    code = self._arm.set_position(*pick_pose_plus, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                    if not self._check_code(code, 'set_position'): return

                    code = self._arm.set_position(*place_pose_plus, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                    if not self._check_code(code, 'set_position'): return

                    code = self._arm.set_position(*place_pose, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1, wait=True)
                    if not self._check_code(code, 'set_position'): return

                    code = self._arm.set_suction_cup(False, wait=False, delay_sec=0)
                    if not self._check_code(code, 'set_suction_cup'): return

                    code = self._arm.set_position(*place_pose_plus, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                    if not self._check_code(code, 'set_position'): return

                else:
                    print("Object not picked")
                    
                    # Returning to initial position
                    code = self._arm.set_suction_cup(False, wait=False, delay_sec=0)
                    if not self._check_code(code, 'set_suction_cup'): return
                    
                    code = self._arm.set_position(*pick_pose_plus, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=25, wait=False)
                    if not self._check_code(code, 'set_position'): return
                
                code = self._arm.set_position(*MIDDLE_POSE_SORTING, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=200, wait=False)
                if not self._check_code(code, 'set_position'): return
                
        except Exception as e:
            self.pprint('MainException: {}'.format(e))


    def go_to_initial_pose(self):
        # Moving xArm5 to initial position
        code = self._arm.set_position(*START_POSE, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1, wait=True)
        if not self._check_code(code, 'set_position'): return
        code = self._arm.set_servo_angle(angle=START_POSE_JOINTS, speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=-1)
        if not self._check_code(code, 'set_servo_angle'): return


    def stop(self):
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)
