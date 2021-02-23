# -*- coding: utf-8 -*-
from slugify import slugify

from ..extensions import db, BaseModel


class Region(BaseModel):
    __tablename__ = 'regions'

    slug = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    parent_slug = db.Column("parent_slug", db.ForeignKey("regions.slug"))

    def __init__(self, name, parent_slug, slug=None):
        db.Model.__init__(self, name=name,
                          slug=slug or slugify(name, separator='_'),
                          parent_slug=parent_slug)

    def __repr__(self):
        return self.name


class Port(BaseModel):
    __tablename__ = 'ports'

    code = db.Column(db.String(5), unique=True, primary_key=True)
    name = db.Column(db.String(100))
    parent_slug = db.Column("parent_slug", db.ForeignKey("regions.slug"))

    def __init__(self, name, parent_slug, slug=None):
        db.Model.__init__(self, name=name,
                          slug=slug or slugify(name, separator='_'),
                          parent_slug=parent_slug
                          )
