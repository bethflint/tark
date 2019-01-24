'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2019] EMBL-European Bioinformatics Institute

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
from release.models import ReleaseSet, ReleaseSource, TranscriptReleaseTag
from django.db.models.aggregates import Max
from django.conf import settings
from assembly.models import Assembly
from numpy import source
from django.db.models import Q


class ReleaseUtils(object):

    @classmethod
    def get_latest_release(cls):
        current_release = getattr(settings, "CURRENT_RELEASE", "92")

        if current_release is None:
            current_release = ReleaseSet.objects.all().aggregate(Max('shortname'))
            if 'shortname__max' in current_release:
                return current_release['shortname__max']

        return current_release

    @classmethod
    def get_latest_assembly(cls):
        current_assembly = getattr(settings, "CURRENT_ASSEMBLY", "GRCh38")
        return current_assembly

    @classmethod
    def get_default_source(cls):
        default_source = getattr(settings, "DEFAULT_SOURCE", "ensembl")
        return default_source

    @classmethod
    def get_all_releases(cls, assembly_name=None):
        if assembly_name is None:
            assembly_name = cls.get_latest_assembly()

        all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name)
        return all_releases

    @classmethod
    def get_all_release_short_names(cls, assembly_name=None, source_name=None):
        if assembly_name is None:
            assembly_name = cls.get_latest_assembly()

        if source_name is None:
            source_name = cls.get_default_source()

        if source_name is "all":
            all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name).values('shortname')
        else:
            all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name).\
                filter(source__shortname__iexact=source_name).values('shortname')

        all_release_short_names = [release["shortname"] for release in all_releases]

        return sorted(all_release_short_names, reverse=True)

    @classmethod
    def get_all_assemblies(cls):
        all_assemblies = Assembly.objects.all()
        return all_assemblies

    @classmethod
    def get_all_assembly_names(cls):
        all_assemblies = Assembly.objects.all().values('assembly_name')
        all_assembly_names = [assembly["assembly_name"] for assembly in all_assemblies]
        return all_assembly_names

    @classmethod
    def get_all_assembly_releases(cls, source_name=None):
        assembly_releases = {}
        all_assembly_names = cls.get_all_assembly_names()
        for assembly_name in all_assembly_names:
            if len(cls.get_all_release_short_names(assembly_name, source_name)) > 0:
                assembly_releases[assembly_name] = cls.get_all_release_short_names(assembly_name, source_name)

        return assembly_releases

    @classmethod
    def get_all_release_sources(cls):
        all_sources = ReleaseSource.objects.all().values('shortname')
        all_source_names = [source["shortname"] for source in all_sources]
        return all_source_names

    @classmethod
    def get_release_diff(cls, diff_dict):
        print("get release diff called")
        set1_params = diff_dict['release_set_1']
        set2_params = diff_dict['release_set_2']

        # param_keys = ["source", "assembly", "version"]

        queryset_all = TranscriptReleaseTag.objects.all()
        queryset1 = queryset_all.filter(Q(release__source__shortname__iexact=str(set1_params["source"]))
                                     & Q(release__shortname__iexact=set1_params["version"])
                                     & Q(release__assembly__assembly_name__iexact=str(set1_params["assembly"]))
                                     )
        print(queryset1.query)
        queryset1_count = queryset1.count()
        print("Transcript count for set1 " + str(queryset1_count) )

        queryset_all = TranscriptReleaseTag.objects.all()
        queryset2 = queryset_all.filter(Q(release__source__shortname__iexact=str(set2_params["source"]))
                                     & Q(release__shortname__iexact=set2_params["version"])
                                     & Q(release__assembly__assembly_name__iexact=str(set2_params["assembly"]))
                                     )

        print(queryset2.query)
        queryset2_count = queryset2.count()
        print("Transcript count for set2 " + str(queryset2_count))

        # intersection
        qs_intersection = queryset1 & queryset2
        qs_intersection_count = qs_intersection.count()
        print("Intersection of set1 and set2 count " + str(qs_intersection.count()))

        # difference set1-set2
        qs1_qs2_difference_count = queryset1_count - qs_intersection_count
        print("Difference of set1 - set2 count " + str(qs1_qs2_difference_count))


        # difference set2-set2
        qs2_qs1_difference_count = queryset2_count - qs_intersection_count
        print("Difference of set2 - set1 count " + str(qs2_qs1_difference_count))

