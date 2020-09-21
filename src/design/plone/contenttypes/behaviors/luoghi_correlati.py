# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.component import adapter
from zope.interface import provider, implementer


# TODO: merge with NEWS
class ILuoghiCorrelatiSchema(model.Schema):

    luoghi_correlati = RelationList(
        title=_("luoghi_correlati_label", default="Luoghi correlati"),
        description=_(
            "luoghi_correlati_help",
            default="Seleziona una lista di luoghi citati.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )
    form.widget(
        "luoghi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["Venue"],
        },
    )


@provider(IFormFieldProvider)
class ILuoghiCorrelati(ILuoghiCorrelatiSchema):
    """
    Default fieldset
    """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["luoghi_correlati"],
    )


@provider(IFormFieldProvider)
class ILuoghiCorrelatiEvento(ILuoghiCorrelatiSchema):
    """
    Events have a differente fieldset for this field
    """

    model.fieldset(
        "luogo",
        label=_("luogo_label", default=u"Luogo"),
        fields=["luoghi_correlati"],
    )


@implementer(ILuoghiCorrelati)
@adapter(IDexterityContent)
class LuoghiCorrelati(object):
    """
    """

    def __init__(self, context):
        self.context = context


@implementer(ILuoghiCorrelatiEvento)
@adapter(IDexterityContent)
class LuoghiCorrelatiEvento(object):
    """
    """

    def __init__(self, context):
        self.context = context
