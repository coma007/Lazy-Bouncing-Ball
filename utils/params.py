import numpy as np

g = 9.81
r_air = 0.001
c_fr = 0.01
a_cmd = 7
a_cmd_down = 4

v_up = 900
angle_up = 1/2 * np.pi

ball_mass = 1
bullet_mass = 1


def print_params():
    print("\nDEFAULT PARAMETERS: ")
    print(f"1. Air restistance = {r_air}")
    print(f"2. Ground friction = {c_fr}")
    print(f"3. Jump velocity = {v_up}")
    print(f"4. Acceleration on right key = {a_cmd}")
    print(f"5. Acceleration on left key = {a_cmd_down}")
    print(f"6. Ball mass = {ball_mass}")
    print(f"7. Linear bullet mass = {bullet_mass}")


def ask_for_params():
    print_params()
    global r_air, c_fr, a_cmd, a_cmd_down, v_up, ball_mass
    while True:
        try:
            num = int(input("\nImport number 1-7 to change parameter from list above or 0 to start: "))
            if num == 0:
                print("3 2 1 START ...")
                return
            elif num == 1:
                inp = float(input("\nAir resistance [from 0 to 1]: "))
                if 0 > inp or 1 < inp:
                    raise Exception
                r_air = inp
            elif num == 2:
                inp = float(input("\nGround friction [from 0 to 1]: "))
                if 0 > inp or 1 < inp:
                    raise Exception
                c_fr = inp
            elif num == 3:
                inp = float(input("\nJump velocity [from 800 to 1500]: "))
                if 900 > inp or 1500 < inp:
                    raise Exception
                v_up = inp
            elif num == 4:
                inp = float(input("\nAcceleration on right key [from 3 to 15]: "))
                if 3 > inp or 15 < inp:
                    raise Exception
                a_cmd = inp
            elif num == 5:
                inp = float(input("\nAcceleration on left key [from 3 to 15]: "))
                if 3 > inp or 15 < inp:
                    raise Exception
                a_cmd_down = inp
            elif num == 6:
                inp = float(input("\nMass of ball [from 1 to 10]: "))
                if 1 > inp or 10 < inp:
                    raise Exception
                ball_mass = inp
            elif num == 7:
                inp = float(input("\nMass of bullet [from 1 to 10]: "))
                if 1 > inp or 10 < inp:
                    raise Exception
                bullet_mass = inp
            else:
                raise Exception
        except Exception:
            print("Wrong input !")
