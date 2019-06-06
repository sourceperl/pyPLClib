from __future__ import division
import time


class PID:
    # class const
    OUT_MAX = 100.0
    OUT_MIN = 0.0

    def __init__(self, kp, ti=0.0, td=0.0, update_every=1.0, pv_max=100.0, pv_min=0.0, set_point=0.0):
        """
        Python module for PID compute

        :param kp: proportional gain
        :type kp: float
        :param ti: integral time (in s)
        :type ti: float
        :param td: derivative time (in s)
        :type td: float
        :param update_every: delay between PID update (in s)
        :type update_every: float
        :param pv_max: max process value for PID scaling
        :type pv_max: float
        :param pv_min: min process value for PID scaling
        :type pv_min: float
        :param set_point: set-point value
        :type set_point: float
        """
        # public
        self.run = False
        self.kp = float(kp)
        self.ti = float(ti)
        self.td = float(td)
        self.update_every = float(update_every)
        self.sp = float(set_point)
        self.pv = 0.0
        self.pv_max = float(pv_max)
        self.pv_min = float(pv_min)
        self.out = 0.0
        self.man = False
        self.out_man = 0.0
        # private
        self._term_p = 0.0
        self._term_i = 0.0
        self._term_d = 0.0
        self._last_input = 0.0
        self._err = 0.0
        self._last_update = 0.0

    @property
    def sp_scale(self):
        """
        Convert set-point to 0/100 %

        :return: set-point scaled value
        """
        return (self.sp - self.pv_min) * 100.0 / (self.pv_max - self.pv_min)

    @property
    def pv_scale(self):
        """
        Convert process value to 0/100 %

        :return: process value scaled value
        """
        return (self.pv - self.pv_min) * 100.0 / (self.pv_max - self.pv_min)

    def start(self):
        """
        Turn on PID
        """
        self.run = True

    def stop(self):
        """
        Turn off PID
        """
        self.run = False

    def set_auto(self):
        """
        Set PID in automatic mode
        """
        self.man = False

    def set_man(self, out=None):
        """
        Set PID in manual mode (optional out value, default is current one)

        :param out: PID output value
        :type out: float
        """
        if out is None:
            self.out_man = self.out
        else:
            self.out_man = out
        self.man = True

    def update(self, force=False):
        """
        Update PID value (call this in your main loop)

        :param force: update PID without take care of update_every time
        :type force: bool
        :return: true if PID value are updated
        :rtype: bool
        """
        now = time.time()
        delta_t = now - self._last_update

        # it's time to update PID or it's a forced update ?
        if delta_t > self.update_every or force:
            self._last_update = now

            # compute error
            self._err = self.sp_scale - self.pv_scale

            # proportional term
            self._term_p = self.kp * self._err

            # integral term
            # errors sum with second weighting
            self._term_i += self._err * delta_t / self.ti

            # check integral saturation
            self._term_i = min(self._term_i, self.OUT_MAX)
            self._term_i = max(self._term_i, self.OUT_MIN)

            # derivative term
            self._term_d = - self.td * ((self.pv_scale - self._last_input) / delta_t)

            # for next cycle
            self._last_input = self.pv_scale

            # compute PID Output
            if self.run:
                # manual mode
                if self.man:
                    # output direct update
                    self.out = self.out_man
                    # keep integral term in sync
                    self._term_i = self.out_man - self._term_p - self._term_d
                # auto mode
                else:
                    self.out = self._term_p + self._term_i + self._term_d

            # limit PID out
            self.out = min(self.out, self.OUT_MAX)
            self.out = max(self.out, self.OUT_MIN)

            # return true if PID is update
            return True
        else:
            # return false if PID is not update
            return False
