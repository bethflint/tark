'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


class FilterNotFound(LookupError):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class AssemblyNotFound(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class ReleaseNotFound(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class FeatureNotFound(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class MissingTranscriptError(LookupError):
    "No transcript has been associated with the mapper"


class FeatureNonCoding(LookupError):
    "This transcript doesn't have a translation"


class IncompatibleFeatureType(LookupError):
    "This feature isn't compatible with the operation requested"


class LocationNotInFeature(ValueError):
    "The location isn't contained in the given feature"


class BadLocationCoordinates(ValueError):
    "The location coordinates are either incorrectly formatted or otherwise invalid"


class UnknownCoordinateSystem(ValueError):
    "The coordinate system isn't known"


class WrongStrandError(TypeError):
    "The strand doesn't match between the given features"