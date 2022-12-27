from ..peanut import PeanutCanvas
from .. import ppm

def gen_bar_chart(data_pts, canvas: PeanutCanvas = PeanutCanvas(1000, 1000), chart_color: int = 0xFFBB00):
    if len(data_pts) > 10:
        print("Max data points: 10")
        return

    bar_width = 50
    bar_inity_axis_pos = 600

    canvas.fill(0xFFFFFF)
    canvas.color = 0x000000
    canvas.draw_line(0, bar_inity_axis_pos, canvas.width, bar_inity_axis_pos)
    canvas.color = chart_color
    x = bar_width
    for pt in data_pts:
        y = abs(bar_inity_axis_pos - pt)
        print(pt)
        canvas.fill_rect(x, y, bar_width, pt)
        x += 65
    return canvas

if __name__ == "__main__":
    chart = gen_bar_chart([50, 100, 34, 76, 59, 200, 45])
    ppm.save_as_ppm("out.ppm", chart(), chart.width, chart.height)