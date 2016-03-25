#!/usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from earo.event import Event, Field
from earo.handler import Handler, Emittion, NoEmittion
from earo.mediator import Mediator
from earo.context import Context
from earo.processor import Processor, ProcessFlow
from earo.diagram import Diagram


class TestDiagram(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_active_process_flow(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            event_a_field = Field(int, 100);

        class EventB(Event):
            event_b_field = Field(str, 'hello');

        class EventC(Event):
            event_c_field = Field(float, 1.1);

        class EventD(Event):
            event_d_field = Field(dict, {'x': 3, 'y': 4});

        class EventE(Event):
            event_e_field = Field(list, [3, 8, 7]);

        def fooA_BC(context, event):
            import time
            time.sleep(0.5)
            return (Emittion(EventB()), NoEmittion(EventC, 'Test No Emmittion EventC'))

        def fooA(context, event):
            pass

        def fooB_D(context, event):
            return Emittion(EventD())

        def fooC(context, event):
            pass

        def fooD(context, event):
            1 / 0

        handler_1 = Handler(EventA, fooA_BC, [EventB, EventC])
        handler_2 = Handler(EventA, fooA)
        handler_3 = Handler(EventB, fooB_D, [EventD])
        handler_4 = Handler(EventC, fooC)
        handler_5 = Handler(EventD, fooD)

        mediator.register_event_handler(
            handler_1,
            handler_2,
            handler_3,
            handler_4,
            handler_5
        )

        context = Context(mediator, EventA(), processor)
        context.process()
        process_flow = context.process_flow

        diagram = Diagram(process_flow=process_flow)
        diagram.to_html('/tmp/earo/active')

    def test_inactive_process_flow(self):

        mediator = Mediator()

        class EventA(Event):
            event_a_field = Field(int, 100);

        class EventB(Event):
            event_b_field = Field(str, 'hello');

        class EventC(Event):
            event_c_field = Field(float, 1.1);

        class EventD(Event):
            event_d_field = Field(dict, {'x': 3, 'y': 4});

        def fooBC(context, event):
            return (Emittion(EventB()), Emittion(EventC()))

        def fooD(context, event):
            return Emittion(EventD())

        def foo(context, event):
            pass

        def fooEx(context, event):
            1 / 0

        handler_1 = Handler(EventA, fooBC, [EventB, EventC])
        handler_2 = Handler(EventA, foo)
        handler_3 = Handler(EventB, fooD, [EventD])
        handler_4 = Handler(EventC, foo)
        handler_5 = Handler(EventD, fooEx)

        mediator.register_event_handler(
            handler_1,
            handler_2,
            handler_3,
            handler_4,
            handler_5
        )

        process_flow = ProcessFlow(mediator, EventA)
        diagram = Diagram(process_flow=process_flow)
        diagram.to_html('/tmp/earo/inactive')

    def test_json(self):

        mediator = Mediator()

        class EventA(Event):
            event_a_field = Field(int, 100);

        class EventB(Event):
            event_b_field = Field(str, 'hello');

        class EventC(Event):
            event_c_field = Field(float, 1.1);

        class EventD(Event):
            event_d_field = Field(dict, {'x': 3, 'y': 4});

        def fooBC(context, event):
            return (Emittion(EventB()), Emittion(EventC()))

        def fooD(context, event):
            return Emittion(EventD())

        def foo(context, event):
            pass

        def fooEx(context, event):
            1 / 0

        handler_1 = Handler(EventA, fooBC, [EventB, EventC])
        handler_2 = Handler(EventA, foo)
        handler_3 = Handler(EventB, fooD, [EventD])
        handler_4 = Handler(EventC, foo)
        handler_5 = Handler(EventD, fooEx)

        mediator.register_event_handler(
            handler_1,
            handler_2,
            handler_3,
            handler_4,
            handler_5
        )

        process_flow = ProcessFlow(mediator, EventA)
        diagram_from_process_flow = Diagram(process_flow=process_flow)
        json = diagram_from_process_flow.to_json()
        diagram_from_json = Diagram(json=json)
        diagram_from_json.to_html('/tmp/earo/json')


if __name__ == '__main__':
    unittest.main()
