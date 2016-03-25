#!/usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from earo.event import Event, Field
from earo.handler import Handler, Emittion, NoEmittion
from earo.mediator import Mediator
from earo.context import Context
from earo.processor import ProcessFlow, Processor


class TestProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_emit_excepted_events(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            return Emittion(EventB())

        def boo(context, event):
            pass

        handler_1 = Handler(EventA, foo, [EventB])
        handler_2 = Handler(EventB, boo)

        mediator.register_event_handler(
            handler_1,
            handler_2
        )

        context = Context(mediator, EventA(), processor)
        context.process()
        process_flow = context.process_flow

        handler_node = process_flow.root.child_nodes[0]
        handler_runtime = handler_node.active_item
        self.assertTrue(handler_runtime.succeeded)

    def test_emit_unexcepted_events(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            return Emittion(EventB())

        def boo(context, event):
            pass

        handler_1 = Handler(EventA, foo)
        handler_2 = Handler(EventB, boo)

        mediator.register_event_handler(
            handler_1,
            handler_2
        )

        context = Context(mediator, EventA(), processor)

        with self.assertRaises(TypeError):
            context.process()

    def test_no_emittion(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            return NoEmittion(EventB, 'test')

        def boo(context, event):
            pass

        handler_a = Handler(EventA, foo, [EventB])
        handler_b = Handler(EventB, boo)

        mediator.register_event_handler(
            handler_a,
            handler_b
        )

        context = Context(mediator, EventA(), processor)
        context.process()
        process_flow = context.process_flow
        self.assertIsNone(process_flow.find_event(EventB))
        self.assertEqual(process_flow.why_no_emittion(EventB), 'test')

    def test_process_flow_active(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        class EventC(Event):
            pass

        class EventD(Event):
            pass

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

        context = Context(mediator, EventA(), processor)
        context.process()
        process_flow = context.process_flow

        event_node_1 = process_flow.root
        handler_node_1 = event_node_1.child_nodes[0]
        handler_node_2 = event_node_1.child_nodes[1]
        event_node_2 = handler_node_1.child_nodes[0]
        event_node_3 = handler_node_1.child_nodes[1]
        handler_node_3 = event_node_2.child_nodes[0]
        handler_node_4 = event_node_3.child_nodes[0]
        event_node_4 = handler_node_3.child_nodes[0]
        handler_node_5 = event_node_4.child_nodes[0]

        self.assertIsInstance(event_node_1.active_item, EventA)
        self.assertIsInstance(event_node_2.active_item, EventB)
        self.assertIsInstance(event_node_3.active_item, EventC)
        self.assertIsInstance(event_node_4.active_item, EventD)

        self.assertTrue(handler_node_1.active_item.succeeded)
        self.assertTrue(handler_node_2.active_item.succeeded)
        self.assertTrue(handler_node_3.active_item.succeeded)
        self.assertTrue(handler_node_4.active_item.succeeded)
        self.assertFalse(handler_node_5.active_item.succeeded)

        self.assertIsNotNone(process_flow.find_event(EventA))
        self.assertIsNotNone(process_flow.find_event(EventB))
        self.assertIsNotNone(process_flow.find_event(EventC))
        self.assertIsNotNone(process_flow.find_event(EventD))

        self.assertTrue(event_node_1.active)
        self.assertTrue(event_node_2.active)
        self.assertTrue(event_node_3.active)
        self.assertTrue(event_node_4.active)

        self.assertTrue(handler_node_1.active)
        self.assertTrue(handler_node_2.active)
        self.assertTrue(handler_node_3.active)
        self.assertTrue(handler_node_4.active)
        self.assertTrue(handler_node_5.active)


    def test_process_flow_inactive(self):

        mediator = Mediator()

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        class EventC(Event):
            pass

        class EventD(Event):
            pass

        class EventE(Event):
            pass

        def foo(context, event):
            pass

        handler_1 = Handler(EventA, foo, [EventB, EventC])
        handler_2 = Handler(EventA, foo, [EventD])
        handler_3 = Handler(EventA, foo)
        handler_4 = Handler(EventB, foo, [EventE])
        handler_5 = Handler(EventC, foo)
        handler_6 = Handler(EventD, foo)
        handler_7 = Handler(EventE, foo)

        mediator.register_event_handler(
            handler_1,
            handler_2,
            handler_3,
            handler_4,
            handler_5,
            handler_6,
            handler_7
        )

        process_flow = ProcessFlow(mediator, EventA)

        event_node_1 = process_flow.root
        handler_node_1 = event_node_1.child_nodes[0]
        handler_node_2 = event_node_1.child_nodes[1]
        handler_node_3 = event_node_1.child_nodes[2]
        event_node_2 = handler_node_1.child_nodes[0]
        event_node_3 = handler_node_1.child_nodes[1]
        event_node_4 = handler_node_2.child_nodes[0]
        handler_node_4 = event_node_2.child_nodes[0]
        handler_node_5 = event_node_3.child_nodes[0]
        handler_node_6 = event_node_4.child_nodes[0]
        event_node_5 = handler_node_4.child_nodes[0]
        handler_node_7 = event_node_5.child_nodes[0]

        self.assertEqual(event_node_1.inactive_item, EventA)
        self.assertEqual(event_node_2.inactive_item, EventB)
        self.assertEqual(event_node_3.inactive_item, EventC)
        self.assertEqual(event_node_4.inactive_item, EventD)
        self.assertEqual(event_node_5.inactive_item, EventE)

        self.assertFalse(event_node_1.active)
        self.assertFalse(event_node_2.active)
        self.assertFalse(event_node_3.active)
        self.assertFalse(event_node_4.active)
        self.assertFalse(event_node_5.active)

        self.assertEqual(handler_node_1.inactive_item, handler_1)
        self.assertEqual(handler_node_2.inactive_item, handler_2)
        self.assertEqual(handler_node_3.inactive_item, handler_3)
        self.assertEqual(handler_node_4.inactive_item, handler_4)
        self.assertEqual(handler_node_5.inactive_item, handler_5)
        self.assertEqual(handler_node_6.inactive_item, handler_6)
        self.assertEqual(handler_node_7.inactive_item, handler_7)

        self.assertFalse(handler_node_1.active)
        self.assertFalse(handler_node_2.active)
        self.assertFalse(handler_node_3.active)
        self.assertFalse(handler_node_4.active)
        self.assertFalse(handler_node_5.active)
        self.assertFalse(handler_node_6.active)
        self.assertFalse(handler_node_7.active)

    def test_processor_statistics(self):

        mediator = Mediator()
        processor = Processor('.+')

        class EventA(Event):
            sleep_seconds = Field(float, 0.05)
            raise_exception = Field(bool, False)

        class EventB(Event):
            pass

        def fooA_B(context, event):
            import time
            time.sleep(event.sleep_seconds)
            if event.raise_exception:
                raise Exception()
            return NoEmittion(EventB, 'test')

        def fooB(context, event):
            pass

        handler_a = Handler(EventA, fooA_B, [EventB])
        handler_b = Handler(EventB, fooB)

        mediator.register_event_handler(
            handler_a,
            handler_b
        )

        self.assertEqual(processor.process_count, 0)
        self.assertEqual(processor.exception_count, 0)
        self.assertEqual(processor.event_process_count(EventA), 0)
        self.assertEqual(processor.event_process_count(EventB), 0)
        self.assertEqual(processor.event_exception_count(EventA), 0)
        self.assertEqual(processor.event_exception_count(EventB), 0)
        self.assertEqual(processor.event_min_time_cost(EventA), -1)
        self.assertEqual(processor.event_min_time_cost(EventB), -1)
        self.assertEqual(processor.event_max_time_cost(EventA), -1)
        self.assertEqual(processor.event_max_time_cost(EventB), -1)

        for sleep_seconds, raise_exception in (
                                    (0.01, False),
                                    (0.05, False),
                                    (0.02, True)):
            context = Context(
                mediator,
                EventA(sleep_seconds=sleep_seconds,
                        raise_exception=raise_exception),
                processor)
            context.process()

        self.assertEqual(processor.process_count, 3)
        self.assertEqual(processor.exception_count, 1)
        self.assertEqual(processor.event_process_count(EventA), 3)
        self.assertEqual(processor.event_process_count(EventB), 0)
        self.assertEqual(processor.event_exception_count(EventA), 1)
        self.assertEqual(processor.event_exception_count(EventB), 0)
        self.assertLess(processor.event_min_time_cost(EventA), 15)
        self.assertEqual(processor.event_min_time_cost(EventB), -1)
        self.assertGreaterEqual(processor.event_max_time_cost(EventA), 50)
        self.assertEqual(processor.event_max_time_cost(EventB), -1)


if __name__ == '__main__':
    unittest.main()
