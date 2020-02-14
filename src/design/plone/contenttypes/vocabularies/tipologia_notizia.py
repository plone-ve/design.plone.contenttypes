# -*- coding: utf-8 -*-

# from plone import api
from design.plone.contenttypes import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.schema.vocabulary import SimpleTerm
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class TipologiaNotizia(object):
    """ Vocabolario per le tipologie di notizie (non definitivo)
    """

    def __call__(self, context):

        registry = getUtility(IRegistry)
        values = registry.get(
            "design.plone.contenttypes.controlpanels.vocabularies.IVocabulariesControlPanel.news_tipologia_notizia",  # noqa
            default=""
        )
        if not values:
            return SimpleVocabulary([])

        values = values.splitlines()
        items = [VocabItem(value, value) for value in values]
        items.insert(0, VocabItem("", "-- seleziona un valore --"))

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


TipologiaNotiziaFactory = TipologiaNotizia()
