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
@provider(IFormFieldProvider)
class IServiziCorrelati(model.Schema):

    servizi_correlati = RelationList(
        title=_(u"servizi_correlati_label", default=u"Servizi correlati"),
        description=_(
            u"servizi_correlati_description",
            default=u"Questi servizi non verranno mostrati nel contenuto, ma"
            " permetteranno di vedere questo contenuto associato quando si"
            " visita il servizio",
        ),
        default=[],
        value_type=RelationChoice(
            title=u"Related", vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )
    form.widget(
        "servizi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Servizio"],
        },
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["servizi_correlati"],
    )


@implementer(IServiziCorrelati)
@adapter(IDexterityContent)
class ServiziCorrelati(object):
    """"""

    def __init__(self, context):
        self.context = context
