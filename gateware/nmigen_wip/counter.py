import itertools

from pergola import PergolaPlatform
from nmigen import *
from nmigen.build import *


class Counter(Elaboratable):
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

		div = 20
		counter = Signal(8+div)

		m.d.sync += counter.eq(counter + 1)
		m.d.comb += Cat(leds).eq(counter[div:])
		return m


if __name__ == "__main__":
	p = PergolaPlatform()
	p.build(Counter(), do_program=True)
