#!/usr/bin/env python3

import os
os.path('../')
from pyPLClib import PID
import tkinter as tk


class FrmTab(tk.Frame):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        tk.Frame.__init__(self, notebook, *args, **kwargs)
        # global tk app shortcut
        self.notebook = notebook
        self.app = notebook.master
        # frame auto-refresh delay (in ms)
        self.update_ms = update_ms
        # setup auto-refresh of notebook tab (on-visibility and every update_ms)
        self.bind('<Visibility>', lambda evt: self.tab_update())
        self._tab_update()

    def _tab_update(self):
        if self.winfo_ismapped():
            self.tab_update()
        self.master.after(self.update_ms, self._tab_update)

    def tab_update(self):
        pass


class TkApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Test PID')
        # self.attributes('-fullscreen', True)
        # self.geometry('800x400')
        # build a notebook with tabs
        self.fMain = FrmMain(self)
        self.fMain.pack(fill=tk.BOTH, expand=tk.YES)

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


class FrmMain(FrmTab):
    def __init__(self, notebook, update_ms=500, *args, **kwargs):
        FrmTab.__init__(self, notebook, update_ms, *args, **kwargs)
        # some vars
        self.sp_str = tk.StringVar(value='0.0')
        self.pv_str = tk.StringVar(value='0.0')
        # capture frame
        self.frm1 = tk.Frame(self)
        self.frm1.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.lbl_sp = tk.Label(self.frm1, text='Set-Point')
        self.lbl_sp.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_sp = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.sp_str)
        self.ent_sp.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_sp = tk.Button(self.frm1, text='Set SP', command=self.set_sp)
        self.but_sp.grid(row=0, column=2, sticky=tk.EW, padx=5, pady=5)
        self.lbl_pv = tk.Label(self.frm1, text='Process Value')
        self.lbl_pv.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_pv = tk.Entry(self.frm1, width=16, textvariable=self.pv_str)
        self.ent_pv.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_pv = tk.Button(self.frm1, text='Set PV', command=self.set_pv)
        self.but_pv.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)

    def set_sp(self):
        try:
            pid.sp = float(self.ent_sp.get())
        except ValueError:
            pass

    def set_pv(self):
        try:
            pid.pv = float(self.ent_pv.get())
        except ValueError:
            pass


if __name__ == '__main__':
    # some vars
    pid = PID(kp=0, ti=10, update_every=4.0)
    pid.start()
    # main Tk App
    app = TkApp()
    app.do_every(lambda: pid.update(), every_ms=10)
    app.do_every(lambda: print(pid.out), every_ms=1000)
    app.mainloop()
