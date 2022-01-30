import math
import nans_lib
import numpy as np


def speed_up_ball(ball):

    if ball.v_h == 0:
        ball.v_h = 1
    angle, velocity = ball.v

    # data sila
    a_cmd = 5
    f_cmd = ball.m * a_cmd
    f_cmd_h = f_cmd * math.cos(angle)
    f_cmd_v = f_cmd * math.sin(angle)

    # otpor vazduha
    r_air = 2
    f_air = lambda v: ball.m * r_air * v
    f_air_h = lambda v: f_air(v) * math.cos(angle)
    f_air_v = lambda v: f_air(v) * math.sin(angle)

    # tezina lopte
    g = 9.81
    q_ball = ball.m * g

    # vertikalne sile
    f_v = lambda v: f_cmd_v + q_ball
    ball.a_v = lambda v: f_v(v) / ball.m

    # sila trenja
    c_fr = 0.1
    f_fr = lambda v: c_fr * f_v(v)

    # horizontalne sile
    f_h = lambda v: f_cmd_h - f_air_h(v) - f_fr(v)
    ball.a_h = lambda v: f_h(v) / ball.m

    # ovo je zakucano
    t0 = 0
    t1 = 1
    h = 10000

    dv_h = lambda *args: 1/ball.m * (f_cmd_h - f_fr(args[0])) - r_air * args[0]
    print(dv_h(ball.v_h))
    v_h_0 = np.array([ball.v_h])

    v_h = nans_lib.rk4N(t0, t1, h, v_h_0, dv_h)[0][0]
    print(v_h)


def slow_down_ball(ball):
    pass


def jump_ball(ball):
    pass
