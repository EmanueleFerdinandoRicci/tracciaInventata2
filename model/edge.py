from dataclasses import dataclass

from model.customer import Customer
from model.track import Track


@dataclass
class Edge:
    c1: Customer
    c2: Customer
    p1: float
    p2: float