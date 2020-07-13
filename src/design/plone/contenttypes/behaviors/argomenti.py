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


@provider(IFormFieldProvider)
class IArgomenti(model.Schema):
    """ Marker interface for Argomenti
    """

    tassonomia_argomenti = RelationList(
        title=_("tassonomia_argomenti_label", default="Tassonomia argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            " contenuto.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )
    form.widget(
        "tassonomia_argomenti",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Pagina Argomento"]},
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default=u"Correlati"),
        fields=["tassonomia_argomenti"],
    )

    # form.order_before(tassonomia_argomenti="IDublinCore.subjects")


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """
    """

    def __init__(self, context):
        self.context = context
