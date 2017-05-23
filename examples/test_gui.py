#!/usr/bin/env python3

from pyPLClib import PID
import tkinter as tk
from tkinter import ttk


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
        self.fMain = FrmMain(self)
        self.fMain.pack(fill=tk.BOTH, expand=tk.YES)


class FrmMain(FrmTab):
    def __init__(self, parent, *args, **kwargs):
        FrmTab.__init__(self, parent, *args, **kwargs)
        # some vars
        self.pid = PID(kp=1.0, ti=60.0, td=0.0, update_every=1.0)
        self.pid.start()
        self.sp_str = tk.StringVar(value='0.0')
        self.pv_str = tk.StringVar(value='0.0')
        self.kp_str = tk.StringVar(value='%.2f' % self.pid.kp)
        self.ti_str = tk.StringVar(value='%.2f' % self.pid.ti)
        self.td_str = tk.StringVar(value='%.2f' % self.pid.td)
        self.set_out_str = tk.StringVar(value='%.2f' % self.pid.out)
        # capture frame
        self.frm1 = tk.Frame(self)
        self.frm1.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        # sp
        self.lbl_sp = tk.Label(self.frm1, text='Set-Point (0/100)')
        self.lbl_sp.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_sp = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.sp_str)
        self.ent_sp.bind("<Return>", lambda evt: self.set_sp())
        self.ent_sp.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_sp = tk.Button(self.frm1, text='Set SP', command=self.set_sp)
        self.but_sp.grid(row=0, column=2, sticky=tk.EW, padx=5, pady=5)
        # pv
        self.lbl_pv = tk.Label(self.frm1, text='Process Value (0/100)')
        self.lbl_pv.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_pv = tk.Entry(self.frm1, width=16, textvariable=self.pv_str)
        self.ent_pv.bind("<Return>", lambda evt: self.set_pv())
        self.ent_pv.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_pv = tk.Button(self.frm1, text='Set PV', command=self.set_pv)
        self.but_pv.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)
        # out
        self.lbl_out = tk.Label(self.frm1)
        self.lbl_out.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.pb_out = ttk.Progressbar(self.frm1, orient='horizontal', length=200, mode='determinate')
        self.pb_out.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        # kp
        self.lbl_kp = tk.Label(self.frm1, text='kp')
        self.lbl_kp.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_kp = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.kp_str)
        self.ent_kp.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_kp = tk.Button(self.frm1, text='Set kp', command=self.set_kp)
        self.but_kp.grid(row=3, column=2, sticky=tk.EW, padx=5, pady=5)
        # ti
        self.lbl_ti = tk.Label(self.frm1, text='Ti (s)')
        self.lbl_ti.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_ti = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.ti_str)
        self.ent_ti.bind("<Return>", lambda evt: self.set_ti())
        self.ent_ti.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_ti = tk.Button(self.frm1, text='Set Ti', command=self.set_ti)
        self.but_ti.grid(row=4, column=2, sticky=tk.EW, padx=5, pady=5)
        # td
        self.lbl_td = tk.Label(self.frm1, text='Td (s)')
        self.lbl_td.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_td = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.td_str)
        self.ent_td.bind("<Return>", lambda evt: self.set_td())
        self.ent_td.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_td = tk.Button(self.frm1, text='Set Td', command=self.set_td)
        self.but_td.grid(row=5, column=2, sticky=tk.EW, padx=5, pady=5)
        # set out
        self.lbl_set_out = tk.Label(self.frm1, text='Fix out (0/100)')
        self.lbl_set_out.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_set_out = tk.Entry(self.frm1, width=16, validate='all', textvariable=self.set_out_str)
        self.ent_set_out.bind("<Return>", lambda evt: self.set_out())
        self.ent_set_out.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.but_set_out = tk.Button(self.frm1, text='Set out', command=self.set_out)
        self.but_set_out.grid(row=6, column=2, sticky=tk.EW, padx=5, pady=5)
        # start update function
        self.update_pid()

    def set_sp(self):
        self.pid.sp = float(self.sp_str.get())

    def set_pv(self):
        self.pid.pv = float(self.pv_str.get())

    def set_kp(self):
        self.pid.kp = float(self.kp_str.get())

    def set_ti(self):
        self.pid.ti = float(self.ti_str.get())

    def set_td(self):
        self.pid.td = float(self.td_str.get())

    def set_out(self):
        s_out = float(self.set_out_str.get())
        self.pid.set_man(s_out)
        self.pid.update(force=True)
        self.pid.set_auto()

    def update_pid(self):
        if self.pid.update():
            self.pb_out['value'] = self.pid.out
            self.lbl_out['text'] = 'Out = %.2f' % self.pid.out
        self.after(ms=100, func=self.update_pid)


if __name__ == '__main__':

    # main Tk App
    app = TkApp()
    app.mainloop()
