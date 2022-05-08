#! /usr/bin/env python
from migen import *
from migen.build.platforms import icestick


class Rot(Module):
    def __init__(self):
        self.clk_freq = 12000000
        self.read = Signal()
        self.rot = Signal(4)
        self.divider = Signal(max=self.clk_freq)
        self.d1 = Signal()
        self.d2 = Signal()
        self.d3 = Signal()
        self.d4 = Signal()
        self.d5 = Signal()

        ###
        self.comb += [j.eq(self.rot[i]) for i, j in enumerate([self.d1, self.d2, self.d3, self.d4])]
       
        self.comb += [self.d5.eq(1)]

        self.sync += [
            If(self.read,
                If(self.divider == int(self.clk_freq) - 1,
                    self.divider.eq(0),
                    self.rot.eq(Cat(self.rot[-1], self.rot[:-1]))
                ).Else(
                    self.divider.eq(self.divider + 1)
                )
            ).Else(
                self.read.eq(1),
                self.rot.eq(1),
                self.divider.eq(0)
            )
        ]


if __name__ == "__main__":
    plat = icestick.Platform()
    m = Rot()
    m.comb += [plat.request("user_led").eq(1) for l in [m.d1, m.d2, m.d3, m.d4, m.d5]]
    plat.build(m, run=True, build_dir="rot", build_name="rot_migen")
    plat.create_programmer().flash(0, "rot/rot_migen.bin")

