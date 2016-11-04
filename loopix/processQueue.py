from twisted.internet import reactor, task, defer, threads
import heapq
import time
import copy
from twisted.internet.defer import DeferredQueue, DeferredLock
import weakref

class ProcessQueue():

	def __init__(self, parent):
		self.queue = []
		self.consumers = []

		self.parent = weakref.ref(parent)

	def put(self, obj):
		self.queue.append(obj)
		print "Putting to the queue."
		#print "Current size PUT: ", len(self.queue)

	def get(self):
		print "Process Queue: Called get"
		d = defer.Deferred()
		self.consumers += [d]

		reactor.callLater(0.0, self._process)
		return d

	def _process(self):
		print "--- Called _process in ProcessQueue file"
		try:
			if self.queue == []:
				print "Seems the queue is empty"
				self.parent.processQueue.get().addCallback(self.parent.do_PROCESS)
			else:
				print "Else condition"
				while self.consumers != [] and self.queue != []:
					print "Inside while"
					d = self.consumers.pop(0)
					obj = self.queue.pop(0)
					dt = threads.deferToThread(self._process_in_thread, d, obj)
		except Exception, e:
			print str(e)

	def _process_in_thread(self, d, obj):
		print "---- Called process in thread in ProcessQueue ------"
		d.callback(obj)
	


