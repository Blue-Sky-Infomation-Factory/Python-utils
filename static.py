from typing import Generic, TypeVar


T=TypeVar('T')

class constant(Generic[T]):
	def __init__(self, value: T): self.value = value
	def __get__(self, instance, owner) -> T: return self.value
	def __set__(self, instance, value): raise AttributeError("Can't set attribute")
	def __delete__(self, instance): raise AttributeError("Can't delete attribute")

class abstractproperty:
	def __init__(self): pass # abstract
	def __get__(self, instance, owner): raise RuntimeError("Not implemented")
	def __set__(self, instance, value): raise RuntimeError("Not implemented")
	def __delete__(self, instance): raise RuntimeError("Not implemented")