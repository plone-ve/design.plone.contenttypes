# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import IDeserializeFromJson
from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface
from AccessControl import getSecurityManager
from plone.restapi.deserializer.dxcontent import DeserializeFromJson


@implementer(IDeserializeFromJson)
@adapter(IPersona, Interface)
class DeserializePersonaFromJson(DeserializeFromJson):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.sm = getSecurityManager()
        self.permission_cache = {}
        self.modified = {}

    def __call__(
        self, validate_all=False, data=None, create=False
    ):  # noqa: ignore=C901

        if data is None:
            data = json_body(self.request)
        if data:
            if (
                "data_insediamento" in data
                and len(data["data_insediamento"]) > 10
            ):
                data["data_insediamento"] = data["data_insediamento"][0:10]

            if (
                "data_conclusione_incarico" in data
                and len(data["data_conclusione_incarico"]) > 10
            ):
                data["data_conclusione_incarico"] = data[
                    "data_conclusione_incarico"
                ][0:10]
        return super(DeserializePersonaFromJson, self).__call__(
            validate_all=False, data=data, create=False
        )
