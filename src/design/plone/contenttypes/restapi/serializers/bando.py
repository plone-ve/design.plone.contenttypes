# -*- coding: utf-8 -*-
from .dxcontent import SerializeFolderToJson as BaseSerializer
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from design.plone.contenttypes.interfaces.bando import IBandoAgidSchema


@implementer(ISerializeToJson)
@adapter(IBandoAgidSchema, Interface)
class BandoSerializer(BaseSerializer):
    def get_approfondimenti(self, bando_view):
        """
        """
        folders = bando_view.retrieveFolderDeepening()
        results = []

        for folder in folders:
            contents = bando_view.retrieveContentsOfFolderDeepening(
                folder["path"]
            )
            folder.update({"children": contents})
            results.append(folder)
        return sorted(results, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        result = super(BandoSerializer, self).__call__(
            version=version, include_items=include_items
        )
        bando_view = self.context.restrictedTraverse("bando_view")
        result["approfondimento"] = self.get_approfondimenti(bando_view)
        result["bando_state"] = bando_view.getBandoState()
        return result
