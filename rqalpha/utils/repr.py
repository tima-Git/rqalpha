# -*- coding: utf-8 -*-
#
# Copyright 2016 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from six import iteritems

from .cached_property import CachedProperty


def property_repr(inst):
    # return pformat(properties(inst))
    return "%s(%s)" % (inst.__class__.__name__, properties(inst))


def slots_repr(inst):
    # return pformat(slots(inst))
    return "%s(%s)" % (inst.__class__.__name__, slots(inst))


def dict_repr(inst):
    # return pformat(inst.__dict__)
    return "%s(%s)" % (
        inst.__class__.__name__, {k: v for k, v in iteritems(inst.__dict__) if k[0] != "_"})


def properties(inst):
    result = {}
    for cls in inst.__class__.mro():
        for varname in iter_properties_of_class(cls):
            if varname[0] == "_":
                continue
            # FIXME 这里getattr在iter_properties_of_class中掉用过了，性能比较差，可以优化
            tmp = getattr(inst, varname)
            if varname == "positions":
                tmp = list(tmp.keys())
            if hasattr(tmp, '__simple_object__'):
                result[varname] = tmp.__simple_object__()
            else:
                result[varname] = tmp
    return result


def slots(inst):
    result = {}
    for slot in inst.__slots__:
        result[slot] = getattr(inst, slot)
    return result


def iter_properties_of_class(cls):
    for varname in vars(cls):
        value = getattr(cls, varname)
        if isinstance(value, (property, CachedProperty)):
            yield varname
