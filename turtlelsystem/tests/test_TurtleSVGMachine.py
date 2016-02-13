from turtlelsystem.TurtleSVGMachine import TurtleSVGMachine
from nose.tools import assert_almost_equal

def test_forward():
    turtle = TurtleSVGMachine(width = 20, height = 20)
    turtle.do_command("FORWARD 10")
    assert_almost_equal(turtle.x, 20.0)

def test_backward():
    turtle = TurtleSVGMachine(width = 20, height = 20)
    turtle.do_command("BACKWARD 10")
    assert_almost_equal(turtle.x, 0.0)

def test_left():
    turtle = TurtleSVGMachine()
    turtle.do_command("LEFT 30")
    assert_almost_equal(turtle.theta, 30.0)

def test_right():
    turtle = TurtleSVGMachine()
    turtle.do_command("RIGHT 30")
    assert_almost_equal(turtle.theta, 330.0)
