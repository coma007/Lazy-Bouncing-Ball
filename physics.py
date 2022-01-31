import math
import nans_lib
import numpy as np


def speed_up_ball(ball):

    if ball.v_h == 0:
        ball.v_h = 1
    velocity, angle = ball.v

    # data sila
    a_cmd = 7
    f_cmd = ball.m * a_cmd
    f_cmd_h = f_cmd * math.cos(angle)
    f_cmd_v = f_cmd * math.sin(angle)

    # otpor vazduha
    r_air = 0.02
    f_air = lambda v: ball.m * r_air * v
    f_air_h = lambda v: f_air(v) * math.cos(angle)
    f_air_v = lambda v: f_air(v) * math.sin(angle)

    # tezina lopte
    g = 9.81
    q_ball = ball.m * g

    # vertikalne sile
    f_v = lambda v: f_cmd_v - f_air(v) + q_ball

    # sila trenja
    c_fr = 0.6
    f_fr = lambda v: c_fr * f_v(v)

    # horizontalne sile
    f_h = lambda v: f_cmd_h - f_air_h(v) - f_fr(v)

    # ovo je zakucano
    t0 = 0
    t1 = 1
    h = 2

    dv_h = lambda *args: 1/ball.m * (f_cmd_h - f_fr(args[0])) - r_air * args[0]
    v_h_0 = np.array([ball.v_h])

    v_h = nans_lib.rk4N(t0, t1, h, v_h_0, dv_h)[0]
    if v_h[1] < ball.v_h_max:
        ball.v_h = v_h[1]
        ball.a_h = f_h(v_h_0[0])/ball.m
        ball.x += (v_h_0[0] + ball.a_h * 1/2 * (t1-t0)**2) / 1000
    else:
        ball.x += ball.v_h * (t1-t0)


def slow_down_ball(ball):
    pass


def jump_ball(ball):
    pass


def inertion(ball):
    if ball.v_h == 0:
        return
    else:
        pass

