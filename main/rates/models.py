from sqlalchemy import Index
from sqlalchemy.orm import relationship

from ..extensions import db, BaseModel


class Price(BaseModel):
    __tablename__ = 'prices'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    orig_code = db.Column(db.String(),
                          db.ForeignKey("ports.code"), nullable=False)
    dest_code = db.Column(db.String(),
                          db.ForeignKey("ports.code"), nullable=False)
    day = db.Column(db.DATE)
    price = db.Column("price", db.DECIMAL)

    origin_port = relationship("Port",
                               backref="price_from_origin",
                               foreign_keys="[Price.orig_code]")
    destination_port = relationship("Port",
                                    backref="price_from_destination",
                                    foreign_keys="[Price.dest_code]")
    __table_args__ = (Index('price_index', "orig_code", "dest_code", "day"),)

    def __init__(self, orig_code, dest_code, day, price, **kwargs):
        db.Model.__init__(self, orig_code=orig_code,
                          dest_code=dest_code,
                          day=day, price=price, **kwargs
                          )
