import turtle
import sys, random, argparse
import numpy as np
import math
import random
from PIL import Image
from datetime import datetime
from math import gcd


# 绘制曲线的类
class Spiro:
    # 定义
    def __init__(self, xc, yc, col, R, r, l):
        # 创建海龟对象
        self.t = turtle.Turtle()
        # 设计光标形象
        self.t.shape("turtle")
        # 设计绘图角度增量
        self.step = 5
        # 设置一个标志，将在动画中使用他，他会产生一组螺旋线
        self.drawingComplete = False
        # 下面是调用自定义函数部分
        # set parameters
        self.setparams(xc, yc, col, R, r, l)
        # 初始化绘画
        self.restart()

    # 设置参数
    def setparams(self, xc, yc, col, R, r, l):
        # 曲线参数
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r // gcdVal
        # get ratio of radii
        self.k = r / float(R)
        # 设置颜色
        self.t.color(*col)
        # 保存当前角度 我们将用他来创建动画
        self.a = 0

    def restart(self):
        # 设计标志
        self.drawingComplete = False
        # 展现海龟
        self.t.showturtle()
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        # 绘画剩下的点
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    def update(self):
        # 退出循环
        if self.drawingComplete:
            return

        # 增加角度
        self.a += self.step
        # draw a step
        R, k, l = self.R, self.k, self.l
        # set the angle
        a = math.radians(self.a)
        x = self.R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = self.R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True
            # 绘制完成时隐藏海龟
            self.t.hideturtle()
        # 清除所有

    def clear(self):
        self.t.clear()


# 让曲线变得活动起来的类
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # 设置以毫秒为单位的计数器
        self.deltaT = 10  # 时间差
        # 得到窗口的大小
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro 对象
        self.spiros = []
        for i in range(N):
            # 产生随机的因素
            rparams = self.genRandomParams()
            # 设置曲线因素
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            # call timer 每隔deltaT时间间隔进行一次update
            turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col = (
            random.random(),
            random.random(),
            random.random()
        )
        return (xc, yc, col, R, r, l)

    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    def update(self):
        # update all spiros

        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed sppiros
            if spiro.drawingComplete:
                nComplete += 1
            # restart if all spiros are complete
            if nComplete == len(self.spiros):
                self.restart()
            # call the timer
            turtle.ontimer(self.update, self.deltaT)
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

    # 作为png文件保存曲线


def saveDrawing():
    # 隐藏海龟
    turtle.hideturtle()
    # 产生唯一的文件名
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = "spiro" + dateStr
    print("saving drawing to %s.eps/png" % fileName)
    # 得到tkinter和canvas
    canvas = turtle.getcanvas()
    # save the drawing as a postscript image(EPS)嵌入式文件格式
    canvas.postscript(file=fileName + "eps")
    # 使用pillow模型把EPS转化为png文件
    img = Image.open(fileName + ".eps")
    img.save(fileName + ".pbg", "png")
    # show the turtle cursor
    turtle.showturtle()


# main() function
def main():
    # use sys.argv if needed
    print("generating spirograph...")
    # create parser创建解释器
    descStr = """
    This program draws Spirographs using the Turtle module.
    When run with no arguments ,this program draws random Spirographs.
    Terminology:
    R:radius of outer circle.
    r:radios of inner circle.
    l:ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description=descStr)
    # 添加期望的参数
    parser.add_argument("--sparams", nargs=3, dest="sparams", required=False,
                        help="The three arguments in sparams:R,r,l")
    # 解析参数
    args = parser.parse_args()
    # 设置窗口宽度为80%的整个屏幕
    turtle.setup(width=0.8)
    # 设置光标为海龟
    turtle.shape("turtle")
    # 设置标题
    turtle.title("Spirographs")
    # 添加关键处理程序来保存我们的图纸
    turtle.onkey(saveDrawing, "s")
    # 开始监听
    turtle.listen()
    # 隐藏海龟
    turtle.hideturtle()
    # 检查将所有参数送入--sparams并且画这个曲线
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # 用以给的参数画图
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animater object
        spiroAnim = SpiroAnimator(4)
        # 添加解释器
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # 添加解释器来重启动画
        turtle.onkey(spiroAnim.restart,"space")
    # start the turtle main loop
    turtle.mainloop()

# call main
if __name__ == '__main__':
    main()
