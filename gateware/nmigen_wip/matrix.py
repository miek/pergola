import itertools

from pergola import PergolaPlatform
from nmigen import *
from nmigen.build import *


class Matrix(Elaboratable):
	def elaborate(self, platform):
		m = Module()

		def get_all_resources(name):
			resources = []
			for number in itertools.count():
				try:
					resources.append(platform.request(name, number))
				except ResourceError:
					break
			return resources

		leds = [res.o for res in get_all_resources("led")]
		matrix = platform.request('matrix', 0)

		div = 20
		counter = Signal(8+div)

		m.d.sync += counter.eq(counter + 1)
		m.d.comb += Cat(leds).eq(counter[div:])

		m.d.comb += [
			matrix.rows.eq(counter[div+3:div+3+4]),
			matrix.oe.eq(counter[0:3] != 0b000),
			matrix.ser.eq(counter[div+2]),
			matrix.clk.eq(counter[div]),
			matrix.lat.eq(counter[div+1]),
		]
		return m


if __name__ == "__main__":
	p = PergolaPlatform()

	conn = ('pmod', 2)
	p.add_resources([
		Resource('matrix', 0,
			Subsignal('rows', Pins('1 2 3 4', conn=conn, dir='o')),
			Subsignal('oe',   Pins('7', conn=conn, dir='o')),
			Subsignal('lat',  Pins('8', conn=conn, dir='o')),
			Subsignal('clk',  Pins('9', conn=conn, dir='o')),
			Subsignal('ser',  Pins('10', conn=conn, dir='o')),
		),
	])
	p.build(Matrix(), do_program=True)
