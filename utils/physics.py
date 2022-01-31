import numpy as np
from utils import nans_lib
from utils import params as p


def speed_up_ball(ball):

    if ball.v_h == 0:
        ball.v_h = 1
    velocity, angle = ball.v

    # data sila
    f_cmd = ball.m * p.a_cmd
    f_cmd_h = f_cmd * np.cos(angle)
    f_cmd_v = f_cmd * np.sin(angle)

    # otpor vazduha
    f_air = lambda v: ball.m * p.r_air * v
    f_air_h = lambda v: f_air(v) * np.cos(angle)
    f_air_v = lambda v: f_air(v) * np.sin(angle)

    # vertikalne sile
    f_v = lambda v: f_cmd_v - f_air_v(v) + ball.Q

    # sila trenja
    c_fr = 0.6
    f_fr = lambda v: c_fr * f_v(v)

    # horizontalne sile
    f_h = lambda v: f_cmd_h - f_air_h(v) - f_fr(v)

    # ovo je zakucano
    t0 = 0
    t1 = 1
    h = 2

    dv_h = lambda *args: 1/ball.m * (f_cmd_h - f_fr(args[0])) - p.r_air * args[0]
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
        velocity, angle = ball.v

        # otpor vazduha
        f_air = lambda v: ball.m * p.r_air * v
        f_air_h = lambda v: f_air(v) * np.cos(angle)
        f_air_v = lambda v: f_air(v) * np.sin(angle)

        # vertikalne sile
        f_v = lambda v: - f_air_v(v) + ball.Q

        # sila trenja
        f_fr = lambda v: p.c_fr * f_v(v)

        # horizontalne sile
        f_h = lambda v: - f_air_h(v) - f_fr(v)

        # moment sile
        M = lambda v: f_h(v) * ball.r

        # pocetna ugaona brzina i ubrzanje
        w_0 = ball.v[0] / ball.r
        alpha_0 = ball.a[0] / ball.r
        omega_0 = np.array([w_0])

        # ovo je zakucano
        t0 = 0
        t1 = 1
        h = 2

        dw = lambda *args: M(args[0]) / ball.I
        w = nans_lib.rk4N(t0, t1, h, omega_0, dw)[0]
        ball.v_h = w[1]*ball.r
        ball.a_h = dw(w[1])/(t1-t0)


