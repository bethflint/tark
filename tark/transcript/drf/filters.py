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

from rest_framework.filters import BaseFilterBackend
from tark_drf.utils.drf_fields import CommonFields, DrfFields
from tark_drf.utils.drf_filters import CommonFilterBackend
from transcript.models import Transcript
from release.utils.release_utils import ReleaseUtils
from django.db.models import Q


class TranscriptFilterBackend(BaseFilterBackend):
    """
    Filter to filter by common fields..
    """
    def filter_queryset(self, request, queryset, view):
        queryset = CommonFilterBackend.get_common_filter_querysets(request, queryset, view)
        queryset = CommonFilterBackend.get_common_related_querysets(request, queryset, view)

        release_short_name = request.query_params.get('release_short_name', None)
        if release_short_name is not None:
            queryset = queryset.filter(transcript_release_set__shortname__icontains=release_short_name)

        return queryset

    def get_schema_fields(self, view):
        return CommonFields.get_common_query_set("Transcript") + CommonFields.COMMON_RELATED_QUERY_SET + \
                CommonFields.get_expand_query_set(Transcript)


class TranscriptDiffFilterBackend(BaseFilterBackend):
    """
    Diff Filter
    """
    def filter_queryset(self, request, queryset, view):
        stable_id = request.query_params.get('stable_id', 'ENST00000171111')
        if stable_id is not None:
            queryset = queryset.filter(stable_id=stable_id)

        diff_me_release = request.query_params.get('diff_me_release', None)
        diff_with_release = request.query_params.get('diff_with_release', ReleaseUtils.get_latest_release())

        diff_me_assembly = request.query_params.get('diff_me_assembly', ReleaseUtils.get_latest_assembly())
        diff_with_assembly = request.query_params.get('diff_with_assembly', ReleaseUtils.get_latest_assembly())

        expand_all = request.query_params.get('expand_all', "true")

        print("Stable id " + str(stable_id) + "Diff me " + str(diff_me_release) +
              "Diff with " + str(diff_with_release) + "expand all " + expand_all)

        if diff_me_release is not None and diff_me_assembly is not None:
            queryset_me = queryset.filter(assembly__assembly_name__icontains=diff_me_assembly). \
                filter(transcript_release_set__shortname=diff_me_release)
            print("=======queryset_me============")

            # get the exontranscript object so you have access to the order of exons
            # ringos_membership = ringo.membership_set.get(group=beatles)

            print("===================")
            queryset_with = queryset.filter(assembly__assembly_name__icontains=diff_with_assembly). \
                filter(transcript_release_set__shortname=diff_with_release)

            queryset = queryset_me | queryset_with   # queryset will contain all unique records of q1 + q2

        return queryset.distinct()

    def get_schema_fields(self, view):
        return [DrfFields.stable_id_field("Transcript"), DrfFields.diff_me_release_field(),
                DrfFields.diff_me_assembly_field(), DrfFields.diff_with_release_field(),
                DrfFields.diff_with_assembly_field(), DrfFields.get_expand_transcript_release_set_field()]


class TranscriptSearchFilterBackend(BaseFilterBackend):
    """
    Diff Filter
    """
    def filter_queryset(self, request, queryset, view):
        identifier = request.query_params.get('identifier_field', None)
        search_assembly = request.query_params.get('search_assembly')
        search_release = request.query_params.get('search_release')

        print("identifier " + str(identifier) + "search_assembly " + str(search_assembly) +
              "search_release " + str(search_release))

        if identifier is not None:
            # queryset = queryset.filter(Q(stable_id=identifier) | Q(genes__stable_id=identifier) |
            # Q(genes__hgnc__name__icontains=identifier))
            print(" Identifier " + identifier)
            if "ENST" in identifier:
                queryset = queryset.filter(stable_id=identifier)
            elif "ENSG" in identifier:
                queryset = queryset.filter(genes__stable_id=identifier)
            else:
                queryset = queryset.filter(genes__hgnc__name__iexact=identifier)

            if search_assembly is not None and len(search_assembly) > 1:
                queryset = queryset.filter(assembly__assembly_name__iexact=search_assembly)

            if search_release is not None and len(search_release) > 1:
                queryset = queryset.filter(transcript_release_set__shortname=search_release)



        return queryset.distinct()

    def get_schema_fields(self, view):
        return [DrfFields.identifier_field(), DrfFields.search_release_field(),
                DrfFields.search_assembly_field(), DrfFields.get_expand_all_field()]
