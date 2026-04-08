import pytest
from appwindows.geometry import Point

import apparser.movers.math_antirobot as math_antirobot
from apparser.movers.math_antirobot import AntiRobotMover, DefaultMoveGenerator


@pytest.mark.parametrize(('kwargs', 'error', 'message'), [
    ({'min_time': '1'}, TypeError, 'min_time must be number'),
    ({'max_time': '2'}, TypeError, 'max_time must be number'),
    ({'min_shift': '3'}, TypeError, 'min_shift must be number'),
    ({'max_shift': '4'}, TypeError, 'max_shift must be number'),
    ({'min_shift': 20, 'max_shift': 10}, ValueError, 'min_shift must be less than max_shift'),
    ({'min_time': 3, 'max_time': 2}, ValueError, 'min_time must be less than max_time'),
    ({'min_time': -1}, ValueError, 'min_time must be greater than 0'),
])
def test_default_move_generator_init_validation(kwargs, error, message):
    with pytest.raises(error, match=message):
        DefaultMoveGenerator(**kwargs)


def test_default_move_generator_get_random_time(monkeypatch):
    random_calls = []

    def fake_uniform(min_time, max_time):
        random_calls.append((min_time, max_time))
        return 1.5

    monkeypatch.setattr(math_antirobot.random, 'uniform', fake_uniform)
    generator = DefaultMoveGenerator(min_time=1, max_time=2)

    assert generator._DefaultMoveGenerator__get_random_time() == 1.5
    assert random_calls == [(1, 2)]


@pytest.mark.parametrize(('current_position', 'end_position', 'random_shift', 'expected_position'), [
    (Point(10, 20), Point(20, 30), 6, Point(3, 3)),
    (Point(10, 10), Point(7, 4), 100, Point(-3, -6)),
])
def test_default_move_generator_get_random_position(monkeypatch,
                                                    current_position,
                                                    end_position,
                                                    random_shift,
                                                    expected_position):
    monkeypatch.setattr(math_antirobot.random, 'uniform', lambda min_shift, max_shift: random_shift)
    generator = DefaultMoveGenerator(min_shift=0, max_shift=100)

    assert generator._DefaultMoveGenerator__get_random_position(current_position, end_position) == expected_position


@pytest.mark.parametrize(('start_position', 'end_position', 'message'), [
    ('start', Point(1, 1), 'start_position must be Point'),
    (Point(1, 1), 'end', 'end_position must be Point'),
])
def test_default_move_generator_call_validation(start_position, end_position, message):
    generator = DefaultMoveGenerator()

    with pytest.raises(TypeError, match=message):
        list(generator(start_position, end_position))


def test_default_move_generator_call_returns_empty_if_positions_equal():
    generator = DefaultMoveGenerator()

    assert list(generator(Point(10, 10), Point(10, 10))) == []


def test_default_move_generator_call_returns_end_position_if_it_is_close(monkeypatch):
    generator = DefaultMoveGenerator(min_shift=0, max_shift=10)
    monkeypatch.setattr(generator, '_DefaultMoveGenerator__get_random_time', lambda: 0.5)

    result = list(generator(Point(1, 1), Point(4, 4)))

    assert result == [(Point(4, 4), 0.5)]


def test_default_move_generator_call_returns_intermediate_and_end_positions(monkeypatch):
    generator = DefaultMoveGenerator(min_shift=0, max_shift=6)
    time_values = iter([0.1, 0.2])
    positions = []

    monkeypatch.setattr(generator, '_DefaultMoveGenerator__get_random_time', lambda: next(time_values))

    def fake_get_random_position(start_position, end_position):
        positions.append((start_position, end_position))
        return Point(5, 0)

    monkeypatch.setattr(generator, '_DefaultMoveGenerator__get_random_position', fake_get_random_position)

    result = list(generator(Point(0, 0), Point(10, 0)))

    assert positions == [(Point(0, 0), Point(10, 0))]
    assert result == [(Point(5, 0), 0.1),
                      (Point(10, 0), 0.2)]


def test_anti_robot_mover_move_validation():
    mover = AntiRobotMover()

    with pytest.raises(TypeError, match='position must be Point'):
        mover.move('position')


def test_anti_robot_mover_move(monkeypatch):
    generated_points = []
    moved_points = []

    def fake_move_generator(start_position, end_position):
        generated_points.append((start_position, end_position))
        yield Point(5, 6), 0.1
        yield Point(7, 8), 0.2

    monkeypatch.setattr(math_antirobot.mouse, 'get_position', lambda: (1, 2))
    monkeypatch.setattr(math_antirobot.mouse, 'move',
                        lambda x, y, duration=0: moved_points.append((x, y, duration)))

    mover = AntiRobotMover(fake_move_generator)
    mover.move(Point(10, 20))

    assert generated_points == [(Point(1, 2), Point(10, 20))]
    assert moved_points == [(5, 6, 0.1),
                            (7, 8, 0.2)]
