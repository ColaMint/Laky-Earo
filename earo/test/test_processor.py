# -*- coding:utf-8 -*-

import unittest
from earo.event import Event
from earo.handler import Handler, Emittion, NoEmittion
from earo.mediator import Mediator
from earo.context import Context


class TestProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_emit_excepted_events(self):

        mediator = Mediator()

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            return Emittion(EventB())

        def boo(context, event):
            pass

        handler_a = Handler(EventA, foo, [EventB])
        handler_b = Handler(EventB, boo)

        mediator.register_event_handler(
            handler_a,
            handler_b
        )

        context = Context(mediator, EventA())
        context.process()
        process_flow = context.process_flow

        handler_runtime_node = process_flow.root.child_nodes[0]
        handler_runtime = handler_runtime_node.item
        self.assertTrue(handler_runtime.succeeded)

    def test_emit_unexcepted_events(self):

        mediator = Mediator()

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            return Emittion(EventB())

        def boo(context, event):
            pass

        handler_a = Handler(EventA, foo)
        handler_b = Handler(EventB, boo)

        mediator.register_event_handler(
            handler_a,
            handler_b
        )

        context = Context(mediator, EventA())

        with self.assertRaises(TypeError):
            context.process()

    def test_process_flow(self):

        mediator = Mediator()

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

        context = Context(mediator, EventA())
        context.process()
        process_flow = context.process_flow

        event_node_1 = process_flow.root
        self.assertIsInstance(event_node_1.item, EventA)

        handler_runtime_node_1 = event_node_1.child_nodes[0]
        self.assertEqual(handler_runtime_node_1.item.handler, handler_1)
        self.assertTrue(handler_runtime_node_1.item.succeeded)

        handler_runtime_node_2 = event_node_1.child_nodes[1]
        self.assertEqual(handler_runtime_node_2.item.handler, handler_2)
        self.assertTrue(handler_runtime_node_2.item.succeeded)

        event_node_2 = handler_runtime_node_1.child_nodes[0]
        self.assertIsInstance(event_node_2.item, EventB)

        event_node_3 = handler_runtime_node_1.child_nodes[1]
        self.assertIsInstance(event_node_3.item, EventC)

        handler_runtime_node_3 = event_node_2.child_nodes[0]
        self.assertEqual(handler_runtime_node_3.item.handler, handler_3)
        self.assertTrue(handler_runtime_node_3.item.succeeded)

        handler_runtime_node_4 = event_node_3.child_nodes[0]
        self.assertEqual(handler_runtime_node_4.item.handler, handler_4)
        self.assertTrue(handler_runtime_node_4.item.succeeded)

        event_node_4 = handler_runtime_node_3.child_nodes[0]
        self.assertIsInstance(event_node_4.item,EventD)

        handler_runtime_node_5 = event_node_4.child_nodes[0]
        self.assertEqual(handler_runtime_node_5.item.handler, handler_5)
        self.assertFalse(handler_runtime_node_5.item.succeeded)

        self.assertIsNotNone(process_flow.find_event(EventA)[0])
        self.assertIsNotNone(process_flow.find_event(EventB)[0])
        self.assertIsNotNone(process_flow.find_event(EventC)[0])
        self.assertIsNotNone(process_flow.find_event(EventD)[0])

    def test_no_emittion(self):

        mediator = Mediator()

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

        context = Context(mediator, EventA())
        context.process()
        process_flow = context.process_flow
        self.assertSequenceEqual(process_flow.find_event(EventB), (None, 'test'))


if __name__ == '__main__':
    unittest.main()

